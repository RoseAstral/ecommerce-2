# Ecommerce store front

## Prerequisites
```bash
﻿asgiref==3.11.1
Django==6.0.6
djangorestframework==3.17.1
mysqlclient==2.2.8
python-decouple==3.8
sqlparse==0.5.5
tzdata==2026.2
```

## Getting Started Locally

Follow these sequential steps to set up the development environment on your machine.

### 1. Clone the Repository
```bash
git clone https://github.com](https://github.com/RoseAstral/ecommerce-2.git
cd into ecommerce folder
```

### 2. Set Up a Virtual Environment
```bash
python3 -m venv venv
source venv/bin/activate  # On Windows use: venv\Scripts\activate
```

### 3. Install Dependencies
```bash
pip install --upgrade pip
pip install -r requirements.txt
```

### 4. Configure Environment Variables
Create a `.env` file in the root directory and copy the variables from `.env.example`:
```bash
cp .env.example .env
```
Open `.env` and fill out your local configuration details:
```env
EMAIL_HOST=example@gamil.com
EMAIL_PORT=587
EMAIL_HOST_USER=your-email@example.com
EMAIL_HOST_PASSWORD=your-secure-app-password
EMAIL_USE_TLS=True
```
### You will also need to link the app to a database for it to function
Open settings.py
Scroll down to the # Database section
fill in the required infomation to like the app to a database


### 5. Apply Migrations and Create a Superuser
```bash
python manage.py migrate
python manage.py createsuperuser
```

### 6. Run the Development Server
```bash
python manage.py runserver
```
Navigate to `http://127.0.0` in your browser to view the application.

##  Running Tests

To run the automated suite and ensure everything passes smoothly:

```bash
# Run standard Django tests
python manage.py test
```
