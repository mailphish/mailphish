# Development guide

Use Python 3.11 or newer. Run the setup commands from the repository root.

## Windows PowerShell

```powershell
py -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install -r backend/requirements.txt
```

If PowerShell blocks activation, run `.\.venv\Scripts\python.exe -m pip install -r backend/requirements.txt` and then `.\.venv\Scripts\fastapi.exe dev`.

## macOS and Linux

```sh
python3 -m venv .venv
source .venv/bin/activate
python -m pip install -r backend/requirements.txt
```

## Start the development server

With the virtual environment active, run this from the repository root.

```sh
fastapi dev
```

FastAPI starts on port 8000 and reloads when Python files change. Refresh the browser after editing HTML or JavaScript. Press Ctrl+C to stop the server.

## How the frontend connects

1. Open [the local frontend](http://127.0.0.1:8000/). FastAPI serves `frontend/src/index.html` and its JavaScript using `StaticFiles`.
2. The browser calls `GET /api/health` from `frontend/src/app.js`. The relative URL uses the same host and port as the page.
3. FastAPI replies with `{"status":"ok"}` and the page displays **Backend connected.** Try the endpoint in [Swagger UI](http://127.0.0.1:8000/docs).

[`pyproject.toml`](../pyproject.toml) configures `backend.app.main:app` as the FastAPI CLI entry point. It refers to the `app` object in `backend/app/main.py`. Register new routes under `/api/` before the frontend mount. As the API grows, move related routes to `backend/app/routers/` and register them with `app.include_router()` before the mount. The starter uses plain HTML and JavaScript so the team can choose a frontend framework later.

- [FastAPI application layout and routers](https://fastapi.tiangolo.com/tutorial/bigger-applications/)
- [Serving static files with FastAPI](https://fastapi.tiangolo.com/tutorial/static-files/)
- [FastAPI CLI](https://fastapi.tiangolo.com/fastapi-cli/)
- [Email template conventions](../templates/emails/README.md)
