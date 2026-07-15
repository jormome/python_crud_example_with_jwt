"""
Password security utilities using bcrypt.
"""

import bcrypt

from api.config.settings import settings


class PasswordSecurity:
    @staticmethod
    def hash_password(password: str) -> str:
        """Generate the hash of the password."""

        salt: bytes = bcrypt.gensalt(rounds=settings.BCRYPT_ROUNDS)
        return bcrypt.hashpw(
            password.encode("utf-8"),
            salt,
        ).decode("utf-8")

    @staticmethod
    def verify_password(password: str, hashed_password: str) -> bool:
        """Verify the password."""

        return bcrypt.checkpw(
            password.encode("utf-8"),
            hashed_password.encode("utf-8"),
        )
