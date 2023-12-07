from __future__ import annotations

from act.mode import Mode
from act.note import NoteKind


def main():
    m = Mode(NoteKind.parse("C"), [0, 4, 7])
    print(m)
    m.print_similar_modes(0.4)


if __name__ == "__main__":
    main()
