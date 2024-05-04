from db.schema import User
from users.helpers.password_encryption import verify_password
from sqlalchemy.orm import Session


def authenticate_user(db: Session, email: str, password: str) -> User:
    """
    Authenticates a user by checking if the email and password match a user in the database.

    Args:
        db (Session): The database session.
        email (str): The email of the user.
        password (str): The password of the user.

    Returns:
        User: The user if the email and password match, None otherwise.
    """
    user = db.query(User).filter(User.email == email).first()
    if not user:
        return None
    if not verify_password(password, user.hashed_password):
        return None
    return user
