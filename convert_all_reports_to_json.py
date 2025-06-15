import os
import json
from bs4 import BeautifulSoup
import fitz  # PyMuPDF


def extract_text_from_html(file_path):
    # Load the HTML file
    with open(file_path, "r", encoding="utf-8") as file:
        soup = BeautifulSoup(file, "html.parser")

    # Find the main content div
    #content_div = soup.find("div", id="content")
    #if not content_div:
    #    content_div = soup


    # Remove unwanted elements like <img>, <hr>, <div class="footer">, etc.
    #for tag in content_div.find_all(['img', 'hr', 'script', 'style', 'div','p']):
    #    tag.decompose()


    # Extract and clean text
    #text = content_div.get_text(separator="\n", strip=True)
    text = soup.get_text(separator="\n", strip=True)
    return text

def extract_text_from_pdf(file_path):
    text = ""
    with fitz.open(file_path) as doc:
        for page in doc:
            text += page.get_text()
    return text.strip()

def collect_texts(root_dir):
    data = []
    for subdir, _, files in os.walk(root_dir):
        for file in files:
            ext = file.lower().split('.')[-1]
            full_path = os.path.join(subdir, file)
            try:
                if ext in ['html', 'htm']:
                    text = extract_text_from_html(full_path)
                elif ext == 'pdf':
                    text = extract_text_from_pdf(full_path)
                else:
                    continue  # Skip other files
                data.append({
                    "file_path": os.path.abspath(full_path),
                    "text": text
                })
            except Exception as e:
                print(f"Failed to process {full_path}: {e}")
    return data

if __name__ == "__main__":
    root_folder = "fomc_documents"
    output_json = "extracted_texts.json"
    
    result = collect_texts(root_folder)

    with open(output_json, "w", encoding="utf-8") as f:
        json.dump(result, f, ensure_ascii=False, indent=2)

    print(f"✅ Extracted texts saved to {output_json}")
