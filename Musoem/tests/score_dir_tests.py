import unittest
import os
from FoxDot import P
from lib.score.score_dir import ScoreDir
from lib.playables.sample import Sample, SampleList
from lib.playables.section import Section
from lib.playables.playable import PlayableGroup
from lib.playables.section_list import SectionList
from lib.operations.operations import *
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
        self.assertEqual(mary.instrument_key, "piano")
        lamb = map["lamb"]
        self.assertEqual(len(lamb._measures), 2)
        self.assertEqual(lamb.instrument_key, "piano")

    def test_file_score(self):
        path = EXAMPLES_PATH + "/" + "filescore (bpm=80)"

        score_dir = ScoreDir(path)
        map = score_dir.load()
        print("test map", map)

        mary = map["Mary"]
        self.assertEqual(len(mary._measures), 2)
        self.assertEqual(mary.instrument_key, "piano")
        self.assertTrue(isinst.ance(mary, Section))

        lamb = map["lamb"]
        self.assertEqual(len(lamb._measures), 2)
        self.assertEqual(lamb.instrument_key, "piano")

        cow = map["cow"]
        self.assertEqual(cow.instrument_key, "midi 1")
        self.assertTrue(len(cow._measures) > 0)
        self.assertTrue(isinstance(mary, Section))
        self.assertTrue(80 in cow.bpm)

        afraid = map["afraid"]
        self.assertEqual(afraid.instrument_key, "vsample")
        self.assertTrue(isinstance(afraid, Sample))

        # subscript will pick random value from the list
        # so we use the playables var here to check the type
        self.assertTrue(isinstance(map.playables["best"], SampleList))
        self.assertEqual(map["best"].instrument_key, "vsample")

        self.assertTrue(isinstance(map.playables["snow"], SectionList))
        self.assertEqual(map["snow"].instrument_key, "midi 1")

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
        self.assertTrue(isinstance(marylamb, PlayableGroup))
        self.assertEqual(map.playables["Mary"].bpm, P[80, 120])

    def test_allp_keyword(self):
        path = EXAMPLES_PATH + "/" + "filescore (bpm=80)"
        score_dir = ScoreDir(path)
        map = score_dir.load()
