import fitz  # PyMuPDF
import requests
import os

def extract_text_from_pdf(file_path):
    doc = fitz.open(file_path)
    text = ""
    for page in doc:
        text += page.get_text()
    return text

def download_pdf_from_arxiv(arxiv_id, save_path="papers"):
    pdf_url = f"https://arxiv.org/pdf/{arxiv_id}.pdf"
    os.makedirs(save_path, exist_ok=True)
    local_path = os.path.join(save_path, f"{arxiv_id}.pdf")

    response = requests.get(pdf_url)
    if response.status_code == 200:
        with open(local_path, "wb") as f:
            f.write(response.content)
        return local_path
    else:
        raise Exception(f"Failed to download PDF: {pdf_url}")
