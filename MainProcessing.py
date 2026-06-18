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

class Book(BaseModel):
    Token: str
    Title: str
    Body: str
    Category: int

@app.get("/")
async def index():
    return {}

@app.post("/books", status_code=201)
async def create_book(body: Book):
    return { { "book_id":"" } }

@app.post("/books", status_code=200)
async def get_books(token: str):
    return { [ { "book_id":"", "author":"", "title":"", "category":"" } ] }

@app.post("/books/{book_id}", status_code=200)
async def get_book(token: str, book_id: int):
    return { { "book_id":"", "author":"", "title":"", "category":"", "body":"" } }

@app.put("/books/{book_id}", status_code=200)
async def update_book(token:str, title:str, body:str, category:str, book_id:int):
    return { { "book_id":"" } }

@app.delete("/books/{book_id}", status_code=204)
async def delete_book(token:str, book_id:int):
    return { { "book_id":"" } }

@app.post("/auth", status_code=200)
async def authenticate(auth: Auth):
    encoded:str = qrty.encode_password(auth.Password)
    valid = await sqli.validate_author(auth.LastName, auth.FirstName, encoded)

    if (valid > 0):
        # if valid, return API token -> validated
        return { "token" : qrty.generate_token(valid) }
    else:
        # if invalid:
        # - make new account in database with password and name
        id = await sqli.insert_credentials(auth.LastName, auth.FirstName, encoded)
        if (int(id) <= 0):
            return { "error" : "validation error" }
        sqli.insert_author(id)

        # - generate API token for session
        return { "token" : qrty.generate_token(id) }
