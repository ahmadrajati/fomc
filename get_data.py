import requests
import json
import os
import json
import requests
from pathlib import Path
from urllib.parse import urljoin
import time
# Configuration
BASE_URL = "https://www.federalreserve.gov"
#JSON_FILE = "data/final-hist.json"  # Your JSON file
JSON_FILE = "data/final-recent.json"  # Your JSON file
TARGET_TYPES = ["PrC", "St", "Trns", "ExCommMin", "HMin"]  # Document types to download
DOWNLOAD_FOLDER = "fomc_documents"  # Root download directory

def ensure_directory_exists(filepath):
    """Ensure the directory for a file exists"""
    directory = os.path.dirname(filepath)
    if directory and not os.path.exists(directory):
        os.makedirs(directory)

def download_file(url, filepath):
    """Download a file if it doesn't exist"""
    if os.path.exists(filepath):
        print(f"File already exists: {filepath}")
        return True,"exist"
    
    try:
        response = requests.get(url, stream=True, timeout=10)
        response.raise_for_status()
        
        ensure_directory_exists(filepath)
        
        with open(filepath, 'wb') as f:
            for chunk in response.iter_content(chunk_size=8192):
                f.write(chunk)
        print(f"Downloaded: {filepath}")
        return True,""
    except Exception as e:
        print(f"Failed to download {url}: {str(e)}")
        return False,"failed"

def process_document(item):
    """Process a single document item"""
    doc_type = item.get('type')
    if doc_type not in TARGET_TYPES:
        return
    
    # Handle items with direct URLs
    if 'url' in item:
        url = item['url']
        if not url.startswith(('http://', 'https://')):
            url = urljoin(BASE_URL, url)
        
        # Create local path preserving URL structure
        relative_path = url.replace(BASE_URL, '').lstrip('/')
        local_path = os.path.join(DOWNLOAD_FOLDER, relative_path)
        
        st,m = download_file(url, local_path)
        if m!="exist":
            time.sleep(3)
    # Handle items with multiple files
    if 'files' in item:
        for file_item in item['files']:
            url = file_item['url']
            if not url.startswith(('http://', 'https://')):
                url = urljoin(BASE_URL, url)
            
            relative_path = url.replace(BASE_URL, '').lstrip('/')
            local_path = os.path.join(DOWNLOAD_FOLDER, relative_path)
            
            st,m = download_file(url, local_path)
            if m!="exist":
                time.sleep(3)
def main():
    # Load JSON data
    try:
        with open(JSON_FILE, 'r', encoding='utf-8') as f:
            data = json.load(f)
    except Exception as e:
        print(f"Error loading JSON file: {str(e)}")
        return
    
    # Process all documents
    if 'mtgitems' in data:
        for item in data['mtgitems']:
            if 'd' in item:
                if int(item['d'][:4])<2000:
                    continue
            print(item)
            process_document(item)
    else:
        print("No 'mtgitems' found in JSON data")

if __name__ == "__main__":
    main()