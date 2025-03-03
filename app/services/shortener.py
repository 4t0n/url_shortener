import random
import string


def generate_short_key(length: int = 6) -> str:
    return "".join(
        random.choices(string.ascii_letters + string.digits, k=length)
    )
