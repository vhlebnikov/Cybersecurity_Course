import numpy as np
import rc

l = 6
w = 2 ** l
b = 25 * w


def get_bit_array(input, littleEndian=True):
    b_array = bytearray(input.encode(), )
    a = []
    for byte in b_array:
        b = bin(byte)[2:].zfill(8)
        if littleEndian:
            b = b[::-1]
        ar = [int(bit) for bit in b]
        a += ar

    return np.array(a + [0, 1])


def pad(rate, message_length):
    j = (-(message_length + 2)) % rate
    return np.array([1] + [0] * j + [1])


def get_state_array(bitArray):
    stateArray = np.zeros(shape=(5, 5, w), dtype=int)
    for x in range(5):
        for y in range(5):
            for z in range(w):
                if w * (5 * y + x) + z >= len(bitArray):
                    break
                stateArray[x][y][z] = bitArray[w * (5 * y + x) + z]
    return stateArray


def theta(A):
    C = np.zeros([5, w], dtype=int)
    D = np.zeros([5, w], dtype=int)
    A1 = A.copy()
    for x in range(0, 5):
        for y in range(0, 5):
            C[x] ^= A[x][y]

    for x in range(0, 5):
        D[x] = C[(x - 1) % 5] ^ np.roll(C[(x + 1) % 5], 1)

    for x in range(0, 5):
        for y in range(0, 5):
            A1[x][y] ^= D[x]

    return A1


def rho(A):
    A1 = A.copy()
    (x, y) = (1, 0)
    for t in range(24):
        A1[x][y] = np.roll(A[x][y], (t + 1) * (t + 2) // 2)
        (x, y) = (y, (2 * x + 3 * y) % 5)

    return A1


def pi(A):
    A1 = A.copy()
    for x in range(0, 5):
        for y in range(0, 5):
            A1[x][y] = A[(x + 3 * y) % 5][x]

    return A1


def chi(A):
    A1 = A.copy()
    for x in range(5):
        for y in range(5):
            A1[x][y] ^= (A[(x + 1) % 5][y] ^ 1) & A[(x + 2) % 5][y]
    return A1


def iota(A, i):
    A1 = A.copy()
    RC = rc.get_round_const(i, calculate=False)
    A1[0][0] ^= RC
    return A1


def squeeze(array, bits):
    initial_hash = ''
    for j in range(5):
        for i in range(5):
            lane = array[i][j]
            binary_lane = ''.join(map(str, lane))

            for n in range(0, len(binary_lane), 8):
                byte = binary_lane[n:n + 8]
                byte = byte[::-1]
                hex_byte = '{0:02x}'.format(int(byte, 2))
                initial_hash += hex_byte

    return initial_hash[:bits // 4]


def keccak(state):
    rounds = 12 + 2 * l
    for round_index in range(rounds):
        state = iota(chi(pi(rho(theta(state)))), round_index)
    return state


def sha3(message, bits):
    capacity = 2 * bits
    rate = b - capacity

    bitstring = get_bit_array(message)
    padded = np.concatenate((bitstring, pad(rate, len(bitstring) % rate)))

    sponge_rounds = len(padded) // rate
    state = np.zeros(b, dtype=int).reshape(5, 5, w)

    for i in range(sponge_rounds):
        block = padded[(i * rate):(i * rate) + rate]
        array = get_state_array(block)
        state = np.bitwise_xor(state, array)
        state = keccak(state)

    return squeeze(state, bits)


def sha3_224(input):
    return sha3(input, 224)


def sha3_256(input):
    return sha3(input, 256)


def sha3_384(input):
    return sha3(input, 384)


def sha3_512(input):
    return sha3(input, 512)
