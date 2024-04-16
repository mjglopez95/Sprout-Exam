# Sprout-Exam

### Prerequisites
Python 3.9
Postgresql


### Setup
1. Create virtual environment

pip install virtualenv
python3.9 -m venv env
source env/bin/activate


2. Install dependencies / libraries

pip install -r requirements.txt


3. Create database

sudo -u postgres -i
createdb sprout_exam


4. Copy the sample .env file and input necessary details

cd backend 
cp .env.example .env


5. Run local

cd backend
uvicorn main:app --reloads

### Changes in DB using Alembic
1. Initialize

alembic init alembic 


2. Applying changes

alembic revision --autogenerate -m “insert commit
alembic upgrade head