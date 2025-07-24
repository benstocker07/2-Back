import hashlib

codes = ["23081999", "27072001"]

with open("dist/login.txt", "w") as f:

    for code in codes:
        hash = hashlib.sha256(code.encode()).hexdigest()
        f.write(hash + "\n")
