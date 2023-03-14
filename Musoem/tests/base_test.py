import unittest
from lib.player.now_playing import NowPlaying
from lib.playables.playable import SoundGroup
from lib.command.command_parser import TextParser
from music.mary_lamb import mary_map

tp = TextParser(mary_map)

class BaseTest(unittest.TestCase):

    def callback(self):
        foo = 1

    def setUp(self):
        NowPlaying.reset()
        NowPlaying.bind_callback(self.callback)
        print("set up")
        self.assertEqual(NowPlaying.playing, [])

    def tearDown(self):
        print("tear down")

    def statement(self, line):
        statement = tp.parse_line(line)
        statement.execute()
        return statement

    def assertIsPlaying(self, section, kw, times):
        self.assertIsNotNone(section)
        self.assertTrue(section in NowPlaying.playing)
        self.assertTrue(section._isplaying)
        self.assertEqual(section._times, times)

    def assertIsNotPlaying(self, kw, section):
        self.assertFalse(section in NowPlaying.playing)
        self.assertFalse(section._isplaying)

    def assertIsScheduled(self, root, kw, times):
        self.assertIsNotNone(root)
        self.assertTrue(root in NowPlaying.playing)

        for s in root:
            if kw == s.keyword:
                self.assertEqual(s._times, times)
                return
        self.fail(kw + "is not scheduled")

    def assertGroupIsPlaying(self, kws, times):
        for p in NowPlaying.playing:
            if isinstance(p, SoundGroup):
                self.assertEqual(kws, list(map(lambda x: x.keyword, p)))
                self.assertEqual(times, p._times)
                if times == None:
                    for x in p:
                        self.assertEqual(x._times, None)


    def assertGroupIsScheduled(self, root, kws, times):
        self.assertIsNotNone(root)
        self.assertTrue(root in NowPlaying.playing)

        for s in root:
            if isinstance(s, SoundGroup) and kws == list(map(lambda x: x.keyword, s)):
                self.assertEqual(s._times, times)
                if times == None:
                    for p in s:
                        self.assertEqual(p._times, None)
                return
        self.fail(kws + " is not scheduled")

    def assertEitherIsPlaying(self, kws, times):
        for p in NowPlaying.playing:
            if p.keyword in kws:
                self.assertEqual(p._times, times)
                return
        self.fail("none of " + kws + "is playing")

    def assertOperationApplied(self, op_kw, section):
        self.assertTrue(op_kw in section.operations)
        self.assertEqual(section.operations[op_kw].section, section)

    def assertOperationNotApplied(self, op_kw, section):
        self.assertFalse(op_kw in section.operations)

    def get_playable(self, kw):
        print("NowPlaying.playing is", NowPlaying.playing)
        for p in NowPlaying.playing:
            if p.keyword == kw:
                return p
            else:
                for n in p:
                    if n.keyword == kw:
                        return n
                    elif isinstance(n, SoundGroup):
                        for k in n:
                            if k.keyword == kw:
                                return k
