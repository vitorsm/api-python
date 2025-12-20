import bcrypt


def encrypt_password(password: str) -> str:
    return bcrypt.hashpw(password.encode("utf-8"), bcrypt.gensalt()).decode("utf-8")



def check_encrypted_password(password: str, encrypted_password: str) -> bool:
    return bcrypt.checkpw(password.encode("utf-8"), encrypted_password.encode("utf-8"))
