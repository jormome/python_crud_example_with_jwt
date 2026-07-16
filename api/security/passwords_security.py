"""
Password security utilities using bcrypt.
"""

import bcrypt

from api.config.settings import settings


class PasswordSecurity:
    """
    Password security utilities using bcrypt.
    """

    @staticmethod
    def hash_password(
        password: str,
    ) -> str:
        """Generate the hash of the password.

        Args:
            password (str): The password to hash.

        Returns:
            str: The hashed password.
        """

        salt: bytes = bcrypt.gensalt(rounds=settings.BCRYPT_ROUNDS)
        return bcrypt.hashpw(
            password.encode("utf-8"),
            salt,
        ).decode("utf-8")

    @staticmethod
    def verify_password(
        password: str,
        hashed_password: str,
    ) -> bool:
        """Verify the password.

        Args:
            password (str): The password to verify.
            hashed_password (str): The hashed password.

        Returns:
            bool: True if the password is correct, False otherwise.
        """

        return bcrypt.checkpw(
            password.encode("utf-8"),
            hashed_password.encode("utf-8"),
        )
