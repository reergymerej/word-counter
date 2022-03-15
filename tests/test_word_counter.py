import pytest
from unittest.mock import MagicMock, patch, mock_open
from custom_types import Tally

from word_counter import (
    get_cache_file,
    get_cached_tally_from_file,
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


@pytest.mark.parametrize(
    ["filepath", "expected"],
    [
        (
            "all/in.me",
            "all/.tally_in.me",
        ),
        (
            "./foo.txt",
            "./.tally_foo.txt",
        ),
        (
            "bar.txt",
            ".tally_bar.txt",
        ),
    ],
)
def test_get_cache_file(filepath, expected):
    actual = get_cache_file(filepath)
    assert actual == expected


def test_get_cached_tally_from_file():

    # mock that the file exists
    with patch("word_counter.exists") as mock_exists:
        mock_exists.return_value = True

        filepath = "i_am/like_a.bird"
        cache_file = get_cache_file(filepath)

        # mock the result pulled from the cache
        with patch("word_counter.get_from_cache") as mock_get_from_cache:
            mock_get_from_cache.return_value = {
                "foo": 1,
                "bingo": 99,
            }

            actual = get_cached_tally_from_file(filepath)

            # it should not call open(filepath)
            # it should call open(cache_file)
            mock_get_from_cache.assert_called_once_with(cache_file)

            expected: Tally = {
                "foo": 1,
                "bingo": 99,
            }
            assert actual == expected
