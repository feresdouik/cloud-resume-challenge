const yearElement = document.querySelector("#year");
const visitElement = document.querySelector("#visit-count");
if (yearElement) yearElement.textContent = new Date().getFullYear();

async function loadVisitorCount() {
  if (!visitElement) return;
  try {
    const response = await fetch("/api/visits", { method: "POST" });
    if (!response.ok) throw new Error("Visitor API unavailable");
    const data = await response.json();
    visitElement.textContent = Number(data.visits).toLocaleString();
  } catch (error) {
    visitElement.textContent = "Unavailable";
    console.error("Could not load visitor count:", error);
  }
}
loadVisitorCount();