const status = document.querySelector("#api-status");

try {
  const response = await fetch("/api/health");
  if (!response.ok) {
    throw new Error(`Health check returned HTTP ${response.status}`);
  }

  const result = await response.json();
  status.textContent = result.status === "ok"
    ? "Backend connected."
    : "Unexpected backend status.";
} catch {
  status.textContent = "Could not connect to the backend.";
}
