import math, random


def fast_pow(base, exp, mod):
    res = 1
    while exp > 0:
        if exp % 2 == 1:
            res = (res * base) % mod
        base = (base * base) % mod
        exp = exp // 2
    return res


def extended_gcd(a, b):
    x1, x2 = 1, 0
    y1, y2 = 0, 1
    while b:
        q = a // b
        a, b = b, a % b
        x1, x2 = x2, x1 - x2 * q
        y1, y2 = y2, y1 - y2 * q
    return a, x1, y1


def rabin_miller_test(n, k=0):
    if not k:
        k = math.floor(math.log2(n))

    if n <= 1 or n % 2 == 0:
        return False
    if n <= 3:
        return True

    s = 0
    t = n - 1
    while t % 2 == 0:
        s = s + 1
        t = t // 2

    for _ in range(k):
        a = random.randrange(2, n - 2)
        x = fast_pow(a, t, n)
        if x == 1 or x == n - 1:
            continue
        for _ in range(s - 1):
            x = fast_pow(x, 2, n)
            if x == 1:
                return False
            if x == n - 1:
                break
        if x != n - 1:
            return False
    return True


def generate_prime(bit_size):
    while True:
        probable_prime = random.getrandbits(bit_size)
        probable_prime = probable_prime | (1 << (bit_size - 1)) | 1
        if rabin_miller_test(probable_prime):
            return probable_prime


def generate_RSA_keys(bit_size):
    p = generate_prime(bit_size)
    q = generate_prime(bit_size)

    while p == q:
        q = generate_prime(bit_size)

    n = p * q
    phi = (p - 1) * (q - 1)

    e = random.randrange(2, phi - 1)
    gcd, _, _ = extended_gcd(e, phi)
    while gcd != 1:
        e = random.randrange(2, phi - 1)
        gcd, _, _ = extended_gcd(e, phi)

    _, d, _ = extended_gcd(e, phi)
    if d < 0:
        d = d + phi

    return (e, n), (d, n)


def bytes_to_blocks(input, block_len):
    return [int.from_bytes(input[i: i + block_len], 'little') for i in range(0, input, block_len)]


def blocks_to_bytes(input):
    array = bytearray()
    for block in input:
        array.extend(block.to_bytes(math.ceil(block.bit_length() / 8), 'little'))


def crypt(blocks, key):
    x, n = key
    return [fast_pow(block, x, n) for block in blocks]


def encrypt(input, public_key):
    e, n = public_key

    block_len = (n.bit_length() - 1) // 8
    blocks = bytes_to_blocks(input, block_len)
    encrypted = crypt(blocks, public_key)
    return blocks_to_bytes(encrypted)


def decrypt(input, private_key):
    d, n = private_key

    block_len = ((n.bit_length() - 1) // 8) + 1
    blocks = bytes_to_blocks(input, block_len)
    encrypted = crypt(blocks, private_key)
    return blocks_to_bytes(encrypted)


def hash_file
