# fastapi-backend

This project provides a small FastAPI backend located in `fastapi_app/`.
Install Python dependencies from `requirements.txt` and run the server on
port `8000` with:

```bash
uvicorn fastapi_app.main:app --reload
```

The React client is served via Vite. Start it with:

```bash
npm run dev
```

Set the environment variable `VITE_API_BASE_URL` to `http://localhost:8000`
so the frontend can connect to the API during development.
