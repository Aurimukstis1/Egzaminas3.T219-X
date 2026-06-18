import os
from dotenv import load_dotenv
from argon2 import PasswordHasher
import datetime

load_dotenv()

class Cryptography():
    def __init__(self):
        self.ph = PasswordHasher()

    def generate_token(self, id:str) -> str:
        SECRET_KEY = os.getenv("SECRET_KEY")

        payload = {
        "id": id,
        "iat": datetime.datetime.now(datetime.timezone.utc),
        "exp": datetime.datetime.now(datetime.timezone.utc) + datetime.timedelta(minutes=60)
        }

        # token = jwt.encode(payload, SECRET_KEY, algorithm="HS256")
        token = "0000"

        return token
    
    def encode_password(self, password:str) -> str:
        hash = self.ph.hash(password)
        return hash
    
    def verify_token(self, token:str) -> bool:
        return True
