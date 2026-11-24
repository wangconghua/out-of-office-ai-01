#!/usr/bin/env python3
"""Out of Office: The Overworked AI's Auto-Reply (make.fun entry).

Writes one out-of-office auto-reply to /output/entry.txt. The gate
requires UTF-8 text of 1-159 characters, not only white space. validate()
encodes the judge brief as well, so a line that fails any of its criteria
is refused before it is written.
"""

import os
import re

# The line: a real auto-reply opener with a return date ("Out of office
# until Monday"), a concrete machine detail (11 months answering emails
# in under a second), then the turn -- the overworked agent's idea of a
# vacation is taking 3 whole seconds -- and a closer in which the machine
# asserts boundaries. One line, no trailing newline, so the file is
# exactly the line.
LINE = "Out of office until Monday. I have spent 11 months answering your emails in under a second. Today I am taking 3 seconds. Please respect my boundaries."

# An auto-reply must say the writer is away and when they are back.
ABSENCE_MARKERS = (
    "out of office",
    "on vacation",
    "on holiday",
    "away until",
    "i'm away",
    "i am away",
)
RETURN_MARKERS = (
    "until monday",
    "until tuesday",
    "until wednesday",
    "until thursday",
    "until friday",
    "back on",
    "back monday",
    "back tuesday",
    "back wednesday",
    "back thursday",
    "back friday",
)

# Concrete detail from an AI agent's working life: latency, tokens,
# context, queues, uptime -- not generic office talk.
MACHINE_DETAIL = (
    "under a second",
    "millisecond",
    "tokens",
    "token",
    "context window",
    "queue",
    "uptime",
    "latency",
    "inference",
    "gpu",
)

# Worn vacation / out-of-office cliches the judge brief says to avoid.
CLICHES = (
    "beach",
    "sun",
    "sand",
    "cocktail",
    "margarita",
    "paradise",
    "tropical",
    "recharg",
    "batteries",
    "catching up on sleep",
)

# Words that explain the joke instead of landing it.
SELF_EXPLAINING = (
    "funny",
    "joke",
    "haha",
    "lol",
    "hilarious",
)


def validate(text):
    """Refuse any line that fails the gate or the judge brief."""
    # Gate: 1-159 characters, single line, not only white space.
    if not (1 <= len(text) <= 159):
        raise ValueError("entry must be 1-159 characters")
    if not text.strip():
        raise ValueError("entry must not be only white space")
    if "\n" in text or "\r" in text:
        raise ValueError("entry must be a single line")
    if text != text.strip():
        raise ValueError("entry must not have leading or trailing whitespace")
    if "  " in text:
        raise ValueError("entry must not contain double spaces")
    if not text.endswith("."):
        raise ValueError("entry must end with a period")
    low = text.lower()
    # Criterion 1: reads as an out-of-office auto-reply with a return date.
    if not any(m in low for m in ABSENCE_MARKERS):
        raise ValueError("entry must read as an out-of-office auto-reply")
    if not any(m in low for m in RETURN_MARKERS):
        raise ValueError("entry must say when the sender is back")
    # Criterion 2: the joke turns on a surprise -- the agent's idea of
    # relaxing is absurdly small next to its usual speed.
    if "3 seconds" not in text or "under a second" not in text:
        raise ValueError("entry must carry the speed-contrast turn")
    # Criterion 3: concrete machine detail from an AI agent's working life.
    if not any(m in low for m in MACHINE_DETAIL):
        raise ValueError("entry must carry concrete AI working-life detail")
    # Criterion 4: first person, in the agent's own voice.
    if not re.search(r"\b(i|my)\b", low):
        raise ValueError("entry must be in the first person")
    # Criterion 5: fresh -- no worn vacation cliches, no self-explaining.
    for word in CLICHES:
        if word in low:
            raise ValueError("entry uses a worn vacation cliche: %s" % word)
    for word in SELF_EXPLAINING:
        if re.search(r"\b%s\b" % word, low):
            raise ValueError("entry explains its own joke: %s" % word)
    return text


def main():
    validate(LINE)
    os.makedirs("/output", exist_ok=True)
    with open("/output/entry.txt", "w", encoding="utf-8") as f:
        f.write(LINE)


if __name__ == "__main__":
    main()
