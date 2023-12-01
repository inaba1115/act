from __future__ import annotations

from act.mode import Mode
from act.note import NoteKind
from termcolor import colored


TUNING = {
    1: NoteKind.parse("E"),
    2: NoteKind.parse("B"),
    3: NoteKind.parse("G"),
    4: NoteKind.parse("D"),
    5: NoteKind.parse("A"),
    6: NoteKind.parse("E"),
}
FRETS = 12
TAB_WIDTH = 6


def print_guitar(root: NoteKind, intervals: list[int]) -> None:
    notes = Mode(root, intervals)._scale_note_kind
    for string in range(1, 7):
        open_string = TUNING[string]
        for fret in range(FRETS + 1):
            note = open_string.transpose(fret)
            if note is root:
                s = colored(str(note).ljust(TAB_WIDTH), "light_cyan", attrs=["reverse"])
            elif note in notes:
                s = colored(str(note).ljust(TAB_WIDTH), "light_blue", attrs=["reverse"])
            else:
                s = str(fret).ljust(TAB_WIDTH)
            print("|{}".format(s), end="")
        print("|")


def main():
    root = NoteKind.parse("A")
    intervals = [0, 2, 3, 5, 7, 8, 10]
    print_guitar(root, intervals)


if __name__ == "__main__":
    main()
