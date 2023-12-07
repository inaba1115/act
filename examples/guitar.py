from __future__ import annotations

from termcolor import colored

from act.mode import Mode
from act.note import NoteKind


TUNING = [
    NoteKind.parse("E"),
    NoteKind.parse("B"),
    NoteKind.parse("G"),
    NoteKind.parse("D"),
    NoteKind.parse("A"),
    NoteKind.parse("E"),
]
FRETS = 12
TAB_WIDTH = 6


def print_guitar(root: NoteKind, intervals: list[int]) -> None:
    notes = Mode(root, intervals).scale_note_kind()
    for open_string in TUNING:
        for fret in range(FRETS + 1):
            note = open_string.transpose(fret)
            if note is root:
                s = colored(str(note).ljust(TAB_WIDTH), "light_cyan", attrs=["reverse"])
            elif note in notes:
                s = colored(str(note).ljust(TAB_WIDTH), "light_blue", attrs=["reverse"])
            else:
                s = str(fret).ljust(TAB_WIDTH)
            print(f"|{s}", end="")
        print("|")


def main():
    root = NoteKind.parse("A")
    intervals = [0, 2, 3, 5, 7, 8, 10]
    print_guitar(root, intervals)


if __name__ == "__main__":
    main()
