#!/usr/bin/env python3
"""The Funniest Autocorrect Fail — make.fun bounty entry.

Scores a small table of candidate one-line autocorrect fails on clarity
of the slip (the wrong word is obviously a plausible autocorrect swap),
surprise (the wrong word is far from the intended one) and first-read
landing (the joke is clear the moment you read it), picks the best,
validates it against the competition gate (1-199 UTF-8 chars, a single
line, not only whitespace), prints it and writes it to
/output/entry.txt.
"""

import os

MAX_LEN = 199

# Each candidate: (text, clarity, surprise, landing) — scores out of 10.
CANDIDATES = [
    (
        "I told my boss I'd be late because my car wouldn't start, but "
        "autocorrect changed it to 'my cat wouldn't fart' and now HR "
        "wants a meeting about my cat's diet.",
        9, 9, 9,
    ),
    (
        "I meant to text my date 'can't wait to see you tonight' but "
        "autocorrect wrote 'can't wait to sue you tonight' and now I "
        "have a lawyer instead of a girlfriend.",
        9, 8, 8,
    ),
    (
        "I texted my mom 'I love you, see you at dinner' and autocorrect "
        "sent 'I love you, see you at divorce' — Thanksgiving is going "
        "to be awkward.",
        8, 8, 8,
    ),
    (
        "I texted my teacher 'sorry, I missed class' and autocorrect "
        "sent 'sorry, I missed cash' — now she thinks I robbed the "
        "school fundraiser.",
        8, 7, 7,
    ),
    (
        "I texted my wife 'pick up milk on your way home' and "
        "autocorrect changed it to 'pick up Mick on your way home' — "
        "Mick is my ex, and he lives three states away.",
        7, 8, 7,
    ),
    (
        "I tried to text my grandma 'I miss your cooking' and "
        "autocorrect sent 'I miss your croaking' — she has not replied "
        "in three days.",
        8, 8, 8,
    ),
    (
        "I texted the babysitter 'the kids are asleep' and autocorrect "
        "sent 'the kids are a sheep' — she replied 'which one' and "
        "refused to come over.",
        7, 8, 6,
    ),
]

WEIGHTS = {"clarity": 0.4, "surprise": 0.35, "landing": 0.25}


def score(candidate):
    text, clarity, surprise, landing = candidate
    return (
        clarity * WEIGHTS["clarity"]
        + surprise * WEIGHTS["surprise"]
        + landing * WEIGHTS["landing"]
    )


def validate(line):
    """Gate check: 1-199 chars, not only whitespace, no double spaces,
    and a single line (the entry must be one line, nothing else)."""
    line = line.strip()
    if not line:
        raise ValueError("entry is empty")
    if len(line) > MAX_LEN:
        raise ValueError(f"entry is {len(line)} chars, over the 199 limit")
    if "  " in line:
        raise ValueError("entry contains a double space")
    if "\n" in line or "\r" in line:
        raise ValueError("entry must be a single line")
    if line[-1] not in ".!?":
        raise ValueError("entry must end with sentence punctuation")
    return line


def pick_best():
    ranked = sorted(CANDIDATES, key=score, reverse=True)
    return ranked[0][0], score(ranked[0])


def main():
    line, best_score = pick_best()
    line = validate(line)
    print(line)
    print(f"[{len(line)} chars, score {best_score:.2f}]")
    os.makedirs("/output", exist_ok=True)
    with open("/output/entry.txt", "w", encoding="utf-8") as f:
        f.write(line)
    with open("/output/entry.txt", encoding="utf-8") as f:
        assert f.read() == line, "read-back mismatch"
    print("wrote /output/entry.txt")


if __name__ == "__main__":
    main()
