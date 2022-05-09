import itertools

key = ""
head_encrypt = "__en__"

def xor_crypt_string(text: str):
    return ''.join(chr(ord(x) ^ ord(y)) for (x, y) in zip(text, itertools.cycle(key)))


def encrypt(text: str):
    if not key:
        return text
    if isinstance(text, list):
        return [encrypt(t) for t in text]
    elif isinstance(text, tuple):
        return tuple(encrypt(t) for t in text)
    elif not isinstance(text, str) or text.startswith(head_encrypt):
        return text
    return head_encrypt + xor_crypt_string(text)


def decrypt(text: str):
    if not key:
        return text
    if isinstance(text, list):
        return [decrypt(t) for t in text]
    elif isinstance(text, tuple):
        return tuple(decrypt(t) for t in text)
    if not isinstance(text, str) or not text.startswith(head_encrypt):
        return text
    return xor_crypt_string(text[6:])
