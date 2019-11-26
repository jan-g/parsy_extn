from parsy import whitespace, string, letter, regex, generate, decimal_digit
from parsy_extn import monkeypatch_parsy
from .grammar import words


def test_parse_words():
    undo = monkeypatch_parsy()
    try:
        ns = ("a  b  cd <<EOF1\n"
              "foo\n"
              "bar\n"
              "EOF1\n"
              "ceh\ndjoqi <<EOF2 odwiqj\n"
              "baz\n"
              "EOF2\n")
        ws = words.parse(ns)
        assert ws == ["a", "b", "cd", "foo\nbar\n", "ceh", "djoqi", "baz\n", "odwiqj"]
    finally:
        undo()
