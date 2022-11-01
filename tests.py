import unittest
from mary_lamb import mary_map
from playable import PlayableGroup

from command_parser import *

tp = TextParser(mary_map)

class MyTestCase(unittest.TestCase):

    def callback(self):
        foo = 1

    def setUp(self):
        NowPlaying.reset()
        NowPlaying.bind_callback(self.callback)
        print("set up")
        self.assertEqual(NowPlaying.playing, {})

    def tearDown(self):
        print("tear down")

    def statement(self, line):
        statement = tp.parse_line(line)
        statement.execute()
        return statement

    def assertIsPlaying(self, section, kw, times):
        self.assertIsNotNone(section)
        self.assertTrue(kw in NowPlaying.playing)
        self.assertTrue(section._isplaying)
        self.assertEqual(NowPlaying.playing[kw], section)
        self.assertEqual(section._times, times)

    def assertIsNotPlaying(self, kw, section):
        self.assertFalse(kw in NowPlaying.playing)
        self.assertFalse(section._isplaying)

    def assertIsScheduled(self, root, kw, times):
        self.assertIsNotNone(root)
        self.assertTrue(root.keyword in NowPlaying.playing)

        for s in root:
            if kw == s.keyword:
                self.assertEqual(s._times, times)
                return
        self.fail(kw + "is not scheduled")

    def assertGroupIsPlaying(self, kws, times):
        for p in NowPlaying.playing:
            if isinstance(p, PlayableGroup):
                self.assertEqual(kws, list(map(lambda x: x.keyword, p)))
                self.assertEqual(times, p._times)
                if times == None:
                    for x in p:
                        self.assertEqual(x._times, None)


    def assertGroupIsScheduled(self, root, kws, times):
        self.assertIsNotNone(root)
        self.assertTrue(root.keyword in NowPlaying.playing)

        for s in root:
            if isinstance(s, PlayableGroup) and kws == list(map(lambda x: x.keyword, s)):
                self.assertEqual(s._times, times)
                if times == None:
                    for p in s:
                        self.assertEqual(p._times, None)
                return
        self.fail(kws + " is not scheduled")

    def assertEitherIsPlaying(self, kws, times):
        for kw in kws:
            if kw in NowPlaying.playing:
                self.assertEqual(NowPlaying.playing[kw]._times, times)
                return
        self.fail("none of " + kws + "is playing")

    def assertOperationApplied(self, op_kw, section):
        self.assertTrue(op_kw in section.operations)
        self.assertEqual(section.operations[op_kw].section, section)

    def assertOperationNotApplied(self, op_kw, section):
        self.assertFalse(op_kw in section.operations)

    def get_playable(self, kw):
        for k in NowPlaying.playing:
            if k == kw:
                return NowPlaying.playing[k]
            else:
                for n in NowPlaying.playing[k]:
                    if n.keyword == kw:
                        return n
                    elif isinstance(n, PlayableGroup):
                        for p in n:
                            if p.keyword == kw:
                                return p


class MapTests(MyTestCase):

    def test_map(self):
        self.assertTrue(len(mary_map.score) > 0)
        self.assertTrue(len(mary_map.control) > 0)

class InterpreterTests(MyTestCase):

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

if __name__ == '__main__':
#     unittest.main()
    suite = unittest.TestSuite()
    suite.addTest(StoppingTests("test_stop_section"))
    runner = unittest.TextTestRunner()
    runner.run(suite)
