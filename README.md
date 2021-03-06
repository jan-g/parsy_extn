# Some small extensions to parsy

This offers a small extension to the behaviour of Parsy.

## Note-keeping

Input streams gain the ability to keep notes. These are additional information
associated with a particular index in the stream. As the parsing process proceeds,
new notes may be written. An attempt to fetch the most recent set of notes can be performed
by:

    recent_notes = yield parsy_extn.get_notes

and notes at the current point in parsing may be written by

    yield put_notes(new_notes)
    
As the parser backtracks, older sets of notes may be thrown away.

### Notes on the mutability of notes

Notes are kept in a dictionary. `get_notes` performs a shallow copy of this dictionary;
however, references to embedded objects are identical.

This is intentional; the utility of notes is in allowing a parser to back-fill
already-generated placeholder values with actual content.

However, care should be taken when writing new sets of notes that references to other
mutable objects (such as lists) are not duplicated accidentally; this will result in
the backtracking process losing the immutability of previous notes.

## Handling augmentation

### Manually augmenting the stream

An input `str` or `list` may be augmented before being passed to a parser. This should
be done at the initial point of ingestion into the grammar:

    result = grammar_entry_point.parse(parsy_extn.Noted.augment(original_input))

### Wrapping a single entry-point's `parse` method

Alternatively, a grammar's entry-point may be decorated to automatically wrap values as
they are passed to the `parse` method:

    grammar_entry_point = parsy_ext.keeps_notes(grammar_entry_point)
    result = grammar_entry_point.parse(original_input)

### Monkey-patching `parsy.Parser`

Finally, the `parsy.Parser` object itself may be monkey-patched to wrap any input on
entry to `parse` or `parse_partial`:

    parsy_extn.monkeypatch_parsy()
    result = grammar_entry_point.parse(original_input)

## Motivation

The motivation for this is to handle constructs like shell 'heredocs' with a single
pass of a parser. They are otherwise notoriously difficult to handle; even with
this facility, the resulting grammars are fiddly.

A trivial example is given in the `test_parsy_extn` module.
