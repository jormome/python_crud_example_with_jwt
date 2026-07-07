"""Utilidades para el hashing y verificación de contraseñas."""

import bcrypt

from api.config.settings import settings


class PasswordHasher:
    """Encapsula la lógica de seguridad para contraseñas."""

    @staticmethod
    def hash_password(password: str) -> str:
        """Genera un hash seguro de una contraseña de texto plano."""
        salt: bytes = bcrypt.gensalt(rounds=settings.BCRYPT_ROUNDS)
        return bcrypt.hashpw(password.encode("utf-8"), salt).decode("utf-8")

    @staticmethod
    def verify_password(plain: str, hashed: str) -> bool:
        """Comprueba si una contraseña en texto plano coincide con un hash."""
        try:
            return bcrypt.checkpw(plain.encode("utf-8"), hashed.encode("utf-8"))

        except (ValueError, TypeError, AttributeError):
            return False
