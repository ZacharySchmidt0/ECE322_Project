# tests/TestRunner.py
#The basic idea here is to have a new Python file Testrunner.py
# alongside your tests that contains our runner.
import unittest

# import your tests modules (Apply integration testing method)
import tests.TestComposeTweet as TestComposeTweet
import tests.TestFollowFeed as TestFollowFeed
import tests.TestFollowUser as TestFollowUser
import tests.TestFunctionMenu as TestFunctionMenu
import tests.TestGetFollowers as TestGetFollowers
import tests.TestGetFollowFeedTweets as TestGetFollowFeedTweets
import tests.TestGetNextTweetID as TestGetNextTweetID
import tests.TestGetTweetStatistics as TestGetTweetStatistics
import tests.TestInit as TestInit
import tests.TestInsertRetweet as TestInsertRetweet
import tests.TestInsertTweet as TestInsertTweet
import tests.TestListFollowers as TestListFollowers
import tests.TestLogin as TestLogin
import tests.TestLogout as TestLogout
import tests.TestQuit as TestQuit
import tests.TestSearchForTweets as TestSearchForTweets
import tests.TestSearchForTweetsQuery as TestSearchForTweetsQuery
import tests.TestSearchForUserQuery as TestSearchForUserQuery
import tests.TestSearchForUsers as TestSearchForUsers
import tests.TestSeeAllTweets as TestSeeAllTweets
import tests.TestShowUserInfo as TestShowUserInfo
import tests.TestSignUp as TestSignUp
import tests.TestStartScreen as TestStartScreen
import tests.TestTweetOptions as TestTweetOptions


# initialize the tests suite
loader = unittest.TestLoader()
suite  = unittest.TestSuite()

# add tests to the tests suite
suite.addTests(loader.loadTestsFromModule(TestComposeTweet))
suite.addTests(loader.loadTestsFromModule(TestFollowFeed))
suite.addTests(loader.loadTestsFromModule(TestFollowUser))
suite.addTests(loader.loadTestsFromModule(TestFunctionMenu))
suite.addTests(loader.loadTestsFromModule(TestGetFollowers))
suite.addTests(loader.loadTestsFromModule(TestGetFollowFeedTweets))
suite.addTests(loader.loadTestsFromModule(TestGetNextTweetID))
suite.addTests(loader.loadTestsFromModule(TestGetTweetStatistics))
suite.addTests(loader.loadTestsFromModule(TestInit))
suite.addTests(loader.loadTestsFromModule(TestInsertRetweet))
suite.addTests(loader.loadTestsFromModule(TestInsertTweet))
suite.addTests(loader.loadTestsFromModule(TestListFollowers))
suite.addTests(loader.loadTestsFromModule(TestLogin))
suite.addTests(loader.loadTestsFromModule(TestLogout))
suite.addTests(loader.loadTestsFromModule(TestQuit))
suite.addTests(loader.loadTestsFromModule(TestSearchForTweets))
suite.addTests(loader.loadTestsFromModule(TestSearchForTweetsQuery))
suite.addTests(loader.loadTestsFromModule(TestSearchForUserQuery))
suite.addTests(loader.loadTestsFromModule(TestSearchForUsers))
suite.addTests(loader.loadTestsFromModule(TestSeeAllTweets))
suite.addTests(loader.loadTestsFromModule(TestShowUserInfo))
suite.addTests(loader.loadTestsFromModule(TestSignUp))
suite.addTests(loader.loadTestsFromModule(TestStartScreen))
suite.addTests(loader.loadTestsFromModule(TestTweetOptions))

# initialize a runner, pass it your suite and run it
runner = unittest.TextTestRunner(verbosity=3)
result = runner.run(suite)