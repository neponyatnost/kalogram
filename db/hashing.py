from passlib.context import CryptContext


# This is the class that will be used to hash the password
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


# This class will be used to hash the password and verify the password
class Hashing:
    @staticmethod
    def hash_password(password: str):
        return pwd_context.hash(password)

    @staticmethod
    def verify_password(plain_password: str, hashed_password: str):
        return pwd_context.verify(plain_password, hashed_password)