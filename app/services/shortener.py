import random
import string


def generate_short_key(length: int = 8) -> str:
    """
    Генерирует случайный короткий ключ, состоящий из ASCII-символов и цифр.
    """
    return "".join(
        random.choices(string.ascii_letters + string.digits, k=length)
    )
