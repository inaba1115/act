import unittest

from act.mode import Mode
from act.note import NoteKind, Note


class TestMode(unittest.TestCase):
    def test_parse(self):
        m = Mode.parse("C Minor")
        self.assertEqual(m._root, NoteKind.parse("C"))
        self.assertEqual(m._scale, [0, 2, 3, 5, 7, 8, 10])
        self.assertEqual(
            m._scale_note_kind,
            [
                NoteKind.parse("C"),
                NoteKind.parse("D"),
                NoteKind.parse("Eb"),
                NoteKind.parse("F"),
                NoteKind.parse("G"),
                NoteKind.parse("Ab"),
                NoteKind.parse("Bb"),
            ],
        )

    def test_nth_note(self):
        m = Mode.parse("C Minor")
        self.assertEqual(m.nth_note(3, 0), Note.parse("C3"))
        self.assertEqual(m.nth_note(3, 1), Note.parse("D3"))
        self.assertEqual(m.nth_note(3, 7), Note.parse("C4"))
        self.assertEqual(m.nth_note(3, 8), Note.parse("D4"))
        self.assertEqual(m.nth_note(3, -1), Note.parse("Bb2"))
        self.assertEqual(m.nth_note(3, -7), Note.parse("C2"))
        self.assertEqual(m.nth_note(3, -8), Note.parse("Bb1"))

    def test_nth_notes(self):
        m = Mode.parse("C Minor")
        self.assertEqual(m.nth_notes(3, [0, 1]), [Note.parse("C3"), Note.parse("D3")])

    def test_range_notes(self):
        m = Mode.parse("C Minor")
        self.assertEqual(m.range_notes(3, -1, 1), [Note.parse("Bb2"), Note.parse("C3"), Note.parse("D3")])

    def test_choices_notes(self):
        m = Mode.parse("C Minor")
        self.assertEqual(len(m.choices_notes(3, -1, 1, 1)), 1)

    def test_sample_notes(self):
        m = Mode.parse("C Minor")
        self.assertEqual(len(m.sample_notes(3, -1, 1, 1)), 1)
