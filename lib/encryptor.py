import json


def encrypt_JSON(dic):  # E(x) ≡ ax + b (mod 256),
    dic_string = json.dumps(dic)
    encrypted = ""
    (a, b, n) = (97, 153, 256)
    for char in dic_string:
        x = ord(char)
        encrypted += chr(((x * a) + b) % n)
    return encrypted


def decrypt_JSON(str):  # D(y) ≡ v(y − b) (mod 256)
    (v, b, n) = (-95, 153, 256)
    decrypted = ""
    for char in str:
        y = ord(char)
        decrypted += chr((v * (y - b)) % n)
    dic = json.loads(decrypted)
    return dic


def encrypt_name(name):
    encrypted = ''
    (a, b, n) = (37, 44, 63)
    valid_char = {"a": 0, "b": 1, "c": 2, "d": 3, "e": 4, "f": 5, "g": 6, "h": 7, "i": 8, "j": 9, "k": 10, "l": 11,
                  "m": 12, "n": 13, "o": 14, "p": 15, "q": 16, "r": 17, "s": 18, "t": 19, "u": 20, "v": 21, "w": 22,
                  "x": 23, "y": 24, "z": 25, "A": 26, "B": 27, "C": 28, "D": 29, "E": 30, "F": 31, "G": 32, "H": 33,
                  "I": 34, "J": 35, "K": 36, "L": 37, "M": 38, "N": 39, "O": 40, "P": 41, "Q": 42, "R": 43, "S": 44,
                  "T": 45, "U": 46, "V": 47, "W": 48, "X": 49, "Y": 50, "Z": 51, "0": 52, "1": 53, "2": 54, "3": 55,
                  "4": 56, "5": 57, "6": 58, "7": 59, "8": 60, "9": 61, "_": 62}
    to_char = 'abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789_'

    for char in name:
        c = valid_char[char]
        encrypted += to_char[((c * a) + b) % n]
    return encrypted


def decrypt_name(name):
    (v, b, n) = (-17, 44, 63)
    valid_char = {"a": 0, "b": 1, "c": 2, "d": 3, "e": 4, "f": 5, "g": 6, "h": 7, "i": 8, "j": 9, "k": 10, "l": 11,
                  "m": 12, "n": 13, "o": 14, "p": 15, "q": 16, "r": 17, "s": 18, "t": 19, "u": 20, "v": 21, "w": 22,
                  "x": 23, "y": 24, "z": 25, "A": 26, "B": 27, "C": 28, "D": 29, "E": 30, "F": 31, "G": 32, "H": 33,
                  "I": 34, "J": 35, "K": 36, "L": 37, "M": 38, "N": 39, "O": 40, "P": 41, "Q": 42, "R": 43, "S": 44,
                  "T": 45, "U": 46, "V": 47, "W": 48, "X": 49, "Y": 50, "Z": 51, "0": 52, "1": 53, "2": 54, "3": 55,
                  "4": 56, "5": 57, "6": 58, "7": 59, "8": 60, "9": 61, "_": 62}
    to_char = 'abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789_'
    decrypted = ''
    for char in name:
        y = valid_char[char]
        decrypted += to_char[(v * (y - b)) % n]
    return decrypted
