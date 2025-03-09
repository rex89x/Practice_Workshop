from fastapi import FastAPI, Request
from sqlalchemy import create_engine, text
from fastapi.templating import Jinja2Templates

app = FastAPI()
templates = Jinja2Templates(directory="templates")

# 連線 Cloud SQL
DB_USER = "DB_USER_NAME"
DB_PASSWORD = "DB_PASSWORD"
DB_NAME = "DB_NAME"
DB_HOST = "DB_HOST"
DB_PORT = "3306" # My SQL Port

db_url = f"mysql+pymysql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"
engine = create_engine(db_url)

@app.get("/")
def read_root(request: Request):
    with engine.connect() as conn:
        result = conn.execute(text("SELECT id, name, email FROM user_database.users")).fetchall()
    
    return templates.TemplateResponse("index.html", {"request": request, "users": result})