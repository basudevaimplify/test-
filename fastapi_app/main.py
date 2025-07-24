from pathlib import Path
from typing import List

from fastapi import Depends, FastAPI, File, HTTPException, UploadFile
from fastapi.middleware.cors import CORSMiddleware
from sqlmodel import Session, select

from .auth import User, authenticate_user, get_current_user
from .db import get_session, init_db
from .models import Document
from .processing import process_file

app = FastAPI(title="Document API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.on_event("startup")
def on_startup():
    init_db()

@app.post("/api/login")
def login(username: str, password: str):
    token = authenticate_user(username, password)
    if not token:
        raise HTTPException(status_code=401, detail="Invalid credentials")
    return {"access_token": token, "token_type": "bearer"}

@app.post("/api/upload")
async def upload_file(
    file: UploadFile = File(...),
    user: User = Depends(get_current_user),
    session: Session = Depends(get_session),
):
    uploads = Path("uploads")
    uploads.mkdir(exist_ok=True)
    file_path = uploads / file.filename
    with file_path.open("wb") as f:
        f.write(await file.read())

    doc = Document(filename=file.filename, content_type=file.content_type)
    session.add(doc)
    session.commit()
    session.refresh(doc)
    return {"id": doc.id, "filename": doc.filename}

@app.post("/api/documents/{doc_id}/process")
async def process_document(
    doc_id: int,
    user: User = Depends(get_current_user),
    session: Session = Depends(get_session),
):
    doc = session.get(Document, doc_id)
    if not doc:
        raise HTTPException(status_code=404, detail="Document not found")
    file_path = Path("uploads") / doc.filename
    result = process_file(file_path, doc.content_type)
    doc.extracted_data = result
    doc.status = "processed"
    session.add(doc)
    session.commit()
    return {"id": doc.id, "status": doc.status}

@app.get("/api/documents", response_model=List[Document])
def list_documents(
    user: User = Depends(get_current_user),
    session: Session = Depends(get_session),
):
    return session.exec(select(Document)).all()

@app.get("/api/documents/{doc_id}", response_model=Document)
def get_document(
    doc_id: int,
    user: User = Depends(get_current_user),
    session: Session = Depends(get_session),
):
    doc = session.get(Document, doc_id)
    if not doc:
        raise HTTPException(status_code=404, detail="Document not found")
    return doc
