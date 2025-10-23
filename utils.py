import hashlib
from collections import Counter

def compute_properties(value: str):
    length = len(value)
    is_palindrome = value.strip().lower() == value.strip().lower()[::-1]
    unique_characters = len(set(value))
    word_count = len(value.split())
    sha_hash = hashlib.sha256(value.encode()).hexdigest()
    freq_map = dict(Counter(value))

    return {
        "length": length,
        "is_palindrome": is_palindrome,
        "unique_characters": unique_characters,
        "word_count": word_count,
        "sha256_hash": sha_hash,
        "character_frequency_map": freq_map,
    }


def parse_natural_language(query: str):
    q = query.lower()
    filters = {}

    if "single word" in q or "one word" in q:
        filters["word_count"] = 1
    if "palindrom" in q:
        filters["is_palindrome"] = True
    if "longer than" in q:
        import re
        match = re.search(r"longer than (\d+)", q)
        if match:
            filters["min_length"] = int(match.group(1)) + 1
    if "contain" in q:
        import re
        match = re.search(r"letter ([a-z0-9])", q)
        if match:
            filters["contains_character"] = match.group(1)

    if not filters:
        return None
    return {"original": query, "parsed_filters": filters}
