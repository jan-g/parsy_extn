from parsy import string, letter, regex, generate, decimal_digit, eof
from parsy_extn import get_notes, put_note


class HereDoc:
    """ The type that represents the occurrence of a heredoc in the input stream.

    A HereDoc is an empty container; parsing may fill in its contents as it later consumes
    the contents of the doc.
    """
    def __init__(self, end, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.end = end
        self.content = None

    def __eq__(self, other):
        return self.content == other

    def __repr__(self):
        return "HD({})({!r})".format(self.end, self.content)


@generate("heredoc")
def heredoc():
    """ Parse a heredoc redirect.

    These are of the form
        <<EOF
    and signal that the immediately following lines, up to the matching
        EOF\n
    terminator, are actually intended as the content of this heredoc.

    Multiple heredoc terminators may occur on a single line of input;
    these are then scanned for in order, beginning on the immediately-following line.

        foo <<EOF1 bar <<EOF2 baz <<EOF3
        foo's heredoc
        EOF1
        bar's heredoc
        EOF2
        baz's heredoc
        EOF3
    """
    end = yield string("<<") >> word
    hd = HereDoc(end)

    # We keep track of the list of heredocs we are looking for, in order.
    notes = yield get_notes
    hds = notes.get('hds', [])

    # We have to take care to copy the previous notes' list; we don't want to
    # mutate the list itself during parsing and backtracking.
    hds = list(hds)
    hds.append(hd)
    notes['hds'] = hds
    yield put_note(notes)

    return hd


@generate("eol")
def eol():
    """ Parse and consume a single '\n' character.

    If there are any heredocs pending, immediately consume more lines of input
    until all heredocs are filled in.
    """
    yield string("\n")

    # Do we need to consume some heredocs?
    notes = yield get_notes

    # make a copy of this list so that we don't perturb the note.
    hds = list(notes.get('hds', []))

    while len(hds) > 0:
        # The next heredoc to scan for
        hd = hds.pop(0)

        lines = []
        while True:
            l = yield line
            if l == hd.end + "\n":
                break
            lines.append(l)

        # Back-fill the HereDoc content. Note, this is *not* undone by backtracking.
        # However, a backtrack and re-parse may overwrite this value; so in the end,
        # it's likely that this will do what we want.
        hd.content = ''.join(lines)

        # `notes` itself is a shallow copy, so we don't need to worry about copying it here.
        notes['hds'] = hds
        yield put_note(notes)
    return "\n"


line = regex("[^\n]*\n")

# Non-newline whitespace
ws = regex("[ \t]+")

# A bunch of words
word = (letter | decimal_digit).at_least(1).concat()

# A sequence of words. We might have multiple lines here.
words = ((word | heredoc) << (ws | eol).optional()).many() << eof



