from passlib.context import CryptContext

pwd_context = CryptContext(schemes= ["bcrypt"], deprecated='auto')


def hash(password:str):
    return pwd_context.hash(password)

def verify(password:str, hashed_password:str):
    return pwd_context.verify(password, hashed_password)


if __name__ == "__main__":
    print(hash("uio"), "====================", hash("uio"))      



