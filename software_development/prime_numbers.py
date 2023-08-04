"""Prime number calculation.

This snippet was created with Starcoder.
"""


def calculate_primes(n):
    # create a list of consecutive integers from 2 up to n
    candidates = [True] * (n + 1)

    # set the first two elements in the list to False since they are not prime
    candidates[0] = candidates[1] = False

    for i in range(2, int(n ** 0.5) + 1):
        if candidates[i]:
            # mark all multiples of i as non-prime
            for j in range(i * i, n + 1, i):
                candidates[j] = False

    return [x for x in range(2, n + 1) if candidates[x]]


if __name__ == "__main__":
    # added manually
    print(eratosthenes_sieve(20))
    # Output: [2, 3, 5, 7, 11, 13, 17, 19]
