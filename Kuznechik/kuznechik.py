pi = [252, 238, 221, 17, 207, 110, 49, 22, 251, 196, 250, 218, 35, 197, 4, 77,
      233, 119, 240, 219, 147, 46, 153, 186, 23, 54, 241, 187, 20, 205, 95, 193,
      249, 24, 101, 90, 226, 92, 239, 33, 129, 28, 60, 66, 139, 1, 142, 79,
      5, 132, 2, 174, 227, 106, 143, 160, 6, 11, 237, 152, 127, 212, 211, 31,
      235, 52, 44, 81, 234, 200, 72, 171, 242, 42, 104, 162, 253, 58, 206, 204,
      181, 112, 14, 86, 8, 12, 118, 18, 191, 114, 19, 71, 156, 183, 93, 135,
      21, 161, 150, 41, 16, 123, 154, 199, 243, 145, 120, 111, 157, 158, 178, 177,
      50, 117, 25, 61, 255, 53, 138, 126, 109, 84, 198, 128, 195, 189, 13, 87,
      223, 245, 36, 169, 62, 168, 67, 201, 215, 121, 214, 246, 124, 34, 185, 3,
      224, 15, 236, 222, 122, 148, 176, 188, 220, 232, 40, 80, 78, 51, 10, 74,
      167, 151, 96, 115, 30, 0, 98, 68, 26, 184, 56, 130, 100, 159, 38, 65,
      173, 69, 70, 146, 39, 94, 85, 47, 140, 163, 165, 125, 105, 213, 149, 59,
      7, 88, 179, 64, 134, 172, 29, 247, 48, 55, 107, 228, 136, 217, 231, 137,
      225, 27, 131, 73, 76, 63, 248, 254, 141, 83, 170, 144, 202, 216, 133, 97,
      32, 113, 103, 164, 45, 43, 9, 91, 203, 155, 37, 208, 190, 229, 108, 82,
      89, 166, 116, 210, 230, 244, 180, 192, 209, 102, 175, 194, 57, 75, 99, 182]

pi_inv = [165, 45, 50, 143, 14, 48, 56, 192, 84, 230, 158, 57, 85, 126, 82, 145,
          100, 3, 87, 90, 28, 96, 7, 24, 33, 114, 168, 209, 41, 198, 164, 63,
          224, 39, 141, 12, 130, 234, 174, 180, 154, 99, 73, 229, 66, 228, 21, 183,
          200, 6, 112, 157, 65, 117, 25, 201, 170, 252, 77, 191, 42, 115, 132, 213,
          195, 175, 43, 134, 167, 177, 178, 91, 70, 211, 159, 253, 212, 15, 156, 47,
          155, 67, 239, 217, 121, 182, 83, 127, 193, 240, 35, 231, 37, 94, 181, 30,
          162, 223, 166, 254, 172, 34, 249, 226, 74, 188, 53, 202, 238, 120, 5, 107,
          81, 225, 89, 163, 242, 113, 86, 17, 106, 137, 148, 101, 140, 187, 119, 60,
          123, 40, 171, 210, 49, 222, 196, 95, 204, 207, 118, 44, 184, 216, 46, 54,
          219, 105, 179, 20, 149, 190, 98, 161, 59, 22, 102, 233, 92, 108, 109, 173,
          55, 97, 75, 185, 227, 186, 241, 160, 133, 131, 218, 71, 197, 176, 51, 250,
          150, 111, 110, 194, 246, 80, 255, 93, 169, 142, 23, 27, 151, 125, 236, 88,
          247, 31, 251, 124, 9, 13, 122, 103, 69, 135, 220, 232, 79, 29, 78, 4,
          235, 248, 243, 62, 61, 189, 138, 136, 221, 205, 11, 19, 152, 2, 147, 128,
          144, 208, 36, 52, 203, 237, 244, 206, 153, 16, 68, 64, 146, 58, 1, 38,
          18, 26, 72, 104, 245, 129, 139, 199, 214, 32, 10, 8, 0, 76, 215, 116]


l_vec = [1, 148, 32, 133, 16, 194, 192, 1, 251, 1, 192, 194, 16, 133, 32, 148]
iter_c = []  # 16 bytes
iter_keys = []  # 16 bytes

BLOCK_SIZE = 16


def X(a, b):
    return a ^ b


def S(a):
    res = 0
    for i in reversed(range(16)):
        res = res << 8
        res = res ^ (pi[(a >> (8 * i)) & 0xff])
    return res


def S_inv(a):
    res = 0
    for i in reversed(range(16)):
        res = res << 8
        res = res ^ (pi_inv[(a >> (8 * i)) & 0xff])
    return res


def L(a):
    res = a
    for i in range(16):
        c = 0  # будущий старший байт
        for j in range(16):
            c = c ^ mul_polynomial((res >> (8 * j)) & 0xff, l_vec[j])
        res = res >> 8
        res = res ^ (c << 120)
    return res


def L_inv(a):
    res = a
    for i in range(16):
        c = 0  # будущий младший байт
        for j in range(16):
            c = c ^ mul_polynomial((res >> (8 * j)) & 0xff, l_vec[(j + 1) % 16])
        res = res << 8
        res = res ^ c
        res = res & ((1 << 128) - 1)
    return res


def mul_polynomial(a, b):
    res = 0
    for i in range(8):
        if b & 1 == 1:
            res = res ^ a
        hi_bit_set = a & 0x80
        a = a << 1
        if hi_bit_set == 0x80:
            a = a ^ 0xc3  # x^8+x^7+x^6+x+1
        b = b >> 1
    return res % 256


def get_iter_c():
    for i in range(1, 33):
        iter_c.append(L(i))


def get_keys(key):
    get_iter_c()
    k1 = key >> 128
    k2 = key & ((1 << 128) - 1)
    iter_keys.append(k1)
    iter_keys.append(k2)
    for i in range(4):
        for j in range(8):
            tmp = k1
            k1 = X(L(S(X(k1, iter_c[i * 8 + j]))), k2)
            k2 = tmp
        iter_keys.append(k1)
        iter_keys.append(k2)


def encrypt_block(block):
    out_block = block
    for i in range(9):
        out_block = L(S(X(iter_keys[i], out_block)))
    out_block = X(iter_keys[9], out_block)
    return out_block


def encrypt(input):
    res = 0
    i = 0
    while input != 0:
        block = input & ((1 << 128) - 1)
        encrypted_block = encrypt_block(block)
        res = res ^ (encrypted_block << (128 * i))
        i = i + 1
        input = input >> 128
    return res


def decrypt_block(block):
    out_block = block
    out_block = X(iter_keys[9], out_block)
    for i in reversed(range(9)):
        out_block = X(iter_keys[i], S_inv(L_inv(out_block)))
    return out_block


def decrypt(input):
    res = 0
    i = 0
    while input != 0:
        block = input & ((1 << 128) - 1)
        decrypted_block = decrypt_block(block)
        res = res ^ (decrypted_block << (128 * i))
        i = i + 1
        input = input >> 128
    return res


def get_string_from_file(filename):
    file = open(filename, "rb")
    string = file.read()
    file.close()
    return string


def text_to_bytes(text):
    res = 0
    for byte in text:
        res = res << 8
        res = res ^ byte
    pad_len = 16 - (len(text) % 16)
    if pad_len:
        res = res << 8
        res = res ^ 0x80
        pad_len = pad_len - 1
        while pad_len:
            res = res << 8
            pad_len = pad_len - 1
    return res


def bytes_to_text(bts):
    res = bytearray()
    without_pad = bts
    while without_pad & 0x80 == 0:
        without_pad = without_pad >> 8
    without_pad = without_pad >> 8
    while without_pad != 0:
        b = without_pad & 0xff
        res.insert(0, b)
        without_pad = without_pad >> 8
    return res.decode('utf-8')
