import pytest
from unittest.mock import patch, mock_open

from word_counter import (
    get_tally_from_file,
    get_text_from_file,
    get_word_counts,
)


test_data = [
    {
        "input_str": "I love you.",
        "expected": {
            "I": 1,
            "love": 1,
            "you.": 1,
        },
    },
    {
        "input_str": "I love you.\nDo you love me?",
        "expected": {
            "Do": 1,
            "I": 1,
            "love": 2,
            "me?": 1,
            "you": 1,
            "you.": 1,
        },
    },
]


@pytest.mark.parametrize(
    ["input_str", "expected"],
    [(x["input_str"], x["expected"]) for x in test_data],
)
def test_get_word_counts(input_str, expected):
    actual = get_word_counts(input_str)
    assert actual == expected


def test_get_text_from_file():
    with patch("builtins.open", mock_open(read_data="xyz\nabc")) as mock_file:
        filepath = "boink"
        actual = get_text_from_file(filepath)
        expected = "xyz\nabc"
        mock_file.assert_called_with(filepath)
        assert actual == expected


def test_get_tally_from_file():
    with patch("word_counter.get_text_from_file") as mock:
        mock.return_value = "foo bar baz bar"
        filepath = "something.txt"
        actual = get_tally_from_file(filepath)
        expected = {
            "bar": 2,
            "baz": 1,
            "foo": 1,
        }
        assert actual == expected
        mock.assert_called_with(filepath)
