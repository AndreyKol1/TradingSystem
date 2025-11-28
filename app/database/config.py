import os 
from dotenv import load_dotenv 

load_dotenv()

def get_connetion_string():
        USER = os.getenv("POSTGRES_USER")
        PASSWORD = os.getenv("POSTGRES_PASSWORD") 
        DB = os.getenv("POSTGRES_DB") 
        HOST = os.getenv("POSTGRES_HOST", "postgres") 
        PORT = os.getenv("POSTGRES_PORT", "5432") 

        return f"postgresql://{USER}:{PASSWORD}@{HOST}:{PORT}/{DB}"

CONN_STRING = get_connetion_string()
 

