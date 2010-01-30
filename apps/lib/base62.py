"""to-and-from base 62 encoding"""
import string

CHARS = ''.join((string.ascii_lowercase, string.ascii_uppercase,
                 string.digits))
BASE = len(CHARS)

VALID_SLUG_CHARS = ''.join((CHARS, '_-'))

def to62(number):
    """encodes a positive integer in base 62."""
    n = int(number)
    assert(n > 0)

    result = []
    while n:
        (n, r) = divmod(n, BASE)
        result.append(CHARS[r])
    result.reverse()
    return "".join(result) or CHARS[0]

def from62(base62str):
    """decodes a base 62 encoded string to base 10"""
    num = 0
    for i in range(len(base62str)):
        digit = CHARS.find(base62str[-i-1])
        assert(digit >= 0)
        num += digit * (62**i)
    return num

