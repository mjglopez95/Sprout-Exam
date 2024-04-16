from passlib.context import CryptContext

password_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


class Hasher:
    #generate hash for passsword
    @staticmethod
    def generate_password_hash(password):
        return password_context.hash(password)
    
    #checks if a provided password matches a stored hash
    @staticmethod
    def verify_password(plain_password, hashed_password):
        return password_context.verify(plain_password, hashed_password)