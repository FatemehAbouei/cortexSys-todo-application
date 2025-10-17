A Task Management REST API built with FastAPI, supporting user authentication via JWT tokens, and data persistence using SQLAlchemy ORM with a MySQL database.

🚀 Features
🔐 User Authentication with JWT (Register, Login, Token validation)
✅ CRUD operations for Tasks (Create, Read, Update, Delete)
🧩 Task filtering by priority and status using query parameters
👥 User-based access control (each user sees only their own tasks)
⚙️ Environment-based configuration with .env
🗄️ SQLAlchemy ORM integration for clean and efficient database access
📘 Interactive Swagger Docs available at /docs

📦 Installation & Setup
1. Clone the repository
git clone https://github.com/yourusername/CortexTODO.git
cd CortexTODO

2. Create and activate virtual environment
python -m venv venv
venv\Scripts\activate

3. Install dependencies
pip install -r requirements.txt

4. Create .env file

Example .env:

SECRET_KEY=your_secret_key_here
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30

DB_HOST=localhost
DB_PORT=3306
DB_USER=root
DB_PASSWORD=yourpassword
DB_NAME=cortex

5. Run the app
uvicorn app.main:app --reload


Swagger Docs: 👉 http://127.0.0.1:8000/docs

🧪 Example Endpoints
Register a new user:
POST /register/
{
  "username": "fatemeh",
  "email": "fatemeh@example.com",
  "password": "12345"
}

Login and get JWT token:
POST /login/
{
  "username": "fatemeh",
  "password": "12345"
}

Create a new task (requires Authorization header):
POST /tasks/
Authorization: Bearer <your_token>
{
  "title": "Learn FastAPI",
  "description": "Build a backend API project",
  "status": false,
  "priority": 2,
  "due_date": "2025-12-01T10:00:00Z"
}

Filter tasks by status and priority:
GET /tasks/?status=false&priority=2
