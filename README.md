## Installation & Setup

Follow the steps below to run the project locally.

###  1. Clone the Repository

git clone https://github.com/harshtarsariya0106/Ecomweb.git

### 2. Navigate to the Project Folder

cd cartify

### 3. Create and Activate a Virtual Environment

python -m venv env
### On Windows
env\Scripts\activate
### On Mac/Linux
source env/bin/activate

### 4️. Install Dependencies

pip install -r requirements.txt

### 5️. Apply Database Migrations

python manage.py migrate

### 6️. Create a Superuser (for Admin Access)

python manage.py createsuperuser

-> Enter a username, email, and password<br>
-> This lets you log into Django Admin

### 7. Run the Development Server

python manage.py runserver

### 8️. Open in Browser

Go to:
http://127.0.0.1:8000/
