import hashlib

codes = ["23081999", "27072001"]  # add new codes here
for c in codes:
    print(f"{c}: {hashlib.sha256(c.encode()).hexdigest()}")