code README.md

# Budgeting Tracker

A simple Django web application for managing personal transactions and categories, with per-user authentication and authorization.

## Features

- **Authentication & Authorization**
  - User registration, login, and logout
  - Each user can only access their own transactions and categories
- **Transactions & Categories CRUD**
  - Create, read, update, and delete transactions
  - Manage categories linked to transactions
- **Planned Features**
  - Password reset/change
  - Account deletion
  - Transaction analytics (charts, summaries)

## Technologies

- **Backend:** Python, Django  
- **Database:** PostgreSQL  
- **Frontend:** Django templates, basic CSS  
- **Deployment:** Railway (planned) 

## Installation

1. Clone the repository:
```bash
git clone https://github.com/yourusername/budgeting-tracker.git
cd budgeting-tracker
```
2. Create a virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # Linux/Mac
venv\Scripts\activate     # Windows
```
3. Install dependencies:
```bash
pip install -r requirements.txt
```
4. Set environment variables (e.g., in .env):
```bash
SECRET_KEY=your_secret_key
DEBUG=True
DATABASE_URL=your_db_url
```
5. Apply migrations:
```bash
python manage.py migrate
```
6. Run the development server:
```bash
python manage.py runserver
```
7. Open http://127.0.0.1:8000/ in your browser.

## Usage

- Register a new user account
- Create categories and transactions
- Edit or delete transactions/categories
- Each user sees only their own data

## License

MIT License