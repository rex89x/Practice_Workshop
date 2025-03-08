from fastapi import FastAPI
from sqlalchemy import create_engine, text

app = FastAPI()

# 連線 Cloud SQL
DB_USER = "DB_USER_NAME"
DB_PASSWORD = "DB_PASSWORD"
DB_NAME = "DB_NAME"
DB_HOST = "DB_HOST"
DB_PORT = "3306" # My SQL Port

db_url = f"mysql+pymysql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"
engine = create_engine(db_url)

@app.get("/")
def read_root():
    with engine.connect() as conn:
        result = conn.execute(text("SELECT 'Hello from Cloud SQL!'")).fetchone()
        return {"message": result[0]}
