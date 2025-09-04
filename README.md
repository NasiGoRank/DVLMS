# Damn Vulnerable LMS App

This project is a **Flask-based e-learning lab** that is intentionally made vulnerable for **web security practice**, such as:

  - Broken Access Control (BAC)
  - Insecure Direct Object Reference (IDOR)
  - Privilege Escalation
  - Others

It can be used for web security training and learning Python/Flask.

-----

## 🗂 Project Structure

```
Vuln Lab/
│── app.py
│── init_db.py
│── requirements.txt
│── Dockerfile
│── docker-compose.yml
│── .gitignore
│── templates/
│   ├── base.html
│   ├── login.html
│   ├── dashboard.html
│   └── ...
│── static/
│   └── css/
│       ├── static.css
│       └── theme.css
│── database.db
```

-----

## ⚙️ Local Installation

1.  Clone the repo:

    ```bash
    git clone https://github.com/NasiGoRank/DVLMS.git
    cd DVLMS
    ```

2.  Create a virtual environment (optional but recommended):

    ```bash
    python -m venv venv
    source venv/bin/activate      # Linux / Mac
    venv\Scripts\activate         # Windows
    ```

3.  Install dependencies:

    ```bash
    pip install -r requirements.txt
    ```

4.  Run the application:

    ```bash
    python app.py
    ```

5.  Access the web at:

    ```
    http://localhost:5000
    ```

-----

## 🐳 Docker

### Build the image and run the container:

```bash
docker build -t dvlms .
docker run -d -p 5050:5000 dvlms
```

Access at:

```
http://localhost:5050
```

-----

## 🐳 Docker Compose

If you use Docker Compose, it's just one command to build & run:

```bash
docker-compose up -d
```

Access at:

```
http://localhost:5050
```

> If port 5050 is already in use on the host, change `docker-compose.yml`:

```yaml
ports:
  - "5051:5000"   # Host:Container
```

-----

## 👤 Default Accounts

| Username | Password   | Role    |
| -------- | ---------- | ------- |
| admin    | admin123   | admin   |
| teacher1 | teach123   | teacher |
| student1 | password1  | student |
| student2 | password2  | student |

> The **Reset Database** button on the login page will restore the accounts to these defaults.

-----

## ⚠️ Warning

  * This application is **intentionally vulnerable**; do not use it in a production environment.
  * For **web security training & educational purposes** only.
  * The SQLite database is **local**; use a volume in Docker for persistent data.

-----

## 🔧 Features

  * User Login/Registration
  * Role-based access: student, teacher, admin
  * Dashboard according to role
  * Admin: create/delete users, reset database
  * Simple e-learning course
  * Toggle theme (dark/light)
