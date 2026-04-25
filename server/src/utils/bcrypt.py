import bcrypt


def hash_password(password: str) -> str:
    return bcrypt.hashpw(password.encode("utf-8"), bcrypt.gensalt()).decode()


def check_password(encoded_pass: str, password: str) -> bool:
    return bcrypt.checkpw(password.encode("utf-8"), encoded_pass.encode())
