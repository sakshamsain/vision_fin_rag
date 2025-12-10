from fastapi import APIRouter, UploadFile, File, HTTPException
from pathlib import Path
import uuid
from .config import DATA_RAW_DIR
from .models import IndexPDFRequest, QueryRequest, AnswerResponse, PageMetadata
from .pdf_utils import pdf_to_images
from .embeddings import index_pages
from .retrieval import answer_question

router = APIRouter()

@router.post("/upload_pdf")
async def upload_pdf(company: str, year: int, file: UploadFile = File(...)):
    DATA_RAW_DIR.mkdir(parents=True, exist_ok=True)
    fname = f"{company}_{year}_{file.filename}"
    dest = DATA_RAW_DIR / fname
    with open(dest, "wb") as f:
        f.write(await file.read())
    return {"pdf_filename": fname}

@router.post("/index_pdf")
def index_pdf(req: IndexPDFRequest):
    images = pdf_to_images(req.company, req.year, req.pdf_filename)
    pages_meta = []
    for page_num, img_path in images:
        pages_meta.append(
            PageMetadata(
                id=str(uuid.uuid4()),
                company=req.company,
                year=req.year,
                page_num=page_num,
                image_path=str(img_path),
            )
        )
    index_pages(req.company, req.year, pages_meta)
    return {"status": "ok", "pages_indexed": len(pages_meta)}

@router.post("/ask", response_model=AnswerResponse)
def ask_question(req: QueryRequest):
    if not req.question:
        raise HTTPException(status_code=400, detail="Question is required")
    return answer_question(req)
