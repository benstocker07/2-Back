try:
    import requests
except ImportError:
    import subprocess
    import sys
    subprocess.check_call([sys.executable, "-m", "pip", "install", "requests"])
    import requests

import zipfile
import io
import os
import platform
import subprocess
import ctypes
import shutil

def download_and_extract_zip(zip_url, extract_to="."):
    print(f"Downloading {zip_url}...\n")
    response = requests.get(zip_url)
    response.raise_for_status()

    print("Extracting repository...\n")
    with zipfile.ZipFile(io.BytesIO(response.content)) as z:
        z.extractall(extract_to)
        extracted_folder_name = z.namelist()[0].split('/')[0]

    new_cwd = os.path.join(extract_to, extracted_folder_name)
    os.chdir(new_cwd)
    print(f"Changed working directory to: {os.getcwd()}\n")

    if not os.listdir():
        print("Error: Extracted folder is empty. Please check the installation or the ZIP contents.")
    else:
        print("Files in current directory:", os.listdir())

    return platform.system()

def ensure_sh_file():
    if not os.path.exists("2-Back.sh"):
        with open("2-Back.sh", "w") as f:
            f.write("#!/bin/bash\n\npython3 2-Back.py\n")
        subprocess.run(["chmod", "+x", "2-Back.sh"])
        print("Created and made 2-Back.sh executable.")

if __name__ == "__main__":
    zip_url = "https://github.com/benstocker07/2-Back/archive/refs/heads/main.zip"
    extract_to = "2-Back"

    system_type = download_and_extract_zip(zip_url, extract_to)

    print(f'\nOS Type: {system_type}')

    if system_type == 'Windows':
        
        #script_path = "dist/2-Back.py"
        subprocess.run("2-Back.bat")
