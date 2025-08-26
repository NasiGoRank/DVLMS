Oke, aku buatkan contoh **README.md** yang rapi untuk project Flask lab kamu, lengkap dengan penjelasan, cara install, Docker, dan Docker Compose.

---

```markdown
# Damn Vulnerable LMS App

Project ini adalah **lab e-learning berbasis Flask** yang sengaja dibuat rentan untuk **praktik keamanan web** seperti:  
- Broken Access Control (BAC)  
- Insecure Direct Object Reference (IDOR)  
- Privilege Escalation  
- Lainnya  

Dapat digunakan untuk latihan keamanan web dan pembelajaran Python/Flask.

---

## 🗂 Struktur Project

```

Vuln Lab/
│── app.py
│── init\_db.py
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
│── database.db  (tidak di-git)

````

---

## ⚙️ Instalasi Lokal

1. Clone repo:

```bash
git clone https://github.com/NasiGoRank/Damn-Vulnerable-LMS-App.git
cd Damn-Vulnerable-LMS-App
````

2. Buat virtual environment (opsional tapi disarankan):

```bash
python -m venv venv
source venv/bin/activate      # Linux / Mac
venv\Scripts\activate         # Windows
```

3. Install dependencies:

```bash
pip install -r requirements.txt
```

4. Jalankan aplikasi:

```bash
python app.py
```

5. Akses web di:

```
http://localhost:5050
```

---

## 🐳 Docker

### Build image dan run container:

```bash
docker build -t damnvulnerablelmsapp_web .
docker run -d -p 5050:5000 damnvulnerablelmsapp_web
```

Akses di:

```
http://localhost:5050
```

---

## 🐳 Docker Compose

Kalau pakai Docker Compose, cukup 1 perintah untuk build & run:

```bash
docker-compose up -d
```

Akses di:

```
http://localhost:5050
```

> Jika port 5050 di host sudah kepakai, ubah `docker-compose.yml`:

```yaml
ports:
  - "5051:5000"   # Host:Container
```

---

## 👤 Akun Default

| Username  | Password   | Role    |
| --------  | ---------- | ------- |
| admin     | admin123   | admin   |
| teacher1  | teach123   | teacher |
| student1  | password1  | student |
| student2  | password2  | student |

> Tombol **Reset Database** di login akan mengembalikan akun ke default ini.

---

## ⚠️ Peringatan

* Aplikasi ini **sengaja rentan**, jangan dipakai di lingkungan production.
* Hanya untuk **latihan & edukasi keamanan web**.
* Database SQLite bersifat **lokal**, gunakan volume di Docker untuk persistent data.

---

## 🔧 Fitur

* Login/Register user
* Role-based access: student, teacher, admin
* Dashboard sesuai role
* Admin: create/delete user, reset database
* E-learning course sederhana
* Toggle theme (dark/light)

---