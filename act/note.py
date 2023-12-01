from __future__ import annotations

import re
from enum import IntEnum


_NOTE_KIND_MAP = {
    "C": 0,
    "C#": 1,
    "Db": 1,
    "C#/Db": 1,
    "D": 2,
    "D#": 3,
    "Eb": 3,
    "D#/Eb": 3,
    "E": 4,
    "F": 5,
    "F#": 6,
    "Gb": 6,
    "F#/Gb": 6,
    "G": 7,
    "G#": 8,
    "Ab": 8,
    "G#/Ab": 8,
    "A": 9,
    "A#": 10,
    "Bb": 10,
    "A#/Bb": 10,
    "B": 11,
}

_NOTE_KIND_STR_MAP = {
    0: "C",
    1: "C#/Db",
    2: "D",
    3: "D#/Eb",
    4: "E",
    5: "F",
    6: "F#/Gb",
    7: "G",
    8: "G#/Ab",
    9: "A",
    10: "A#/Bb",
    11: "B",
}


class NoteKind(IntEnum):
    C = 0
    CsDb = 1
    D = 2
    DsEb = 3
    E = 4
    F = 5
    FsGb = 6
    G = 7
    GsAb = 8
    A = 9
    AsBb = 10
    B = 11

    @classmethod
    def parse(cls, literal: str) -> NoteKind:
        if literal not in _NOTE_KIND_MAP:
            raise
        return NoteKind(_NOTE_KIND_MAP[literal])

    def __str__(self) -> str:
        return _NOTE_KIND_STR_MAP[self]

    def __repr__(self) -> str:
        return self.__str__()

    def transpose(self, n: int) -> NoteKind:
        return NoteKind((self + n) % 12)

    def inverse(self, n: int) -> NoteKind:
        return NoteKind((n - self) % 12)


_NOTE_RE = re.compile(r"^([\w|#|/|b]+)(\d)$")


class Note:
    def __init__(self, midi_number: int) -> None:
        if midi_number < 0 or 127 < midi_number:
            raise
        self.midi_number = midi_number

    @classmethod
    def parse(cls, literal: str) -> Note:
        m = _NOTE_RE.match(literal)
        if m is None:
            raise
        kind = NoteKind.parse(m.group(1))
        octave = int(m.group(2))
        midi_number = cls._to_midi_number(kind, octave)
        return Note(midi_number)

    @classmethod
    def from_kind_octave(cls, kind: NoteKind, octave: int) -> Note:
        midi_number = cls._to_midi_number(kind, octave)
        return Note(midi_number)

    @classmethod
    def _to_midi_number(cls, kind: NoteKind, octave: int) -> int:
        return kind + (octave + 2) * 12

    def _to_kind_octave(self) -> tuple[NoteKind, int]:
        kind = NoteKind(self.midi_number % 12)
        octave = int(self.midi_number / 12) - 2
        return kind, octave

    def __repr__(self) -> str:
        kind, octave = self._to_kind_octave()
        return f"Note({self.midi_number}, {kind.name}, {octave})"

    def __str__(self) -> str:
        kind, octave = self._to_kind_octave()
        return f"{kind}{octave}"

    def __eq__(self, other: Note) -> bool:
        if not isinstance(other, Note):
            return False
        return self.midi_number == other.midi_number

    def __hash__(self) -> int:
        return hash(self.midi_number)

    def kind(self) -> NoteKind:
        kind, _ = self._to_kind_octave()
        return kind

    def octave(self) -> int:
        _, octave = self._to_kind_octave()
        return octave

    def transpose(self, n: int) -> Note:
        midi_number = self.midi_number + n
        return Note(midi_number)

    def inverse(self, n: int) -> Note:
        midi_number = 2 * n - self.midi_number
        return Note(midi_number)
