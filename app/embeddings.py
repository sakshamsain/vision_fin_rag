# app/embeddings.py
from typing import List, Dict
import numpy as np
from .models import PageMetadata, RetrievedPage

# simple in-memory “vector DB”
_VECTORS: Dict[str, np.ndarray] = {}
_META: Dict[str, PageMetadata] = {}

DIM = 128

def init_qdrant_collection(dim: int = DIM):
    # kept for compatibility; does nothing
    pass

def _simple_embed(text: str, dim: int = DIM):
    rng = np.random.default_rng(abs(hash(text)) % (2**32))
    return rng.normal(size=(dim,)).astype("float32")

def index_pages(company: str, year: int, pages: List[PageMetadata]):
    for p in pages:
        vec = _simple_embed(f"{company} {year} page {p.page_num}")
        _VECTORS[p.id] = vec
        _META[p.id] = p

def search_pages(question: str, top_k: int = 5, company: str | None = None) -> List[RetrievedPage]:
    if not _VECTORS:
        return []
    qvec = _simple_embed(question)
    ids = list(_VECTORS.keys())
    vectors = np.stack([_VECTORS[i] for i in ids], axis=0)  # [N, D]
    # cosine similarity
    qn = qvec / (np.linalg.norm(qvec) + 1e-8)
    vn = vectors / (np.linalg.norm(vectors, axis=1, keepdims=True) + 1e-8)
    sims = vn @ qn
    scored = list(zip(ids, sims))
    if company:
        scored = [(i, s) for (i, s) in scored if _META[i].company.lower() == company.lower()]
    scored.sort(key=lambda x: x[1], reverse=True)
    top = scored[:top_k]
    results: List[RetrievedPage] = []
    for i, s in top:
        m = _META[i]
        results.append(
            RetrievedPage(
                id=i,
                score=float(s),
                company=m.company,
                year=m.year,
                page_num=m.page_num,
                image_path=str(m.image_path),
            )
        )
    return results
