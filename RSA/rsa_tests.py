import unittest
import my_rsa
import rsa.core


class MyTestCase(unittest.TestCase):
    def test_little_comparison_with_real_rsa(self):
        nbits = 1024

        file = open("files/input.txt", "rb")
        s = file.read()
        file.close()

        public_key, private_key = my_rsa.generate_RSA_keys(nbits)

        my_enc = my_rsa.encrypt(s, public_key)

        block_len = (public_key[1].bit_length() - 1) // 8
        blocks = my_rsa.bytes_to_blocks(s, block_len)
        rsa_enc = my_rsa.blocks_to_bytes(
            [rsa.core.encrypt_int(block, public_key[0], public_key[1]) for block in blocks])

        self.assertEqual(my_enc, rsa_enc)

        my_dec = my_rsa.decrypt(my_enc, private_key)

        block_len = ((private_key[1].bit_length() - 1) // 8) + 1
        blocks = my_rsa.bytes_to_blocks(rsa_enc, block_len)
        rsa_dec = my_rsa.blocks_to_bytes(
            [rsa.core.decrypt_int(block, private_key[0], private_key[1]) for block in blocks])

        self.assertEqual(my_dec, rsa_dec)
        self.assertEqual(s, bytes(my_dec))

        print("Test with small data\n",
              "Initial data                   =", s, "\n",
              "Public key                     =", public_key, "\n",
              "Private key                    =", private_key, "\n",
              "My realization encryption      =", my_enc, "\n",
              "Library realization encryption =", rsa_enc, "\n",
              "My realization decryption      =", my_dec, "\n",
              "Library realization decryption =", rsa_dec, "\n")

    def test_with_big_data(self):
        nbits = 1024

        file = open("files/big_data.txt", "rb")
        s = file.read()
        file.close()

        public_key, private_key = my_rsa.generate_RSA_keys(nbits)

        my_enc = my_rsa.encrypt(s, public_key)

        block_len = (public_key[1].bit_length() - 1) // 8
        blocks = my_rsa.bytes_to_blocks(s, block_len)
        rsa_enc = my_rsa.blocks_to_bytes(
            [rsa.core.encrypt_int(block, public_key[0], public_key[1]) for block in blocks])

        self.assertEqual(my_enc, rsa_enc)

        my_dec = my_rsa.decrypt(my_enc, private_key)

        block_len = ((private_key[1].bit_length() - 1) // 8) + 1
        blocks = my_rsa.bytes_to_blocks(rsa_enc, block_len)
        rsa_dec = my_rsa.blocks_to_bytes(
            [rsa.core.decrypt_int(block, private_key[0], private_key[1]) for block in blocks])

        self.assertEqual(my_dec, rsa_dec)
        self.assertEqual(s, bytes(my_dec))

        print("Test with big data\n",
              "Public key                     =", public_key, "\n",
              "Private key                    =", private_key, "\n", )

    def test_file_signature(self):
        nbits = 1024
        file_name = "files/big_data.txt"

        public_key, private_key = my_rsa.generate_RSA_keys(nbits)

        signature = my_rsa.sign_file(file_name, private_key)
        verification_result = my_rsa.verify_signature(file_name, signature, public_key)
        self.assertEqual(verification_result, True)

        print("File signature test", "\n",
              "Signature =", signature, "\n",
              "Result =", verification_result, "\n")


if __name__ == '__main__':
    unittest.main()
