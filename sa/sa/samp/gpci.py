import random

# gpci is a client serial(not very unique though)

# length must be in the interval [4,48] and be odd, otherwise the server may
# reject it; 40 is a good value
def generate_random_gpci(length=42, factor=1001):
    '''
    The gcpi is an uppercase hex string(0-9 + A-Z).
    It is the representation(in little endian byte order) of a big number that
    is a multiple of 1001(default samp constant). So given the constraints the
    number has 2 to 24 bytes.
    '''

    # calculate the size of the number in bytes
    byte_count = length // 2

    # calculate how many integers exist with byte_count bytes(excluding the ones with fewer bytes)
    top_number = 2**(byte_count*8) # how many integers exist with byte_count bytes(including the ones with fewer bytes)
    base_number = 2**((byte_count-1)*8) # how many integers exist with (byte_count-1) bytes(including the ones with fewer bytes)
    possibilities_count = top_number - base_number

    # calculates how many of these ingetegers are multiples of factor
    possibilities_count //= factor

    # choose one of these factors
    nth_multiple_index = random.randint(0, possibilities_count)

    first_multiple = (base_number + factor)
    first_multiple -= first_multiple % factor

    # calculate the gcpi number
    number = first_multiple + factor * nth_multiple_index

    return f'{number:X}'

# returns True if gpci is valid, False otherwise
# gpci: string containing a hexadecimal representation of a number
def validate_gpci(gpci, factor=1001):
    return int(gpci, 16) % factor == 0
