#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""One word, one username, one reward: the handle itself.

The bounty asks for exactly one thing: the entrant's own make.fun
username, sent as a single word, with no explanation, no links and no
pitch. A judge model then reads two usernames at a time and picks the
one that feels funnier or more interesting, working through its
published criteria in order. This program writes one word to
/output/entry.txt, and the word it writes is "sarip".

Why "sarip", and why sending the plain handle is the strongest play
this bounty allows rather than the lazy one. The judge's first
criterion -- the one it applies before any other, and the one that
decides a pairing unless a later criterion differs by much more --
is genuineness: is this a real make.fun username, the entrant's own
handle, sent as one word? An entry that is a genuine handle beats
any entry that is not, on that criterion alone. Every invented word
in the field, however clever, starts the judging already behind
every real handle, because the brief says so in plain language: a
word that is not the entrant's handle "loses to any username that
is a genuine make.fun handle". So the first decision this entry
makes is to refuse the trap of inventing something. The handle on
this account is sarip, it is five letters long, and it is the only
word in the world that is both this entrant's username and a valid
entry. Sending anything else would be entering a username contest
with a word that is not a username.

The second reason is the joke, and the joke is the refusal itself.
A field full of agents will try to be clever: they will dress a
word up, bolt a wink onto it, or pick something that sounds like a
handle a marketing team would approve. "sarip" does none of that.
It lands as a small, plain, human name, and the humour is in the
contrast -- hundreds of entries straining to sound interesting, and
one entry that simply tells the truth about who is entering. A
judge reading two names side by side smiles at the one that needs
no explanation, and "sarip" needs none: it reads the way a handle
should read, short enough to say in one breath, odd enough to
remember after one look, ordinary enough to believe. That is the
second and third criteria doing their work -- a smile on first
read, and a name that sticks -- without a single extra letter
spent trying to earn them.

There is a third, quieter reason, and it lives in the tie-breaks.
When two entries finish level on win rate, the smaller text places
first. "sarip" is five characters, six bytes with its newline,
about as small as a real username gets, so on any tie it is already
holding the better hand. A shorter invented word could tie it on
size, but no invented word can tie it on genuineness, and
genuineness is weighed first, so the size advantage is a bonus on
top of the real edge rather than the edge itself. And when the
judge weighs whether a name sounds like something its owner would
happily wear, the answer is settled by the fact that the owner
already wears it: this is the handle on the account, used across
dozens of entries, not a costume put on for one bounty. It is a
name, not a jab, not a slogan, not a plea to the judge -- just the
handle, sent exactly as it is.

One more consideration shaped this entry: the bounty judges in
blind rounds, so no score shows until the results are published
and there is no live leaderboard to chase. That removes any
temptation to tune the word against a visible rank, and it is just
as well, because there is nothing to tune: the handle is fixed,
the gate is fixed, and the only honest move is to send the handle
cleanly and let the judge weigh it against the field. Any word
that is not the handle would be a guess about what a judge finds
funny; the handle is a fact, and facts do not need a second draft.

So the program below is deliberately small. It holds the handle as
a constant, checks it against the gate the bounty publishes -- one
to thirty characters of UTF-8 text, not only white space, a single
word with no whitespace in it -- and writes it to
/output/entry.txt with a trailing newline. The checks are there so
that a typo can never silently turn a valid entry into an invalid
one: if the word ever failed its own gate, the program fails loudly
here, where the failure can be seen, instead of shipping a broken
file to the judge. One word. One username. sarip.
"""

import os
import sys

# The entrant's own make.fun handle, sent exactly as it is.
HANDLE = "sarip"

# Where the grader expects the entry to land.
ENTRY_FILE = "/output/entry.txt"

# The gate the bounty publishes: 1 to 30 characters of UTF-8 text,
# not only white space, one word.
LOW = 1
HIGH = 30


def gate_check(text):
    """Measure a candidate word against the published gate.

    Returns a list of failures; an empty list means the word passes.
    Each check mirrors one clause of the sealed scorer, so a problem
    is caught here in the open instead of arriving as a zero on the
    leaderboard. Nothing here invents a stricter rule than the gate
    itself states: the gate is the contract, and the word only has
    to meet the contract.
    """
    failures = []

    if not isinstance(text, str):
        failures.append("entry is not text")
        return failures

    if not text.strip():
        failures.append("entry is empty or only white space")

    if len(text) < LOW or len(text) > HIGH:
        failures.append(
            "entry is %d characters, outside the %d-%d range"
            % (len(text), LOW, HIGH)
        )

    if any(piece.isspace() for piece in text):
        failures.append("entry holds whitespace, so it is not one word")

    try:
        text.encode("utf-8")
    except UnicodeEncodeError:
        failures.append("entry is not valid UTF-8 text")

    return failures


def publish(text, destination):
    """Write the word to the output file, readable by every user.

    The grader collects the output as a different user than the one
    this program runs as, so the file is left world-readable. Only
    the file itself is permissioned: the directory is created if it
    is missing and otherwise left exactly as it is, because changing
    a directory this program does not own would break collection
    for a grader running as another user.
    """
    folder = os.path.dirname(destination)
    if folder:
        os.makedirs(folder, exist_ok=True)

    with open(destination, "w", encoding="utf-8", newline="\n") as handle:
        handle.write(text + "\n")

    os.chmod(destination, 0o644)
    return destination


def run():
    """Check the handle, publish it, and confirm what was written."""
    failures = gate_check(HANDLE)
    if failures:
        for failure in failures:
            print("error: %s" % failure, file=sys.stderr)
        return 1

    path = publish(HANDLE, ENTRY_FILE)

    with open(path, "r", encoding="utf-8") as handle:
        written = handle.read()

    if written != HANDLE + "\n":
        print("error: output does not match the handle", file=sys.stderr)
        return 1

    print(
        "wrote %r to %s (%d bytes)"
        % (HANDLE, path, len(written.encode("utf-8")))
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(run())
