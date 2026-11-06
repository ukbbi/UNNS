from math import gcd
def denominators(labels):
    k = len(labels)
    D = [1] * (1 << k); num = [1] * (1 << k); den = [1] * (1 << k)
    for I in range(1, 1 << k):
        j = (I & -I).bit_length() - 1
        J = I & (I - 1)
        num[I] = num[J] * labels[j]
        den[I] = den[J] * (labels[j] + 1) ** 2
        D[I] = num[I] // gcd(num[I], den[I])
    return D
