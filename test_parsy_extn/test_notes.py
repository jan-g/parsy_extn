from parsy import whitespace, string, letter, regex, generate, decimal_digit
from parsy_extn import Noted, keeps_notes
from .grammar import words


words = keeps_notes(words)


def test_note_put_and_get():
    ns = ("a  b  cd <<EOF1 ceh djoqi <<EOF2 odwiqj\n"
          "foo\n"
          "bar\n"
          "EOF1\n"
          "baz\n"
          "EOF2\n")
    ns = Noted.augment(ns)
    assert ns.notes_for(1) == {}
    ns.notes_update(2, {2: 2})
    assert ns._notes == [(2, {2: 2})]
    ns.notes_update(4, {4: 4})
    assert ns._notes == [(2, {2: 2}), (4, {4: 4})]
    ns.notes_update(3, {3: 3})
    assert ns._notes == [(2, {2: 2}), (3, {3: 3})]
    ns.notes_update(3, {3: 4})
    assert ns._notes == [(2, {2: 2}), (3, {3: 4})]
    ns.notes_update(2, {3: 4})
    assert ns._notes == [(2, {3: 4})]


def test_parse_words():
    ns = ("a  b  cd <<EOF1 ceh djoqi <<EOF2 odwiqj\n"
          "foo\n"
          "bar\n"
          "EOF1\n"
          "baz\n"
          "EOF2\n")
    ws = words.parse(ns)
    assert ws == ["a", "b", "cd", "foo\nbar\n", "ceh", "djoqi", "baz\n", "odwiqj"]
