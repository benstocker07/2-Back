import hashlib
import sys

def load_hashes(filename):
    with open(filename, "r") as f:
        return {line.strip() for line in f if line.strip()}

hash_codes = load_hashes("login.txt")

tries = 0
max_tries = 5

while tries < max_tries:
    login = input("Login Code: ").strip()
    login_hash = hashlib.sha256(login.encode()).hexdigest()

    if login_hash in hash_codes:
        print("Welcome")
        break
    else:
        tries += 1
        print(f"Invalid code. Attempts left: {max_tries - tries}")

if tries == max_tries:
    print("Too many invalid attempts. Exiting.")
    sys.exit(1)
