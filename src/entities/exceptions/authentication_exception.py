

class AuthenticationException(Exception):
    def __init__(self, login: str):
        super().__init__(f"Invalid credentials for {login}")
