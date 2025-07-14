import hashlib

hash_codes = []

codes = ["23081999", "27072001"]  # add new codes here

for c in codes:
    hashed = hashlib.sha256(c.encode()).hexdigest()
    hash_codes.append(hashed)

tries = 0 

while True:
    
    tries = tries + 1

    login = input('Login Code: ')
    
    login_hash = hashlib.sha256(login.encode()).hexdigest()
    print(f"Login hash: {login_hash}")

    if login_hash in hash_codes:
        print("Welcome")
    
    else:
        tries = tries + 1