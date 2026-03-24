# 🛒 EcomWeb (Cartify)

Follow the steps below to run this project locally on your system.

---

## 📥 1. Clone the Repository

```bash
git clone https://github.com/harshtarsariya0106/Ecomweb.git
```

---

## 📂 2. Navigate to the Project Folder

```bash
cd Ecomweb/Cartify
```

---

## 🧪 3. Create and Activate Virtual Environment

```bash
python -m venv env
```

### ▶️ Activate Environment

**Windows:**

```bash
env\Scripts\activate
```

**Mac/Linux:**

```bash
source env/bin/activate
```

---

## 📦 4. Install Dependencies

```bash
pip install -r requirements.txt
```

> ⚠️ If `requirements.txt` is not available, install manually:

```bash
pip install django pillow razorpay
```

---

## 🗄️ 5. Apply Database Migrations

```bash
python manage.py migrate
```

---

## 👤 6. Create Superuser (Admin Access)

```bash
python manage.py createsuperuser
```

* Enter username, email, and password
* Use this to log in to admin panel

---

## ▶️ 7. Run Development Server

```bash
python manage.py runserver
```

---

## 🌐 8. Open in Browser

Main site:

```
http://127.0.0.1:8000/
```

Admin panel:

```
http://127.0.0.1:8000/admin/
```

---

## ⚠️ Common Issues

* **ModuleNotFoundError (django / razorpay / pillow)**
  👉 Install missing package:

```bash
pip install package_name
```

* **Images not loading**
  👉 Check `MEDIA_URL` and `MEDIA_ROOT` in settings

---

## 💡 Recommended

Create `requirements.txt`:

```bash
pip freeze > requirements.txt
```
