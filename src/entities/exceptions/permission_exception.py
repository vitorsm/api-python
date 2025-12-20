
from src.entities.user import User


class PermissionException(Exception):

    def __init__(self, user: User):
        super().__init__(f"User {user.login} ({user.id}) does not have permission to perform this action")
        self.user = user