# tests/TestRunner.py
#The basic idea here is to have a new Python file Testrunner.py
# alongside your tests that contains our runner.
import unittest

# import your tests modules (Apply integration testing method)
import TestModuleA

# initialize the tests suite
loader = unittest.TestLoader()
suite  = unittest.TestSuite()

# add tests to the tests suite
suite.addTests(loader.loadTestsFromModule(TestModuleA))

# initialize a runner, pass it your suite and run it
runner = unittest.TextTestRunner(verbosity=3)
result = runner.run(suite)