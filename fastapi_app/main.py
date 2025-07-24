from fastapi import FastAPI, UploadFile, File
from typing import List

app = FastAPI(title="Test API")

@app.get("/")
async def root():
    return {"message": "FastAPI backend is running"}

@app.post("/api/upload")
async def upload_file(file: UploadFile = File(...)):
    # In a real application you would save the file and process it
    return {"filename": file.filename}

@app.post("/api/process/{document_id}")
async def process_document(document_id: str):
    return {"document_id": document_id, "status": "processed"}

@app.post("/api/reprocess/{document_id}")
async def reprocess_document(document_id: str):
    return {"document_id": document_id, "status": "reprocessed"}

@app.get("/api/status/{document_id}")
async def status(document_id: str):
    return {"document_id": document_id, "processing": "complete"}

@app.post("/api/bulk-process")
async def bulk_process(document_ids: List[str]):
    return {"processed": document_ids}

@app.get("/api/statistics")
async def statistics():
    return {"documents_processed": 0}
