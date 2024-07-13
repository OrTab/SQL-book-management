from config import hash_key


def validate_username_password_existence(username, password):
    if not username or not password:
        raise ValueError("Username or password cannot be empty.")


def encrypt_decrypt_password(password):
    _password = ""
    for i, char in enumerate(password):
        hashed_char = chr(ord(char) ^ ord(hash_key[i % len(hash_key)]))
        _password += hashed_char
    return _password
