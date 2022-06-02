import os
import requests
from bs4 import BeautifulSoup
    
def fetch_data(url: str):
    r = requests.get(url)
    return r.text
    
def dl_img(url: str, file_path: str):
    r = requests.get(url)
    with open(file_path, "wb") as img:
        img.write(r.content)
        
def download(url: str, parent_folder: str="scans"):
    """Download all the images found in the webpage at the given URL."""
    manga = url.split('/')[-1]
    output_folder = f"{parent_folder}/{manga}"

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
