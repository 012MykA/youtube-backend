from bcrypt import hashpw, gensalt, checkpw

def get_password_hash(password: str) -> str:
    password_bytes = password.encode('utf-8')
    salt = gensalt()
    hashed_password = hashpw(password_bytes, salt)

    return hashed_password.decode('utf-8')

def verify_password(plain_password: str, hashed_password: str) -> bool:
    plain_password_bytes = plain_password.encode('utf-8')
    hashed_password_bytes = hashed_password.encode('utf-8')
    
    return checkpw(plain_password_bytes, hashed_password_bytes)
