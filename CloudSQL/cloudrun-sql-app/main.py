import os
from fastapi import FastAPI, Request
from sqlalchemy import create_engine, text
from sqlalchemy.exc import OperationalError
from fastapi.templating import Jinja2Templates
import pymysql

app = FastAPI()
templates = Jinja2Templates(directory="templates")

# 連線 Cloud SQL
DB_USER = "DB_USER_NAME"
DB_PASSWORD = "DB_PASSWORD"
DB_NAME = "DB_NAME"
DB_HOST = "DB_HOST"
DB_PORT = "3306" # My SQL Port

db_url = f"mysql+pymysql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"
engine = create_engine(db_url, pool_pre_ping=True)

@app.get("/")
def read_root(request: Request):
    try:
        with engine.connect() as conn:
            result = conn.execute(text("SELECT id, name, email FROM user_database.users")).fetchall()
    except OperationalError as e:
        return {"error": "Database connection failed", "details": str(e)}
    
    return templates.TemplateResponse("index.html", {"request": request, "users": result})


# 讓 Cloud Run 使用 PORT 8080
if __name__ == "__main__":
    import uvicorn
    port = int(os.environ.get("PORT", 8080))
    uvicorn.run(app, host="127.0.0.1", port=port)