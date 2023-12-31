from tests.command_parsing_tests import *
from tests.score_dir_tests import *


def loadAll(cls):
    return unittest.defaultTestLoader.loadTestsFromTestCase(cls)

if __name__ == '__main__':
#     unittest.main()
    suite = unittest.TestSuite()
#    suite.addTest(InterpreterTests("test_or"))
    suite.addTests(loadAll(ScoreDirTests))

    suite.addTests(loadAll(MapTests))
    suite.addTests(loadAll(InterpreterTests))
    suite.addTests(loadAll(StoppingTests))

    runner = unittest.TextTestRunner()
    runner.run(suite)
