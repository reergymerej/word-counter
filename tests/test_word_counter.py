import re
from typing import Dict, List


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


def test_get_word_counts():
    actual = get_word_counts("I love you.")
    expected = {
        "I": 1,
        "love": 1,
        "you.": 1,
    }
    assert actual == expected

    actual = get_word_counts("I love you.\nDo you love me?")
    expected = {
        "Do": 1,
        "I": 1,
        "love": 2,
        "me?": 1,
        "you": 1,
        "you.": 1,
    }
    assert actual == expected
