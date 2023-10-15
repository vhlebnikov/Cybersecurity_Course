import unittest
import hashlib
import time

from string_generator import generate_string
from sha3 import sha3_224, sha3_256, sha3_384, sha3_512


class Tests(unittest.TestCase):
    def test_sha_224(self):
        input = generate_string(1024 * 1500)

        start_time = time.time()
        actual = sha3_224(input)
        end_time = time.time()
        actual_time = end_time - start_time

        start_time = time.time()
        expected = hashlib.sha3_224(input.encode()).hexdigest()
        end_time = time.time()
        expected_time = end_time - start_time

        print("SHA3-224")
        print(f"\nActual: \nTime: {actual_time}\nResult: {actual}\n")
        print('-' * 100)
        print(f"\nExpected: \nTime: {expected_time}\nResult: {expected}\n")

        self.assertEqual(actual, expected)

    def test_sha_256(self):
        input = generate_string(1024 * 1500)

        start_time = time.time()
        actual = sha3_256(input)
        end_time = time.time()
        actual_time = end_time - start_time

        start_time = time.time()
        expected = hashlib.sha3_256(input.encode()).hexdigest()
        end_time = time.time()
        expected_time = end_time - start_time

        print("SHA3-256")
        print(f"\nActual: \nTime: {actual_time}\nResult: {actual}\n")
        print('-' * 100)
        print(f"\nExpected: \nTime: {expected_time}\nResult: {expected}\n")

        self.assertEqual(actual, expected)

    def test_sha_384(self):
        input = generate_string(1024 * 1500)

        start_time = time.time()
        actual = sha3_384(input)
        end_time = time.time()
        actual_time = end_time - start_time

        start_time = time.time()
        expected = hashlib.sha3_384(input.encode()).hexdigest()
        end_time = time.time()
        expected_time = end_time - start_time

        print("SHA3-384")
        print(f"\nActual: \nTime: {actual_time}\nResult: {actual}\n")
        print('-' * 100)
        print(f"\nExpected: \nTime: {expected_time}\nResult: {expected}\n")

        self.assertEqual(actual, expected)

    def test_sha_512(self):
        input = generate_string(1024 * 1500)

        start_time = time.time()
        actual = sha3_512(input)
        end_time = time.time()
        actual_time = end_time - start_time

        start_time = time.time()
        expected = hashlib.sha3_512(input.encode()).hexdigest()
        end_time = time.time()
        expected_time = end_time - start_time

        print("SHA3-512")
        print(f"\nActual: \nTime: {actual_time}\nResult: {actual}\n")
        print('-' * 100)
        print(f"\nExpected: \nTime: {expected_time}\nResult: {expected}\n")

        self.assertEqual(actual, expected)


if __name__ == '__main__':
    unittest.main()
