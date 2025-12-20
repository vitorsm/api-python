from src.entities.user import User


class AuthUser:
    id: str
    login: str
    name: str

    def __init__(self, user: User):
        self.id = str(user.id)
        self.login = user.login
        self.name = user.name
