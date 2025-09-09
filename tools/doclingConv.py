from fastapi import FastAPI, File, UploadFile, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from supabase import create_client
from docling.document_converter import DocumentConverter
import os

SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_KEY = os.getenv("SUPABASE_KEY")
BUCKET_NAME = "documents"

supabase = create_client(SUPABASE_URL, SUPABASE_KEY)

app = FastAPI()

# Allow frontend to connect
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # replace with your frontend URL in production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

def upload_to_supabase(file: UploadFile) -> str:
    file_name = file.filename
    try:
        supabase.storage.from_(BUCKET_NAME).upload(file_name, file.file, {"upsert": True})
        return supabase.storage.from_(BUCKET_NAME).get_public_url(file_name)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Upload failed: {str(e)}")

def doc_convert(url: str) -> str:
    converter = DocumentConverter()
    result = converter.convert(url)
    return result.document.export_to_markdown()

@app.post("/upload-doc/")
async def upload_and_convert(file: UploadFile = File(...)):
    url = upload_to_supabase(file)
    try:
        markdown = doc_convert(url)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Docling failed: {str(e)}")
    return {"file_url": url, "markdown": markdown}
