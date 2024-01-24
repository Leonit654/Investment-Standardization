def invert_dict(d: dict) -> dict:
    inverted_dict = {}
    for key, value in d.items():
        inverted_dict.setdefault(value, []).append(key)
    return inverted_dict
