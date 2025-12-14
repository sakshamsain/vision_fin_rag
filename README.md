# Vision-First Financial Document QA (ColPali + Neo4j Graph RAG)

## Overview

This project is a **vision-first RAG system for financial PDFs**, built on top of
**ColPali** for vision embeddings and **Neo4j** for a financial knowledge graph.

You upload annual / quarterly reports as PDFs, and the system answers questions like:

- "Why did profit drop in 2022 compared to 2021?"

Instead of relying only on OCR, it uses **ColPali** to embed each page as an image,
capturing **layout + tables + charts + text**. On top of that, it maintains a
**Neo4j knowledge graph** of financial metrics, so the LLM can combine
**visual retrieval** with **structured numeric reasoning**.


1. **Ingestion**
   - User uploads a financial PDF.
   - Backend converts each page to an image (PyMuPDF).
   - Each page becomes a vision chunk with metadata:
     - `company`, `year`, `page_num`, `image_path`.

2. **Vision Embeddings with ColPali**
   - For each page image, we use **ColPali** to compute a contextual vision embedding.
   - These embeddings are stored in a vector index (in-memory now, pluggable to Qdrant/Milvus).

3. **Neo4j Knowledge Graph (Graph RAG)**
   - A **Neo4j** graph stores financial facts extracted from the reports:
     - Nodes:
       - `(:Company {name: "DemoCorp"})`
       - `(:Metric {name: "revenue", year: 2023, value: 250000})`
     - Relationship:
       - `(:Company)-[:HAS_METRIC]->(:Metric)`
   - This enables:
     - Exact numeric lookup (revenue, net income, EPS)
     - Trends and comparisons across years.

   Example Cypher inserts:


4. **Hybrid Retrieval**
- At query time:
  - Question text is embedded with ColPali.
  - Cosine similarity search fetches the **most relevant pages**.
  - Neo4j is queried via Cypher for **matching financial facts**.
- Result: a set of **visual pages + Neo4j facts (triples)**.

5. **Answer Generation (VLM + LLM)**
- We build a prompt that includes:
  - User question
  - Neo4j facts (formatted as natural language statements)
  - References to retrieved pages (and optionally OCR/summaries)
- A Vision-Language Model (e.g., Llama‑3.2‑Vision) acts as a **financial analyst**
  and generates a grounded answer, often citing pages:
  - *"Net income dropped in 2022 mainly due to higher operating expenses.
     See pages 34–35 of the 2022 report."*

6. **Frontend**
- Streamlit UI provides:
  - PDF upload + ColPali-based indexing
  - Question input
  - Final answer
  - “Used context”: which pages and which Neo4j facts were used.

---

## Tech Stack

- **Language:** Python
- **Vision Embeddings:** ColPali (vision-late interaction model)
- **Vector Index:** in-memory multi-vector index (ready for Qdrant / Milvus)
- **Graph RAG:** **Neo4j** (financial metrics graph, queried via Cypher)
- **VLM / LLM:** Llama 3.x Vision / GPT-4V / Gemini (HTTP API)
- **PDF Processing:** PyMuPDF
- **Backend:** FastAPI
- **Frontend:** Streamlit

---

## Neo4j Setup

1. Install Neo4j (Desktop or Docker).
2. Create a database (e.g., `financial_graph`).
3. Set env vars or config:


4. The backend ETL scripts:
- Extract facts `(company, metric, year, value)` from PDF text.
- Write them into Neo4j using the schema above.

At query time, the backend calls helper functions like:


These results are injected into the LLM prompt as **structured facts**.

---

## Why this matters

- ColPali handles the **visual, unstructured** side of financial PDFs.
- Neo4j handles the **structured, numeric** side (exact values, trends).
- Together, they form a proper **Graph RAG over vision-based retrieval**.

> One-line pitch:  
> **"I built a vision-first financial QA system that combines ColPali for page-level visual retrieval with a Neo4j knowledge graph for precise financial reasoning."**
