from config import hash_key


def encrypt_decrypt_password(password):
    _password = ""
    for i, char in enumerate(password):
        hashed_char = chr(ord(char) ^ ord(hash_key[i % len(hash_key)]))
        _password += hashed_char
    return _password
