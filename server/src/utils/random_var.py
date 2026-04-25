import random


def get_otp() -> str:
    return str(random.randint(100000, 999999))
