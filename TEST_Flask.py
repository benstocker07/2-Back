from flask import Flask, request, abort, jsonify
import os
import csv

app = Flask(__name__)

SECRET_TOKEN = os.environ.get("SECRET_TOKEN")

@app.route(f"/append/<token>", methods=["POST"])
def append_data(token):
    if token != SECRET_TOKEN:
        abort(403)

    data = request.get_json()
    if not data:
        return jsonify({"error": "Missing JSON"}), 400

    row = {
        "source": data.get("source"),
        "participant_number": data.get("payload", {}).get("participant number"),
        "reaction_time": data.get("payload", {}).get("reaction_time"),
        "score": data.get("payload", {}).get("score")
    }

    file_exists = os.path.isfile("log.csv")
    with open("log.csv", "a", newline='') as f:
        writer = csv.DictWriter(f, fieldnames=row.keys())
        if not file_exists:
            writer.writeheader()
        writer.writerow(row)

    return jsonify({"status": "success"}), 200

if __name__ == "__main__":
    app.run(host="127.0.0.1", port=2121)
