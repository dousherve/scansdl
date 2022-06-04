import sys, os
import argparse
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
        
def download(url: str, name: str = "", output_folder: str = "scans/raw"):
    """Download all the images found in the webpage at the given URL."""
    url = url[:-1] if url[-1] == '/' else url
    name = url.split('/')[-1] if (not name or len(name) == 0) else name
    output_folder = f"{output_folder}/{name}"

    if not os.path.exists(output_folder):
        os.makedirs(output_folder)

    print("Downloading scans:\n")

    soup = BeautifulSoup(fetch_data(url), 'html.parser')
    i = 0
    for item in soup.find_all('img'):
        scan_url = item['src']
        if scan_url[:4] != 'http':
            continue
        i += 1
        ext = scan_url.split('.')[-1]
        ext = '.' + ext if '/' not in ext else ".jpg"
        print(f"    - {scan_url}")
        dl_img(scan_url, f"{output_folder}/{i}{ext}")
        
    print(f"\nDownloaded {i} scans from {url} in {output_folder}.\n")
    
def create_cbr(input_folder: str, name: str = "", output_folder: str = "scans/cbr"):
    """Create a CBR archive from all the scans contained in the specified folder."""
    input_folder = input_folder[:-1] if input_folder[-1] == '/' else input_folder
    
    if not os.path.isdir(input_folder) or len(os.listdir(input_folder)) == 0:
        return
        
    if not name or len(name) == 0:
        name = input_folder.split('/')[-1]
        
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)
    
    cbr_path = f"{output_folder}/{name}.cbr"
    with ZipFile(cbr_path, mode='w') as cbr:
        for scan in os.listdir(input_folder):
            cbr.write(f"{input_folder}/{scan}")
            
    return cbr_path

if __name__ == '__main__':
    parser = argparse.ArgumentParser(prog="scans_dl", description="Download and archive manga scans.")
    subparsers = parser.add_subparsers(dest="command")
    
    dl_parser = subparsers.add_parser("download", aliases=["dl", "d"], help="Download all manga scans at the given address.")
    dl_parser.add_argument("address", help="The address of the webpage(s) containing the scans.")
    dl_parser.add_argument("--range", "-r", type=str, help="The range of the chapters to download, in the form a-b. Use '{}' in the address to specify where to increment the chapter. You can also specify a single number, which will be the last chapter to download.")
    dl_parser.add_argument("--name", "-n", type=str, default="", help="The name of the manga.")
    dl_parser.add_argument("--foldername", "-f", type=str, default="", help="The name of the folder containing the scans to be downloaded.")
    dl_parser.add_argument("--output", "-o", type=str, help="The path where the scan(s) should be downloaded. A new folder will be created.")
    
    cbr_parser = subparsers.add_parser("cbr", help="Archive all the scans present in the given folder(s) in CBR format.")
    cbr_parser.add_argument("path", type=str, help="The path of the folder(s) containing the scans to archive.")
    cbr_parser.add_argument("--all", action="store_true", help="Look for all the subfolders in the given folder and create all the corresponding archives.")
    cbr_parser.add_argument("--name", "-n", type=str, default="", help="The name of the manga.")
    cbr_parser.add_argument("--filename", "-f", type=str, default="", help="The name of the archive(s) to create.")
    cbr_parser.add_argument("--output", "-o", type=str, help="The path where the archive(s) should be created.")
    
    if len(sys.argv) == 1:
        parser.print_help(sys.stderr)
        sys.exit(1)
    
    args = parser.parse_args()
    
    if args.command in ["download", "dl", "d"]:
        if "{}" in args.address and not args.range:
            print("Error: '{}' was found in the address, but no range was specified.", file=sys.stderr)
            sys.exit(1)
        
        if args.range:
            if "{}" not in args.address:
                print("Error: a range was specified, but '{}' missing in the address.", file=sys.stderr)
                sys.exit(1)
            
            raw_range = args.range.split('-')
            dl_range = None
            
            if len(raw_range) > 2 or '' in raw_range:
                print("Error: please specify the range in the form 'a-b', where a < b, i.e '1-10'. Or, specify a single number that will act as the last number of the range.", file=sys.stderr)
                sys.exit(1)
            
            raw_range = [int(x) for x in raw_range]
                
            if len(raw_range) == 1:
                dl_range = range(1, raw_range[0] + 1)
            else:
                dl_range = range(raw_range[0], raw_range[1] + 1)
                
            for i in dl_range:
                download(
                    args.address.format(i),
                    args.foldername + '-' + str(i) if args.foldername else "",
                    args.output if args.output else "scans/raw" + ('/' + args.name if args.name else "")
                )
        
        else:
            download(
                args.address,
                args.foldername,
                args.output if args.output else "scans/raw" + ('/' + args.name if args.name else "")
            )
        
    elif args.command == "cbr":
        if args.all:
            i = 0
            for chapter in os.listdir(args.path):
                if os.path.isfile(chapter):
                    continue
                
                i += 1
                path = create_cbr(
                    f"{args.path}/{chapter}",
                    args.filename + '-' + str(i) if args.filename else "",
                    args.output if args.output else "scans/cbr/" + args.path.split('/')[-1]
                )
                
                print(f"Created CBR file for {chapter}: {path}")
                
            print(f"\nCreated {i} CBR files.")
            
        else:
            path = create_cbr(
                args.path,
                args.filename,
                args.output if args.output else "scans/cbr/" + args.path.split('/')[-1]
            )
            print(f"\nArchive created: {path}")