from os.path import exists
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


def get_tally_from_file_no_cache(filepath) -> Tally:
    text = get_text_from_file(filepath)
    return get_word_counts(text)


def get_cache_filepath(filepath: str) -> str:
    divider = "/"
    parts = filepath.split(divider)
    *front, last = parts
    new_last = f".tally_{last}"
    front.append(new_last)
    return divider.join(front)


def get_from_cache(filepath: str) -> Tally:
    raise NotImplementedError()


def should_use_cache(filepath: str) -> bool:
    pass


def can_get_from_cache(cache_file: str) -> bool:
    return exists(cache_file)


def get_tally_from_file(filepath: str) -> Tally:
    """Get tally of words from file, defers to cache."""
    cache_file = get_cache_filepath(filepath)
    has_cache = can_get_from_cache(cache_file)
    use_cache = has_cache and should_use_cache(filepath)
    if use_cache:
        return get_from_cache(cache_file)
    else:
        return get_tally_from_file_no_cache(filepath)
