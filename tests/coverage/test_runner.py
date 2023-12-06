import unittest

if __name__ == '__main__':
    loader = unittest.TestLoader()
    start_dir = '.'  # Assuming the test files are in the current directory
    suite = loader.discover(start_dir)

    runner = unittest.TextTestRunner()
    runner.run(suite)
