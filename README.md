#  Ecommerce

## Prerequisites

Before you get started, ensure you have the following installed on your local machine:

* **Python:** 3.11+
* **Django:** 5.0+
* **Database:** MySQL
* **Package Manager:** `pip` or `poetry`

---

## Getting Started (Local Setup)

Follow these sequential steps to clone the repository and run the application locally.

### 1. Clone the Repository
```bash
git clone https://github.com
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
pip install --upgrade pip
pip install -r requirements.txt
```

### 4. Environment Variables
Create a `.env` file in the root project directory (alongside `manage.py`) and populate it with your local configurations. See `.env.example` for details.

```env

```

### 5. Run Database Migrations
```bash
python manage.py migrate
```

### 6. Create a Superuser
```bash
python manage.py createsuperuser
```

### 7. Launch the Development Server
```bash
python manage.py runserver
```
The application will be accessible locally at `http://127.0.0`.

---

## 🧪 Running Tests

This project utilizes `pytest` (or Django's native unit testing framework) to ensure codebase stability.

To run the test suite, execute:
```bash
python manage.py test
```
