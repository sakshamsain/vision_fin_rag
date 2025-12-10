import fitz  # PyMuPDF
from pathlib import Path
from .config import DATA_RAW_DIR, DATA_PROCESSED_DIR

def pdf_to_images(company: str, year: int, pdf_filename: str):
    pdf_path = DATA_RAW_DIR / pdf_filename
    out_dir = DATA_PROCESSED_DIR / company / str(year)
    out_dir.mkdir(parents=True, exist_ok=True)

    doc = fitz.open(pdf_path)
    image_paths = []
    for page_num in range(len(doc)):
        page = doc.load_page(page_num)
        pix = page.get_pixmap(dpi=150)
        img_path = out_dir / f"page_{page_num+1}.png"
        pix.save(str(img_path))
        image_paths.append((page_num + 1, img_path))
    doc.close()
    return image_paths
