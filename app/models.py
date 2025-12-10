from pydantic import BaseModel
from typing import List, Optional

class IndexPDFRequest(BaseModel):
    company: str
    year: int
    pdf_filename: str  # stored under data/raw

class PageMetadata(BaseModel):
    id: str
    company: str
    year: int
    page_num: int
    image_path: str

class QueryRequest(BaseModel):
    question: str
    company: Optional[str] = None

class RetrievedPage(BaseModel):
    id: str
    score: float
    company: str
    year: int
    page_num: int
    image_path: str

class GraphFact(BaseModel):
    subject: str
    relation: str
    obj: str
    value: Optional[float] = None
    year: Optional[int] = None

class AnswerResponse(BaseModel):
    answer: str
    retrieved_pages: List[RetrievedPage]
    graph_facts: List[GraphFact]
