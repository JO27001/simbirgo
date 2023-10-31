from hashlib import md5

SALT = "asdf"


def hash_string(string: str) -> str:
    hashed = md5((string + SALT).encode())
    return hashed.hexdigest()
