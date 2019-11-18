from test_global_var.conf import GlobalVars
import unittest


def main():
    GlobalVars.a = 1
    GlobalVars.b = 2
    GlobalVars.c = 3

    tests = list()
    loader = unittest.TestLoader()
    tests.extend(loader.loadTestsFromName("test_global_var.test_code.ThisTest"))

    suite = unittest.TestSuite()
    for test in tests:
        suite.addTest(test)
    runner = unittest.TextTestRunner()
    runner.run(suite)


if __name__=="__main__":
    main()
