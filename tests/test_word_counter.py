from unittest import TestCase
import pytest
from unittest.mock import patch, mock_open
from custom_types import Tally

from word_counter import (
    can_get_from_cache,
    get_cache_filepath,
    get_tally_from_file,
    get_tally_from_file_no_cache,
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


def test_get_tally_from_file_no_cache():
    with patch("word_counter.get_text_from_file") as mock:
        mock.return_value = "foo bar baz bar"
        filepath = "something.txt"
        actual = get_tally_from_file_no_cache(filepath)
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
    actual = get_cache_filepath(filepath)
    assert actual == expected


@pytest.mark.parametrize(
    ["file_exists", "expected"],
    [
        (True, True),
        (False, False),
    ],
)
def test_can_get_from_cache(file_exists, expected):
    with patch("word_counter.exists") as mock_exists:
        mock_exists.return_value = file_exists
        actual = can_get_from_cache("some/sweet.file")
        assert actual == expected


def test_get_tally_from_file():
    with patch("word_counter.can_get_from_cache") as mock_can_get_from_cache:
        mock_can_get_from_cache.return_value = True

        filepath = "i_am/like_a.bird"
        cache_file = get_cache_filepath(filepath)

        with patch("word_counter.should_use_cache") as mock_should_use_cache:
            mock_should_use_cache.return_value = True

            # mock the result pulled from the cache
            with patch("word_counter.get_from_cache") as mock_get_from_cache:
                mock_get_from_cache.return_value = {
                    "foo": 1,
                    "bingo": 99,
                }

                actual = get_tally_from_file(filepath)

                mock_get_from_cache.assert_called_once_with(cache_file)

                expected: Tally = {
                    "foo": 1,
                    "bingo": 99,
                }
                assert actual == expected


def test_when_there_is_no_cache():
    with patch("word_counter.can_get_from_cache") as mock_can_get_from_cache:
        mock_can_get_from_cache.return_value = False

        with patch(
            "word_counter.get_tally_from_file_no_cache"
        ) as mock_get_tally_from_file_no_cache:
            cached_value: Tally = {
                "foo": 1,
                "bingo": 99,
            }
            mock_get_tally_from_file_no_cache.return_value = cached_value

            filepath = "richie.hawtin"
            actual = get_tally_from_file(filepath)

            mock_get_tally_from_file_no_cache.assert_called_once_with(filepath)
            assert actual == cached_value


class TestWhenThereIsCache(TestCase):
    def test_if_it_should_use_the_cache(self):
        with patch("word_counter.can_get_from_cache") as mock_can_get_from_cache:
            mock_can_get_from_cache.return_value = True
            with patch("word_counter.should_use_cache") as mock_should_use_cache:
                with patch("word_counter.get_from_cache") as _mock_get_from_cache:
                    filepath = "richie.hawtin"
                    get_tally_from_file(filepath)
                    mock_should_use_cache.assert_called_once_with(filepath)

    def test_when_it_should_use_the_cache(self):
        with patch("word_counter.can_get_from_cache") as mock_can_get_from_cache:
            mock_can_get_from_cache.return_value = True
            with patch("word_counter.should_use_cache") as mock_should_use_cache:
                mock_should_use_cache.return_value = True
                with patch("word_counter.get_from_cache") as mock_get_from_cache:
                    cached_value: Tally = {"foo": 99}
                    mock_get_from_cache.return_value = cached_value
                    filepath = "umek"
                    actual = get_tally_from_file(filepath)
                    assert actual == cached_value

    def test_when_it_should_not_use_the_cache(self):
        with patch("word_counter.can_get_from_cache") as mock_can_get_from_cache:
            mock_can_get_from_cache.return_value = True
            with patch("word_counter.should_use_cache") as mock_should_use_cache:
                mock_should_use_cache.return_value = False
                with patch(
                    "word_counter.get_tally_from_file_no_cache"
                ) as mock_get_tally_from_file_no_cache:
                    tally: Tally = {"bloop": 33}
                    mock_get_tally_from_file_no_cache.return_value = tally
                    filepath = "charlie.cheese"
                    actual = get_tally_from_file(filepath)
                    assert actual == tally
