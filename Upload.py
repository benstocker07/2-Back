import os, ctypes, shutil, ssl, csv
from discord_webhook import DiscordWebhook
import requests

def read_participant_number():
    try:
        with open(f'{addpath}participant_number.txt', "r") as file:
            participant_number = file.read().strip()
            return participant_number

try:
    response = requests.get("https://api.ipify.org?format=json")
    response.raise_for_status()
    ip = response.json()["ip"]
    print(f"Your public IP is: {ip}")
except requests.RequestException as e:
    print(f"Error getting IP: {e}")

FeedID = f'Data for Participant {participant_number} from {ip}'
FeedID = str(FeedID)

hook = "https://discord.com/api/webhooks/1408447427299508267/5TycmtSrzT9AIyUsgUAAHHoeZbkop8PkK1Ck-PTs-fmPGfwZS1mNkYr52DUi2CmhlWl9"

webhook = DiscordWebhook(url=hook, username="File Upload", thread_id=FeedID)

LOCAL_SAVE_PATH = "dist/unsent_data.csv"
current_dir = os.getcwd()
print(current_dir)

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
        with open(LOCAL_SAVE_PATH, "rb") as f:
            webhook.add_file(file=f.read(), filename=LOCAL_SAVE_PATH)

        response = webhook.execute()

        if response.status_code == 400:
            webhook2 = DiscordWebhook(url=hook, username="File Upload", thread_name=str(FeedID))
            with open(LOCAL_SAVE_PATH, "rb") as f:
                webhook2.add_file(file=f.read(), filename=LOCAL_SAVE_PATH)

            response = webhook2.execute()
        print("Bulk upload successful. Deleting local file...")
        
        #os.remove(LOCAL_SAVE_PATH)
        
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

files = [f for f in os.listdir(current_dir) if os.path.isfile(os.path.join(current_dir, f))]

print(files)

#removal()
