import unittest
import os
from FoxDot import P
from lib.score.score_dir import ScoreDir
from lib.playables.sample import Sample, SampleList
from lib.playables.section import Section, SectionList
from lib.playables.playable import SoundGroup
from lib.operations.operations import *
from lib.player.instrument import Instrument
from run_tests import EXAMPLES_PATH

class ScoreDirTests(unittest.TestCase):

    def setUp(self):
        print("set up")

    def tearDown(self):
        print("tear down")

    def test_single_musicxml(self):
        path = EXAMPLES_PATH + "/" + "musicxmlscore"

        score_dir = ScoreDir(path)
        map = score_dir.load()
        mary = map["Mary"]
        self.assertEqual(len(mary._measures), 2)
        self.assertEqual(mary.instrument, Instrument("piano"))
        lamb = map["lamb"]
        self.assertEqual(len(lamb._measures), 2)
        self.assertEqual(lamb.instrument, Instrument("piano"))

    def test_file_score(self):
        path = EXAMPLES_PATH + "/" + "filescore (bpm=80)"

        score_dir = ScoreDir(path)
        map = score_dir.load()
        print("test map", map)

        mary = map["Mary"]
        self.assertEqual(len(mary._measures), 2)
        self.assertEqual(mary.instrument, Instrument("piano"))
        self.assertTrue(isinstance(mary, Section))

        lamb = map["lamb"]
        self.assertEqual(len(lamb._measures), 2)
        self.assertEqual(lamb.instrument, Instrument("piano"))

        cow = map["cow"]
        self.assertEqual(cow.instrument, Instrument("midi 1"))
        self.assertTrue(len(cow._measures) > 0)
        self.assertTrue(isinstance(mary, Section))
        self.assertTrue(80 in cow.bpm)

        afraid = map["afraid"]
        self.assertEqual(afraid.instrument, Instrument("sampler"))
        self.assertTrue(isinstance(afraid, Sample))

        # subscript will pick random value from the list
        # so we use the playables var here to check the type
        self.assertTrue(isinstance(map.playables["best"], SampleList))
        self.assertEqual(map["best"].instrument, Instrument("sampler"))

        self.assertTrue(isinstance(map.playables["snow"], SectionList))
        self.assertEqual(map["snow"].instrument, Instrument("midi 1"))

    def test_config_file(self):
        path = EXAMPLES_PATH + "/" + "score_with_config"
        score_dir = ScoreDir(path)
        map = score_dir.load()

        self.assertTrue("marylamb" in map.playables)
        self.assertTrue("backwards" in map.operations)
        self.assertTrue("retro" in map.operations)

        backwards = map.operations["backwards"]
        marylamb = map.playables["marylamb"]
        self.assertTrue(isinstance(backwards, ReversePitch))
        self.assertTrue(isinstance(marylamb, SoundGroup))
        self.assertEqual(map.playables["Mary"].bpm, P[80, 120])

    def test_convenience_keywords(self):
        path = EXAMPLES_PATH + "/" + "filescore (bpm=80)"
        score_dir = ScoreDir(path)
        map = score_dir.load()
        print("playables in test ", map.playables)
        dog = map["dog"]
        self.assertEqual(dog.degree, 5)
        self.assertEqual(dog.oct, 2)
        self.assertEqual(dog.sus, 2)

        afraid = map["afraid"]
        self.assertEqual(afraid.degree, 5)
        self.assertEqual(afraid.freeze, 1.5)
        self.assertEqual(afraid.comb, 0.7)
