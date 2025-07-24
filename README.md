# fastapi-backend

This repository uses a small FastAPI application in `fastapi_app/` instead of the previous Node/Express server. To run the API locally install dependencies from `requirements.txt` and start the server with:

```bash
uvicorn fastapi_app.main:app --reload
```

The React client is still served using Vite. Use `npm run dev` to start the client.
