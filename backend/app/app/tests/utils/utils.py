import secrets
import string


def random_lower_string(k=32, alphabet=string.ascii_lowercase) -> str:
    return "".join(secrets.choice(alphabet) for _ in range(k))


def random_email() -> str:
    return f"{random_lower_string()}@{random_lower_string()}.com"
