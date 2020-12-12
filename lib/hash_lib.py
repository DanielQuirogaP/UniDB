from .encryptor import encrypt_name
from .read_data import get_index

def to_binary(number, base=8):
    binary = bin(number)
    binary = binary[2:]
    while len(binary) < base:
        binary = '0' + binary
    return binary


def to_hex(number):
    hex_n = hex(number)
    hex_n = hex_n[2:]
    return hex_n


def rotate_right(x, n):
    return int(f"{x:032b}"[-n:] + f"{x:032b}"[:-n], 2)


def get_round_constants():
    return [0x428a2f98, 0x71374491, 0xb5c0fbcf, 0xe9b5dba5, 0x3956c25b, 0x59f111f1, 0x923f82a4, 0xab1c5ed5,
            0xd807aa98, 0x12835b01, 0x243185be, 0x550c7dc3, 0x72be5d74, 0x80deb1fe, 0x9bdc06a7, 0xc19bf174,
            0xe49b69c1, 0xefbe4786, 0x0fc19dc6, 0x240ca1cc, 0x2de92c6f, 0x4a7484aa, 0x5cb0a9dc, 0x76f988da,
            0x983e5152, 0xa831c66d, 0xb00327c8, 0xbf597fc7, 0xc6e00bf3, 0xd5a79147, 0x06ca6351, 0x14292967,
            0x27b70a85, 0x2e1b2138, 0x4d2c6dfc, 0x53380d13, 0x650a7354, 0x766a0abb, 0x81c2c92e, 0x92722c85,
            0xa2bfe8a1, 0xa81a664b, 0xc24b8b70, 0xc76c51a3, 0xd192e819, 0xd6990624, 0xf40e3585, 0x106aa070,
            0x19a4c116, 0x1e376c08, 0x2748774c, 0x34b0bcb5, 0x391c0cb3, 0x4ed8aa4a, 0x5b9cca4f, 0x682e6ff3,
            0x748f82ee, 0x78a5636f, 0x84c87814, 0x8cc70208, 0x90befffa, 0xa4506ceb, 0xbef9a3f7, 0xc67178f2]


def hash_password(password):
    binary_pass = ''.join(format(ord(i), 'b') for i in password)
    binary_pass += '1'
    while len(binary_pass) % 512 != 440:
        binary_pass += '0'

    length = len(password) % 256
    bin_len = to_binary(length)
    binary_pass += bin_len

    chink_size = 448
    chunks = [binary_pass[i:i+chink_size] for i in range(0, len(binary_pass), chink_size)]

    h0 = 0x6a09e667
    h1 = 0xbb67ae85
    h2 = 0x3c6ef372
    h3 = 0xa54ff53a
    h4 = 0x510e527f
    h5 = 0x9b05688c
    h6 = 0x1f83d9ab
    h7 = 0x5be0cd19

    round_constants = get_round_constants()

    for chunk in chunks:
        message_schedule = [int(chunk[i:i+32], 2) for i in range(0,len(chunk), 32)]

        while len(message_schedule) < 64:
            message_schedule.append(0)

        for i in range(16, 64):
            s0 = rotate_right(message_schedule[i-15], 7) ^ rotate_right(message_schedule[i-15], 18) ^ (message_schedule[i-15] >> 3)
            s1 = rotate_right(message_schedule[i-2], 17) ^ rotate_right(message_schedule[i-2], 19) ^ (message_schedule[i-2] >> 10)
            sum1 = (message_schedule[i-16] + s0) % (2 ** 32)
            sum2 = (message_schedule[i-7] + s0) % (2 ** 32)
            message_schedule[i] = (sum1 + sum2) % (2 ** 32)

        a = h0
        b = h1
        c = h2
        d = h3
        e = h4
        f = h5
        g = h6
        h = h7

        for i in range(0, 64):
            s1 = rotate_right(e, 6) ^ rotate_right(e, 11) ^ rotate_right(e, 25)
            ch = (e & f) ^ ((~e) & g)
            temp1 = (h + s1 + ch + round_constants[i] + message_schedule[i]) % (2**32)
            s0 = rotate_right(a, 2) ^ rotate_right(a, 13) ^ rotate_right(a, 22)
            temp2 = (a & b) ^ (a & c) ^ (b & c)
            temp3 = (s0 + temp2) % (2**32)

            h = g
            g = f
            f = e
            e = d + temp1
            d = c
            c = b
            b = a
            a = temp1 + temp3

        h0 = (h + a) % (2**32)
        h1 = (h1 + b) % (2**32)
        h2 = (h2 + c) % (2**32)
        h3 = (h3 + d) % (2**32)
        h4 = (h4 + e) % (2**32)
        h5 = (h5 + f) % (2**32)
        h6 = (h6 + g) % (2**32)
        h7 = (h7 + h) % (2**32)

    hash = to_hex(h0)+to_hex(h1)+to_hex(h2)+to_hex(h3)+to_hex(h4)+to_hex(h5)+to_hex(h6)+to_hex(h7)

    return hash


def hash_value(name):
    value = 0
    for char in name:
        value += ord(char)
    value %= 311
    return value


def find_index(name, table, encrypt=False):
    #(name)
    #print(table)
    if encrypt:
        name = encrypt_name(name)
    value = hash_value(name)
    results = table[value]
    for item in results:
        if name in item:
            #return value, item
            return True
    return False


def update_index(name, table, encrypt=False):
    updated_table = table
    if find_index(name, table):
        return updated_table
    if encrypt:
        name = encrypt_name(name)
    value = hash_value(name)
    results = updated_table[value]
    if results == ['']:
        updated_table[value] = [name]
    else:
        updated_table[value].append(name)
    return updated_table
