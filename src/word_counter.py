import re
from typing import Dict, List


def get_text_from_file(filepath: str) -> str:
    with open(filepath) as f:
        return f.read()


def get_words(input: str) -> List[str]:
    """
    Get the words from an input string.
    """
    words = re.split(r"\s", input)
    return words


def get_word_counts(input: str) -> Dict[str, int]:
    words = get_words(input)
    tally: Dict[str, int] = {}
    for word in words:
        if word in tally:
            tally[word] = tally[word] + 1
        else:
            tally[word] = 1

    return tally
