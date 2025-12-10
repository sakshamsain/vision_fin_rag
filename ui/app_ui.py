import streamlit as st
import requests

API_BASE = "http://localhost:8000/api"

st.set_page_config(page_title="Vision-First Financial RAG", layout="wide")

st.title("📊 Vision-First Financial Document QA")

st.sidebar.header("Upload & Index PDFs")

company = st.sidebar.text_input("Company", value="DemoCorp")
year = st.sidebar.number_input("Year", min_value=2000, max_value=2100, value=2023, step=1)

uploaded = st.sidebar.file_uploader("Upload PDF", type=["pdf"])
if uploaded is not None and st.sidebar.button("Upload & Index"):
    files = {"file": (uploaded.name, uploaded.getvalue(), "application/pdf")}
    params = {"company": company, "year": year}
    r = requests.post(f"{API_BASE}/upload_pdf", params=params, files=files)
    if r.status_code == 200:
        pdf_filename = r.json()["pdf_filename"]
        r2 = requests.post(f"{API_BASE}/index_pdf", json={
            "company": company,
            "year": year,
            "pdf_filename": pdf_filename
        })
        if r2.status_code == 200:
            st.sidebar.success(f"Indexed {r2.json()['pages_indexed']} pages.")
        else:
            st.sidebar.error(f"Index error: {r2.text}")
    else:
        st.sidebar.error(f"Upload error: {r.text}")

st.header("Ask a Question")

q = st.text_input("Your question")
if st.button("Ask") and q:
    r = requests.post(f"{API_BASE}/ask", json={"question": q, "company": company})
    if r.status_code == 200:
        data = r.json()
        st.subheader("Answer")
        st.write(data["answer"])

        st.subheader("Graph Facts Used")
        if data["graph_facts"]:
            for f in data["graph_facts"]:
                st.write(f"- {f['subject']} {f['relation']} {f['obj']} (value={f.get('value')}, year={f.get('year')})")
        else:
            st.write("No graph facts yet (you can add later).")

        st.subheader("Retrieved Pages (metadata)")
        for p in data["retrieved_pages"]:
            st.write(f"- {p['company']} {p['year']} page {p['page_num']} (score={p['score']:.4f})")
    else:
        st.error(f"Error: {r.text}")
