def normalized_string(string: str) -> str:
    """
    Normalize a string by removing leading and trailing whitespace and converting it to lowercase.

    Args:
        string (str): The string to normalize.

    Returns:
        str: The normalized string.
    """
    return string.strip().lower()
