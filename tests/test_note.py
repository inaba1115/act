import unittest

from act.note import NoteKind, Note


class TestNoteKind(unittest.TestCase):
    def test_parse(self):
        self.assertEqual(NoteKind.parse("C"), 0)

    def test_str(self):
        self.assertEqual("{}".format(NoteKind.parse("C")), "C")


class TestNote(unittest.TestCase):
    def test_parse(self):
        self.assertEqual(Note.parse("C3").midi_number, 60)

    def test_str(self):
        self.assertEqual("{}".format(Note.parse("C3")), "C3")
        self.assertEqual("{}".format(Note.parse("C#3")), "C#/Db3")
