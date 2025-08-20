# create_tables.py
from app.db import Base, engine
from app.models import User, Task

# این خط جدول‌ها رو توی دیتابیس میسازه
Base.metadata.create_all(bind=engine)
# هر مدلی که نوشتی رو بگیر، توی دیتابیس تبدیلش کن به جدول واقعی
print("✅ Tables created successfully!")
