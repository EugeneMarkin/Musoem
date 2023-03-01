import unittest

from music.mary_lamb import mary_map
from tests.base_test import BaseTest

class MapTests(BaseTest):

    def test_map(self):
        self.assertTrue(len(mary_map.score) > 0)
        self.assertTrue(len(mary_map.control) > 0)

class InterpreterTests(BaseTest):

    def test_solo_section(self):
        st = self.statement("Mary")
        self.assertIsPlaying(st.top_playable, "Mary", None)

    def test_period(self):
        st = self.statement("Mary.")
        self.assertIsPlaying(st.top_playable, "Mary", 1)

    def test_exclamation(self):
        st = self.statement("Mary!")
        self.assertIsPlaying(st.top_playable, "Mary", 1)
        self.assertIsPlaying(st.top_control, "!", 1)

    def test_question(self):
        st = self.statement("Mary?")
        self.assertIsPlaying(st.top_playable, "Mary", 1)
        self.assertIsPlaying(st.top_control, "?", 1)

    def test_solo_control(self):
        st = self.statement("Rise")
        self.assertIsPlaying(st.top_playable, "Rise", None)

    def test_spaced_seq(self):
        st = self.statement("Mary had a little lamb")
        self.assertIsPlaying(st.top_playable, "Mary", 1)
        for s in ["had", "little"]:
            self.assertIsScheduled(st.top_playable, s, 1)
        self.assertIsScheduled(st.top_playable, "lamb", None)

    def test_and(self):
        st = self.statement("Mary had little and lamb")
        self.assertIsPlaying(st.top_playable, "Mary", 1)
        self.assertIsScheduled(st.top_playable, "had", 1)
        self.assertGroupIsScheduled(st.top_playable, ["little", "lamb"], None)

    def test_and_playing(self):
        st = self.statement("Mary and lamb")
        self.assertGroupIsPlaying(["Mary", "lamb"], None)

    def test_or(self):
        st = self.statement("Mary or lamb.")
        self.assertEitherIsPlaying(["Mary", "lamb"], 1)

    def test_operation1(self):
        st = self.statement("Mary reverse lamb")
        section = self.get_playable("Mary")
        self.assertIsPlaying(st.top_playable, "Mary", 1)
        self.assertIsScheduled(st.top_playable, "lamb", None)
        self.assertOperationApplied("reverse", section)
        self.assertOperationNotApplied("reverse", self.get_playable("lamb"))

    def test_operation2(self):
        st = self.statement("reverse Mary and lamb")
        self.assertGroupIsPlaying(["Mary", "lamb"], None)
        self.assertOperationApplied("reverse", self.get_playable("Mary"),)
        self.assertOperationApplied("reverse", self.get_playable("lamb"))

    def test_solo_operation(self):
        st1 = self.statement("Mary lamb")
        st2 = self.statement("had")
        self.assertIsPlaying(st1.top_playable, "Mary", 1)
        self.assertIsPlaying(st2.top_playable, "had", None)
        self.assertIsScheduled(st1.top_playable, "lamb", None)

        st3 = self.statement("reverse")
        self.assertOperationApplied("reverse", st1.top_playable)
        self.assertOperationApplied("reverse", st2.top_playable)
        self.assertOperationNotApplied("reverse", self.get_playable("lamb"))

    def test_comma(self):
        st = self.statement("Mary, lamb!")
        self.assertIsPlaying(st.top_playable, "Mary", 1)
        self.assertIsScheduled(st.top_playable, "lamb", 1)
        print("now ", NowPlaying.playing)

    def test_complex_statement(self):
        st = self.statement("Mary or lamb reverse Rise had and a little reverse and lamb and Rise had or little, Mary, lamb and Mary!")

        self.assertEitherIsPlaying(["Mary", "lamb"], 1)
        self.assertIsPlaying(st.top_control, "!", 1)
        self.assertGroupIsScheduled(st.top_playable, ["had", "little"], 1)
        self.assertGroupIsScheduled(st.top_playable, ["lamb", "Rise"], 1)
        self.assertOperationApplied("reverse", self.get_playable("lamb"))
        self.assertOperationApplied("reverse", st.top_playable)
        self.assertIsScheduled(st.top_playable, "Mary", 1)

    def test_semicolon(self):
        st1 = self.statement("Mary.")
        st2 = self.statement("cow.")
        st3 = self.statement("had;")
        self.assertIsPlaying(st1.top_playable, "Mary", 1)
        self.assertIsPlaying(st2.top_playable, "cow", 1)
        self.assertIsScheduled(st1.top_playable, "had", 1)

class StoppingTests(InterpreterTests):

    def test_stop_section(self):
        st1 = self.statement("Mary had a little")
        self.assertIsPlaying(st1.top_playable, "Mary", 1)
        print("one" , NowPlaying.display())
        NowPlaying.stop("Mary")
        self.assertIsNotPlaying("Mary", st1.top_playable)
        print(NowPlaying.display())
