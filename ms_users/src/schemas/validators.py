import re

def is_email(s: str) -> bool:
    """Проверяет, что строка это email

    Args:
        email (str): Строка, которую необходимо проверить

    Returns:
        bool: True если строка это email
    """
    match = re.search(r'[^@ ]+@[^@ ]+\.[^@ ]+', s)
    return match is not None and match.group(0) == s