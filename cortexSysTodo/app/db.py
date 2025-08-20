from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base
from sqlalchemy.orm import sessionmaker

DB_URL = "mysql+pymysql://root:12345%40@localhost:3306/Cortex"


engine = create_engine(DB_URL, echo=True)   #etesal db 
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()
try:
    conn = engine.connect()
    print("✅ Connection sucsessfull")
    conn.close()
except Exception as e:
    print("❌ Connection Error", e)



# اضافه کردن این تابع
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()