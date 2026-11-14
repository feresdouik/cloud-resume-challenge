import os
import sqlite3
from contextlib import closing
from pathlib import Path

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

DATABASE_PATH = Path(os.getenv("DATABASE_PATH", "data/visits.db"))
app = FastAPI(title="Cloud Resume Visitor API", version="1.0.0")
app.add_middleware(
    CORSMiddleware,
    allow_origins=os.getenv("CORS_ORIGINS", "*").split(","),
    allow_methods=["GET", "POST"],
    allow_headers=["*"],
)


class VisitResponse(BaseModel):
    visits: int


def get_connection() -> sqlite3.Connection:
    DATABASE_PATH.parent.mkdir(parents=True, exist_ok=True)
    connection = sqlite3.connect(DATABASE_PATH, timeout=10)
    connection.row_factory = sqlite3.Row
    return connection


def initialize_database() -> None:
    with closing(get_connection()) as connection:
        connection.execute(
            """CREATE TABLE IF NOT EXISTS visitor_counter (
                id INTEGER PRIMARY KEY CHECK (id = 1),
                visits INTEGER NOT NULL DEFAULT 0
            )"""
        )
        connection.execute(
            "INSERT OR IGNORE INTO visitor_counter (id, visits) VALUES (1, 0)"
        )
        connection.commit()


@app.on_event("startup")
def on_startup() -> None:
    initialize_database()


@app.get("/api/health")
def health() -> dict[str, str]:
    return {"status": "ok"}


@app.get("/api/visits", response_model=VisitResponse)
def read_visits() -> VisitResponse:
    try:
        with closing(get_connection()) as connection:
            row = connection.execute(
                "SELECT visits FROM visitor_counter WHERE id = 1"
            ).fetchone()
        return VisitResponse(visits=row["visits"])
    except sqlite3.Error as exc:
        raise HTTPException(status_code=500, detail="Could not read visitor count") from exc


@app.post("/api/visits", response_model=VisitResponse)
def record_visit() -> VisitResponse:
    try:
        with closing(get_connection()) as connection:
            connection.execute("BEGIN IMMEDIATE")
            connection.execute(
                "UPDATE visitor_counter SET visits = visits + 1 WHERE id = 1"
            )
            row = connection.execute(
                "SELECT visits FROM visitor_counter WHERE id = 1"
            ).fetchone()
            connection.commit()
        return VisitResponse(visits=row["visits"])
    except sqlite3.Error as exc:
        raise HTTPException(status_code=500, detail="Could not update visitor count") from exc