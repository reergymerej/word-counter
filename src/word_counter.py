import re
from typing import Dict, List

from custom_types import Tally


def get_text_from_file(filepath: str) -> str:
    with open(filepath) as f:
        return f.read()


def get_words(input: str) -> List[str]:
    """
    Get the words from an input string.
    """
    words = re.split(r"\s", input)
    return words


def get_word_counts(input: str) -> Tally:
    words = get_words(input)
    tally: Dict[str, int] = {}
    for word in words:
        if word in tally:
            tally[word] = tally[word] + 1
        else:
            tally[word] = 1

    return tally


def get_tally_from_file(filepath) -> Tally:
    text = get_text_from_file(filepath)
    return get_word_counts(text)


def get_cache_file(filepath: str) -> str:
    divider = "/"
    parts = filepath.split(divider)
    *front, last = parts
    new_last = f".tally_{last}"
    front.append(new_last)
    return divider.join(front)
