"""Prime number calculation.

This snippet was created with Salesforce/codegen-350M-mono.
"""
import math


def calculate_primes(n):
    """Create a list of consecutive integers from 2 up to N.

    For example:
    >>> calculate_primes(20)
    Output: [2, 3, 5, 7, 11, 13, 17, 19]
    """
    sieve = [True for _ in range(n+1)]
    for i in range(2, int(math.sqrt(n))+1):
        if sieve[i]:
            for j in range(i*i, n+1, i):
                sieve[j] = False
    return [2] + [i for i in range(3, n, 2) if sieve[i]]


if __name__ == "__main__":
    # added manually
    assert calculate_primes(20) == [2, 3, 5, 7, 11, 13, 17, 19]
