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

    if not os.listdir():
        print("Error: Extracted folder is empty. Please check the installation or the ZIP contents.")
    else:
        print("All files imported")

    return platform.system()



if __name__ == "__main__":
    zip_url = "https://github.com/benstocker07/2-Back/archive/refs/heads/main.zip"
    extract_to = "2-Back"

    system_type = download_and_extract_zip(zip_url, extract_to)

    if system_type == "Darwin":
        print("Using MacOS")
        if not os.path.exists("2-Back.sh"):
            with open("2-Back.sh", "w") as f:
                f.write("#!/bin/bash\n\npython3 dist/Task_Setup.py\npython3 dist/MongoUpload.py\n")
            subprocess.run(["chmod", "+x", "2-Back.sh"])
            print("Created and made 2-Back.sh executable.")
        try:
            subprocess.run(["python3", "2-Back.sh"])
            print('Task loading')
        except Exception as e:
            print(e)

    if system_type == 'Windows':
        subprocess.run("2-Back.bat")
