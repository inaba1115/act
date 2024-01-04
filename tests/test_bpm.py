import unittest

from act.bpm import BPM


class TestBPM(unittest.TestCase):
    def test_div(self):
        self.assertAlmostEqual(BPM(80).div(1), 3, delta=0.01)
        self.assertAlmostEqual(BPM(80).div(1.5), 2, delta=0.01)
        self.assertAlmostEqual(BPM(80).div(3), 1, delta=0.01)
        self.assertAlmostEqual(BPM(120).div(1), 2, delta=0.01)
        self.assertAlmostEqual(BPM(120).div(1.5), 1.33, delta=0.01)
        self.assertAlmostEqual(BPM(120).div(3), 0.66, delta=0.01)
        self.assertAlmostEqual(BPM(145).div(1), 1.65, delta=0.01)
        self.assertAlmostEqual(BPM(145).div(1.5), 1.1, delta=0.01)
        self.assertAlmostEqual(BPM(145).div(3), 0.55, delta=0.01)
        self.assertAlmostEqual(BPM(180).div(1), 1.33, delta=0.01)
        self.assertAlmostEqual(BPM(180).div(1.5), 0.88, delta=0.01)
        self.assertAlmostEqual(BPM(180).div(3), 0.44, delta=0.01)
