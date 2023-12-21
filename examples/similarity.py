from __future__ import annotations

from act.mode import Mode
from act.note import NoteKind


def main():
    m = Mode(NoteKind.parse("C"), [0, 4, 7])
    print(m)
    for x, y in m.similar_modes(0.4):
        print(f"{x}\t{y}")


if __name__ == "__main__":
    main()
