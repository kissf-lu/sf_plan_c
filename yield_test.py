# -*- coding: utf8 -*-

from inspect import isgeneratorfunction


def fab(max):
    n, a, b = 0, 0, 1
    while n < max:
        yield b
        # print b
        a, b = b, a + b
        n = n + 1


if __name__ == '__main__':
    f = fab(5)
    print(type(f))
    for i in f:
        print(i)
