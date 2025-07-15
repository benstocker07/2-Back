import os
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
        client = MongoClient("mongodb+srv://2-Back:CTGKXTNQ6SjpGRk7@2-back.yeusf74.mongodb.net/")
        db = client["2-Back"]
        collection = db["results"]
        collection.insert_many(data)
        print("Bulk upload successful. Deleting local file...")
        os.remove(LOCAL_SAVE_PATH)
    except Exception as e:
        print(f"Bulk upload failed: {e}")

upload_local_csv()
