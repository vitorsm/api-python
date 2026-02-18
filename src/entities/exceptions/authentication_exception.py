

class AuthenticationException(Exception):
    def __init__(self, login: str, description: str = None):
        super().__init__(f"Invalid credentials for {login}: {description if description else ''}")
