import math

res = 0x0
shift = 1


def rc(t):
    result = 0x1

    for i in range(1, t + 1):
        result <<= 1
        if result & 0x100:
            result ^= 0x71

    return result & 0x1


if __name__ == '__main__':
    for i in range(24):
        res = 0x0
        shift = 1
        for j in range(7):
            val = rc(7 * i + j)
            res |= val << (shift - 1)
            shift *= 2

        print(hex(res))
