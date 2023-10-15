import numpy as np

RCs = [0x0000000000000001, 0x0000000000008082, 0x800000000000808a,
       0x8000000080008000, 0x000000000000808b, 0x0000000080000001,
       0x8000000080008081, 0x8000000000008009, 0x000000000000008a,
       0x0000000000000088, 0x0000000080008009, 0x000000008000000a,
       0x000000008000808b, 0x800000000000008b, 0x8000000000008089,
       0x8000000000008003, 0x8000000000008002, 0x8000000000000080,
       0x000000000000800a, 0x800000008000000a, 0x8000000080008081,
       0x8000000000008080, 0x0000000080000001, 0x8000000080008008]


def rc(t):
    result = 0x1

    for i in range(1, t + 1):
        result <<= 1
        if result & 0x100:  # x^8
            result ^= 0x71  # x^4 + x^2 + 1 где x = 2

    return result & 0x1


def round_consts():
    array = []
    for k in range(24):
        res = 0x0
        shift = 1
        for j in range(7):
            val = rc(7 * k + j)
            res |= val << (shift - 1)
            shift *= 2

        array.append(res)
    return array


def get_round_const(r, calculate=True):
    res = 0x0
    shift = 1

    if calculate:
        for j in range(7):
            val = rc(7 * r + j)
            res |= val << (shift - 1)
            shift *= 2
    else:
        res = RCs[r]

    ans = np.array([int(b) for b in bin(res)[2:].zfill(64)])

    return np.flip(ans)
