import os
import requests
from bs4 import BeautifulSoup
from zipfile import ZipFile
    
def fetch_data(url: str):
    r = requests.get(url)
    return r.text
    
def dl_img(url: str, file_path: str):
    r = requests.get(url)
    with open(file_path, "wb") as img:
        img.write(r.content)
        
def download(url: str, parent_folder: str = "scans/raw"):
    """Download all the images found in the webpage at the given URL."""
    manga = url.split('/')[-1]
    output_folder = f"{parent_folder}/{manga}"

    if not os.path.exists(output_folder):
        os.makedirs(output_folder)

    print("Downloading scans:")

    soup = BeautifulSoup(fetch_data(url), 'html.parser')
    i = 0
    for item in soup.find_all('img'):
        i += 1
        scan_url = item['src']
        ext = scan_url.split('.')[-1]
        print(f"    - {item['alt']} ({scan_url})")
        dl_img(scan_url, f"{output_folder}/{i}.{ext}")
        
    print(f"\nDownloaded {i} scans from {url} in {output_folder}.\n")
    
def create_cbr(folder: str, output_folder: str = "scans/cbr", name: str = ""):
    """Create a CBR archive from all the scans contained in the specified folder."""
    if not os.path.isdir(folder):
        return
        
    if not name:
        name = folder.split('/')[-1]
        
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)
    
    cbr_path = f"{output_folder}/{name}.cbr"
    with ZipFile(cbr_path, mode='w') as cbr:
        for scan in os.listdir(folder):
            cbr.write(f"{folder}/{scan}")
            
    return cbr_path
