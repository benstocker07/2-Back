import requests
import socket
import random

for i in range(1,100):

    reaction_time = random.randint(250, 500)
    score = random.randint(0, 1)
    participant_number = 1
        
    def get_local_ip():
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        try:
            s.connect(('10.255.255.255', 1))
            ip = s.getsockname()[0]
        except Exception:
            ip = '127.0.0.1'
        finally:
            s.close()
        return ip

    SECRET_TOKEN = "LJxO29nfIja8zpWI4g_sWSF_cV4759mOFkvTsBoxDsA"
    url = f"http://127.0.0.1:2121/append/{SECRET_TOKEN}"

    data = {
        "source": get_local_ip(),
        "payload": {
            "participant number": participant_number,
            "reaction_time": reaction_time,
            "score": score
        }
    }

    try:
        response = requests.post(url, json=data)
        response.raise_for_status()
        print(response.json)
    except requests.exceptions.HTTPError as e:
        print("HTTP error:", e.response.status_code, e.response.text)
    except Exception as e:
        print("Other error:", e)
