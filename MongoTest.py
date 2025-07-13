import json
import time
import random
from pymongo import MongoClient

import json

sample_data = [
    {
        "participant_number": random.randint(1,50),
        "reaction_time": random.randint(200, 500),
        "score": random.randint(0,1),
        "source": "generated"
    }
]

with open("data.json", "w") as f:
    json.dump(sample_data, f, indent=2)

print("data.json created")

client = MongoClient("mongodb+srv://2-Back:CTGKXTNQ6SjpGRk7@2-back.yeusf74.mongodb.net/")
db = client["2-Back"]
collection = db["results"]

# Load JSON data from file
with open("data.json", "r") as f:
    data = json.load(f)

# Insert data into MongoDB
if isinstance(data, list):
    collection.insert_many(data)
else:
    collection.insert_one(data)

print("Data sent")
time.sleep(5)

