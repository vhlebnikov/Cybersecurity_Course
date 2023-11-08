import hashlib
import unittest

from sha3 import sha3_256


def get_string_from_file(filename):
    file = open(filename, "rb")
    string = file.read()
    file.close()
    return string


class Test(unittest.TestCase):
    def test_japan(self):
        data = get_string_from_file("files/japan_symbols.txt")
        actual = sha3_256(data)
        expected = hashlib.sha3_256(data).hexdigest()
        self.assertEqual(actual, expected)
        print("Actual   = ", actual)
        print("Expected = ", expected)


if __name__ == '__main__':
    unittest.main()
