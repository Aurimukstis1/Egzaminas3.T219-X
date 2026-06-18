from fastapi import FastAPI
from pydantic import BaseModel
from cryptography import Cryptography
from SqlProcessing import SqlProcessing

app = FastAPI()
sqli = SqlProcessing()
qrty = Cryptography()

class Auth(BaseModel):
    FirstName: str
    LastName: str
    Password: str

@app.get("/")
async def index():
    return {}

@app.post("/auth", status_code=200)
async def authenticate(auth: Auth):
    encoded:str = qrty.encode_password(auth.Password)
    valid = sqli.validate_author(auth.LastName, auth.FirstName, encoded)

    if (valid > 0):
        # if valid, return API token -> validated
        return { "token" : qrty.generate_token(valid) }
    else:
        # if invalid:
        # - make new account in database with password and name
        id = sqli.insert_credentials(auth.LastName, auth.FirstName, encoded)
        if (id <= 0):
            return { "error" : "validation error" }
        sqli.insert_author(id)

        # - generate API token for session
        return { "token" : qrty.generate_token(id) }


# @app.get("/items/{item_id}")
# async def read_item(item_id: int, q: str | None = None):
#     return {"item_id": item_id, "q": q}