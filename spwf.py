import hashlib
import sys

hash_codes = []

codes = ["23081999", "27072001"]

for c in codes:
    hashed = hashlib.sha256(c.encode()).hexdigest()
    hash_codes.append(hashed)

tries = 0
max_tries = 5

while tries < max_tries:
    login = input('Login Code: ').strip()
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