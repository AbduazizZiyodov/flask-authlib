from flask import Request
from ..schemas import User


class Guard:
    def can_activate(self, user: User) -> bool:
        return True


class AdminOnly(Guard):
    def can_activate(self, user: User):
        return bool(user.is_admin)
