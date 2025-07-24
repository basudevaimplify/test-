from datetime import datetime
from typing import Optional
from sqlmodel import SQLModel, Field

class Document(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    filename: str
    content_type: str
    uploaded_at: datetime = Field(default_factory=datetime.utcnow)
    status: str = "uploaded"
    extracted_data: Optional[str] = None
