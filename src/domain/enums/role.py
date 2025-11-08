from enum import Enum as PyEnum


class RoleEnum(str, PyEnum):
    user = "user"
    admin = "admin"