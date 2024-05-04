import bcrypt


def hash_password(password: str) -> bytes:
    """
    Hashes a password using bcrypt.

    Args:
        password (str): The password to hash.

    Returns:
        bytes: The hashed password.
    """
    pwd_bytes = password.encode('utf-8')
    salt = bcrypt.gensalt()
    hashed_password = bcrypt.hashpw(password=pwd_bytes, salt=salt)
    return hashed_password


def verify_password(plain_password, hashed_password) -> bool:
    """
    Verifies if a plain password matches a hashed password.

    Args:
        plain_password (str): The plain password to verify.
        hashed_password (bytes): The hashed password to compare against.

    Returns:
        bool: True if the passwords match, False otherwise.
    """
    password_byte_enc = plain_password.encode('utf-8')
    return bcrypt.checkpw(password=password_byte_enc, hashed_password=hashed_password)
