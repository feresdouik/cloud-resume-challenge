# Cloud Resume Challenge — Feres Douik

A cloud-hosted developer resume with a persistent visitor counter, a Python API, automated tests, and CI/CD deployment to a Vultr VPS.

## Stack
- Frontend: semantic HTML, responsive CSS, vanilla JavaScript
- API: Python 3.12 + FastAPI
- Database: SQLite with a persistent Docker volume
- Web server: Nginx
- Containerization: Docker Compose
- Testing: Pytest + FastAPI TestClient
- CI/CD: GitHub Actions
- Cloud: Vultr Ubuntu 24.04

## Architecture
Browser → Nginx → static resume and /api/* reverse proxy → FastAPI → SQLite.

On each page load, the browser sends POST /api/visits to increment the counter. The API returns the new total. GET /api/visits reads the current total without incrementing it.

## Run locally
Requirements: Docker Desktop with Docker Compose, or Python 3.12.

### Docker
```bash
docker compose up --build
```
Open http://localhost. API health: http://localhost/api/health.

### Python
```bash
python -m venv .venv
# Windows:
.venv\Scripts\activate
# macOS/Linux:
# source .venv/bin/activate
pip install -r requirements.txt
uvicorn app.main:app --reload
```
The API will be available at http://127.0.0.1:8000.

## API
| Method | Endpoint | Description |
|---|---|---|
| GET | /api/health | Health check |
| GET | /api/visits | Read current visitor total |
| POST | /api/visits | Increment and return visitor total |

Example:
```bash
curl -X POST http://localhost/api/visits
# {"visits": 1}
curl http://localhost/api/visits
# {"visits": 1}
```

## Tests
```bash
pytest -v
```
The test suite checks the health endpoint and verifies that visitor counts increment and persist in SQLite.

## CI/CD
The GitHub Actions workflow in .github/workflows/ci-cd.yml runs tests for pull requests and pushes to main. A successful push to main triggers deployment over SSH.

Configure these repository Actions secrets before enabling deployment:
- VULTR_HOST: public IPv4 address of the Vultr instance
- VULTR_USER: deployment SSH username
- VULTR_SSH_KEY: private SSH key authorized on the instance

The VPS must have Docker Engine and the Compose plugin installed, and the repository must be cloned to /opt/cloud-resume-challenge.

## Vultr deployment
1. Create an Ubuntu 24.04 instance and configure SSH access.
2. Point your domain's DNS A record to the instance IPv4 address.
3. Run the VPS setup script as root: sudo bash infra/setup-vps.sh
4. Start the app from /opt/cloud-resume-challenge with docker compose up -d --build.
5. Configure HTTPS for your domain before announcing the site publicly. The current Nginx container config is the HTTP bootstrap; TLS termination and certificate renewal remain to be configured.

## Security
- Do not commit passwords, private keys, API tokens, or production environment files.
- Use GitHub Actions Secrets for deployment credentials.
- Keep SSH access restricted and allow only required inbound ports.
- SQLite data is stored in a named Docker volume, not in the Git repository.

## Project status
- [x] Responsive resume page
- [x] FastAPI visitor counter backed by SQLite
- [x] Automated API tests
- [x] GitHub Actions test and deployment workflow
- [x] Docker Compose and VPS bootstrap script
- [ ] Vultr instance and DNS configuration
- [ ] HTTPS certificate and automatic renewal
- [ ] Successful live deployment

Built by [Feres Douik](https://github.com/feresdouik).