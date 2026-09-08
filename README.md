#  Ecommerce

## Prerequisites

Before you get started, ensure you have the following installed on your local machine:

* **Python 3.10+**
* **MySQL Server** (v5.7 or higher)
* **pip** (Python package manager)

---

## Getting Started (Local Setup)

Follow these sequential steps to clone the repository and run the application locally.

### 1. Clone the Repository
```bash
git clone https://github.com/RoseAstral/ecommerce-2.git
```
```bash
cd ecommerce
```
### 2. Set Up a Virtual Environment
```bash
# Create the environment
python -m venv venv

# Activate on macOS/Linux:
source venv/bin/activate

# Activate on Windows:
venv\Scripts\activate
```

### 3. Install Dependencies
```bash
pip install -r requirements.txt
```

---

## Database Setup (MySQL)

### 1. Create the Database & User
Log into your local MySQL server as the root user:
```bash
mysql -u root -p
```

Once inside the MySQL shell, run the following queries to create your database, a dedicated user, and grant privileges:
```sql
-- Create the project database
CREATE DATABASE my_django_db CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;

-- Create a dedicated user (replace 'your_password' with a secure password)
CREATE USER 'django_user'@'localhost' IDENTIFIED BY 'your_password';

-- Grant privileges to the user on your new database
GRANT ALL PRIVILEGES ON my_django_db.* TO 'django_user'@'localhost';

-- Flush privileges to apply changes and exit
FLUSH PRIVILEGES;
EXIT;
```

---

## Environment Configuration

This project uses `django-decouple` to manage configurations and secrets securely. 

### 1. Initialize your `.env` file
Copy the provided environmental template file to create your active configuration file:
```bash
# On macOS/Linux:
cp .env.example .env

# On Windows (Command Prompt):
copy .env.example .env

# On Windows (PowerShell):
cp .env.example .env
```

### 2. Populate the `.env` Credentials
Open the newly created `.env` file in the root directory (alongside `manage.py`) and update the placeholders with your local settings:

* **Django Settings:** Update your `SECRET_KEY`, set `DEBUG=True`, and configure `ALLOWED_HOSTS`.
* **Database Connection:** Insert your MySQL `DB_NAME`, `DB_USER`, and `DB_PASSWORD` created in the previous step.
* **Email Configuration:** Supply your SMTP details (e.g., Gmail App Password) under the `EMAIL_` variables. Alternatively, you can use the terminal console backend for offline testing by toggling the `EMAIL_BACKEND` setting mentioned in the file.

> **Security Warning:** Never commit your `.env` file to version control. Ensure `.env` is explicitly listed in your `.gitignore` file.

---

##  Run the Application

### 1. Apply Database Migrations
Generate and apply Django's system and application tables to your local MySQL schema:
```bash
python manage.py makemigrations
python manage.py migrate
```

### 2. Create a Superuser
Create an administrative account to access the Django admin panel (`/admin`):
```bash
python manage.py createsuperuser
```

### 3. Start the Development Server
```bash
python manage.py runserver
```
Open your browser and navigate to `http://127.0.0`.
