import mysql.connector
from dotenv import load_dotenv
import os

load_dotenv()

class SqlProcessing():
    def __init__(self):
        self.conn = mysql.connector.connect(
            host="localhost",
            user="root",
            password=os.getenv("DB_KEY")
        )
        self.cursor = self.conn.cursor()

    async def validate_connection(self):
        pass

    async def insert_credentials(self, lastname:str, firstname:str, passhash:str) -> str:
        self.cursor.execute(
            f"""
            INSERT INTO CREDENTIAL (Admin, LastName, FirstName, PassHash) 
            VALUES (false, '{lastname}', '{firstname}', '{passhash}');

            SELECT ID FROM CREDENTIAL WHERE PassHash = '{passhash}';
            """
        )
        row = self.cursor.fetchone()
        return row[0]

    async def insert_author(self, credential_id:str):
        self.cursor.execute(
            f"""
            INSERT INTO AUTHOR (CREDENTIALS_ID) 
            VALUES ((SELECT ID FROM CREDENTIAL WHERE PassHash = '{credential_id}'));
            """
        )
        return
    
    async def validate_author(self, lastname:str, firstname:str, passhash:str):
        return 0

