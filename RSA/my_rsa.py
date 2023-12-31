import math
import random
from hashlib import sha256


def sieve_of_eratosthenes(limit):
    primes = []
    numbers = [True] * (limit + 1)
    for p in range(2, limit + 1):
        if numbers[p]:
            primes.append(p)
            for i in range(p * p, limit + 1, p):
                numbers[i] = False
    return primes


low_primes = sieve_of_eratosthenes(10000)


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

    for p in low_primes:
        if n % p == 0:
            return False

    s = 0
    t = n - 1
    while t % 2 == 0:
        s = s + 1
        t = t // 2

    for _ in range(k):
        a = random.randrange(2, n - 2)
        x = pow(a, t, n)
        if x == 1 or x == n - 1:
            continue
        for _ in range(s - 1):
            x = pow(x, 2, n)
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
        bits_to_set = random.randint(1, 7)
        # 111 110 101 100 011 010 001
        probable_prime = probable_prime | (bits_to_set << (bit_size - 3)) | 1
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
    return [int.from_bytes(input[i: i + block_len], 'little') for i in range(0, len(input), block_len)]


def blocks_to_bytes(input):
    array = bytearray()
    for block in input:
        array.extend(block.to_bytes(math.ceil(block.bit_length() / 8), 'little'))
    return array


def crypt(blocks, key):
    x, n = key
    return [pow(block, x, n) for block in blocks]


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
    decrypted = crypt(blocks, private_key)
    return blocks_to_bytes(decrypted)


def hash_file(file_name):
    hasher = sha256()
    file = open(file_name, 'rb')
    block = file.read(hasher.block_size)
    while block:
        hasher.update(block)
        block = file.read(hasher.block_size)
    file.close()
    return hasher.digest()


def sign_file(file_name, private_key):
    return encrypt(hash_file(file_name), private_key)


def verify_signature(file_name, signature, public_key):
    decrypted_signature = decrypt(signature, public_key)
    file_hash = hash_file(file_name)
    if decrypted_signature == file_hash:
        return True
    return False
