from __future__ import annotations

import random

from act.note import NoteKind, Note


SCALES = {
    "8-Tone Spanish": [0, 1, 3, 4, 5, 6, 8, 10],
    "Bhairav": [0, 1, 4, 5, 7, 8, 11],
    "Chromatic": [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11],
    "Dorian #4": [0, 2, 3, 6, 7, 9, 10],
    "Dorian Mode": [0, 2, 3, 5, 7, 9, 10],
    "Half-Whole Diminished": [0, 1, 3, 4, 6, 7, 9, 10],
    "Hirajoshi": [0, 2, 3, 7, 8],
    "Insen": [0, 1, 5, 7, 10],
    "Iwao": [0, 1, 5, 6, 10],
    "Kumoi": [0, 2, 3, 7, 9],
    "Locrian Mode": [0, 1, 3, 5, 6, 8, 10],
    "Locrian Super": [0, 1, 3, 4, 6, 8, 10],
    "Lydian Augmented": [0, 2, 4, 6, 8, 9, 11],
    "Lydian Dominant": [0, 2, 4, 6, 7, 9, 10],
    "Lydian Mode": [0, 2, 4, 6, 7, 9, 11],
    "Major Harmonic": [0, 2, 4, 5, 7, 8, 11],
    "Major Pentatonic": [0, 2, 4, 7, 9],
    "Major": [0, 2, 4, 5, 7, 9, 11],
    "Messiaen 3": [0, 2, 3, 4, 6, 7, 8, 10, 11],
    "Messiaen 4": [0, 1, 2, 5, 6, 7, 8, 11],
    "Messiaen 5": [0, 1, 5, 6, 7, 11],
    "Messiaen 6": [0, 2, 4, 5, 6, 8, 10, 11],
    "Messiaen 7": [0, 1, 2, 3, 5, 6, 7, 8, 9, 11],
    "Minor Blues": [0, 3, 5, 6, 7, 10],
    "Minor Harmonic": [0, 2, 3, 5, 7, 8, 11],
    "Minor Hungarian": [0, 2, 3, 6, 7, 8, 11],
    "Minor Melodic Down": [0, 2, 3, 5, 7, 8, 10],
    "Minor Melodic Up": [0, 2, 3, 5, 7, 9, 11],
    "Minor Pentatonic": [0, 3, 5, 7, 10],
    "Minor": [0, 2, 3, 5, 7, 8, 10],
    "Mixolydian Mode": [0, 2, 4, 5, 7, 9, 10],
    "Pelog Selisir": [0, 1, 3, 7, 8],
    "Pelog Tembung": [0, 1, 5, 7, 8],
    "Phrygian Dominant": [0, 1, 4, 5, 7, 8, 10],
    "Phrygian Mode": [0, 1, 3, 5, 7, 8, 10],
    "Whole Tone": [0, 2, 4, 6, 8, 10],
    "Whole-Half Diminished": [0, 2, 3, 5, 6, 8, 9, 11],
}


class Mode:
    def __init__(self, root: NoteKind, scale: list[int], literal: str = "") -> None:
        self._root = root
        self._scale = scale
        self._scale_note_kind = [root.transpose(i) for i in scale]
        self._literal = literal

    def __repr__(self) -> str:
        class_name = type(self).__name__
        return f"{class_name}(root={self._root!r}, scale={self._scale!r}, literal={self._literal!r})"

    def __str__(self) -> str:
        return self._literal if self._literal != "" else repr(self)

    @classmethod
    def parse(cls, literal: str) -> Mode:
        xs = literal.split(" ")
        root = NoteKind.parse(xs[0])
        scale = SCALES[" ".join(xs[1:])]
        return Mode(root, scale, literal)

    def scale_note_kind(self) -> list[NoteKind]:
        return self._scale_note_kind

    def literal(self) -> str:
        return self._literal

    def nth_note(self, octave: int, nth: int) -> Note:
        octave += nth // len(self._scale)
        nth = nth % len(self._scale)
        note = Note.from_kind_octave(self._root, octave).transpose(self._scale[nth])
        return note

    def nth_notes(self, octave: int, nths: list[int]) -> list[Note]:
        return [self.nth_note(octave, nth) for nth in nths]

    def range_notes(self, octave: int, low_nth: int, high_nth: int) -> list[Note]:
        nths = list(range(low_nth, high_nth + 1))
        return self.nth_notes(octave, nths)

    def choices_notes(self, octave: int, low_nth: int, high_nth: int, k: int) -> list[Note]:
        nths = random.choices(list(range(low_nth, high_nth + 1)), k=k)
        return self.nth_notes(octave, nths)

    def sample_notes(self, octave: int, low_nth: int, high_nth: int, k: int) -> list[Note]:
        nths = random.sample(list(range(low_nth, high_nth + 1)), k=k)
        return self.nth_notes(octave, nths)

    def similarity(self, other: Mode) -> float:
        a = set(self.scale_note_kind())
        b = set(other.scale_note_kind())
        return len(a & b) / len(a | b)

    def similar_modes(self, threshold_low: float = 0.0, threshold_high: float = 1.0) -> list[tuple[float, Mode]]:
        ret = []
        for root in NoteKind:
            for scale_name, _ in SCALES.items():
                other = Mode.parse(f"{root} {scale_name}")
                similarity = self.similarity(other)
                if threshold_low <= similarity <= threshold_high:
                    ret.append((similarity, other))
        return sorted(ret, key=lambda x: x[0], reverse=True)
