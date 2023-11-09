import random
import string
import unittest

import kuznechik


def generate_string(length, filename):
    characters = string.printable
    random_unicode_string = ''.join(random.choice(characters) for _ in range(length))

    write_to_file(random_unicode_string, filename)
    return random_unicode_string


def write_to_file(data, filename):
    f = open(filename, 'w')
    f.write(data)
    f.close()


def read_from_file(filename):
    f = open(filename, 'rb')
    out = f.read()
    f.close()
    return out


master_key = int('8899aabbccddeeff0011223344556677fedcba98765432100123456789abcdef', 16)  # 32 bytes


class Tests(unittest.TestCase):
    def test_japanese(self):
        kuznechik.get_keys(master_key)

        x = kuznechik.get_string_from_file("files/input1.txt")
        x_bytes = kuznechik.text_to_bytes(x)

        actual_enc = kuznechik.encrypt(x_bytes)
        write_to_file(hex(actual_enc), 'files/enc1.txt')

        enc_from_file = read_from_file('files/enc1.txt')
        enc_from_file = int(enc_from_file[2:], 16)

        actual_dec = kuznechik.decrypt(enc_from_file)
        write_to_file(hex(actual_dec), 'files/dec1.txt')

        dec_from_file = read_from_file('files/dec1.txt')
        dec_from_file = int(dec_from_file[2:], 16)

        actual_dec_text = kuznechik.bytes_to_text(dec_from_file)

        print("x   =", hex(x_bytes))
        print("e_a =", hex(enc_from_file))
        print("d_a =", hex(dec_from_file))
        print("d_text =", actual_dec_text)

        f = open("files/input1.txt", "r", encoding='utf-8')
        expected_text = f.read()
        f.close()
        print("e_text =", expected_text)

        self.assertEqual(expected_text, actual_dec_text)
        self.assertEqual(x_bytes, actual_dec)



