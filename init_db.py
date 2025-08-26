import sqlite3

# ---------------- DB setup ----------------
DB_NAME = "database.db"
conn = sqlite3.connect(DB_NAME)
cur = conn.cursor()

# Hapus tabel lama (kalau ada)
cur.execute("DROP TABLE IF EXISTS users")
cur.execute("DROP TABLE IF EXISTS courses")
cur.execute("DROP TABLE IF EXISTS grades")
cur.execute("DROP TABLE IF EXISTS tasks")
cur.execute("DROP TABLE IF EXISTS submissions")

# ---------------- Tabel users ----------------
cur.execute("""
CREATE TABLE users (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    username TEXT,
    password TEXT,
    role TEXT
)
""")

# ---------------- Tabel courses ----------------
cur.execute("""
CREATE TABLE courses (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT,
    description TEXT
)
""")

# ---------------- Tabel grades ----------------
cur.execute("""
CREATE TABLE grades (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    student_id INTEGER,
    course_id INTEGER,
    grade TEXT,
    FOREIGN KEY(student_id) REFERENCES users(id),
    FOREIGN KEY(course_id) REFERENCES courses(id)
)
""")

# ---------------- Seed Users ----------------
cur.execute("INSERT INTO users (username, password, role) VALUES ('admin', 'admin123', 'admin')")
cur.execute("INSERT INTO users (username, password, role) VALUES ('student1', 'password1', 'student')")
cur.execute("INSERT INTO users (username, password, role) VALUES ('student2', 'password2', 'student')")
cur.execute("INSERT INTO users (username, password, role) VALUES ('teacher1', 'teach123', 'teacher')")

# ---------------- Seed Courses ----------------
cur.execute("INSERT INTO courses (name, description) VALUES ('Python Basics', 'Belajar Python dari nol')")
cur.execute("INSERT INTO courses (name, description) VALUES ('Web Security', 'Belajar keamanan web')")

# ---------------- Seed Grades ----------------
cur.execute("INSERT INTO grades (student_id, course_id, grade) VALUES (2,1,'A')")
cur.execute("INSERT INTO grades (student_id, course_id, grade) VALUES (2,2,'B')")
cur.execute("INSERT INTO grades (student_id, course_id, grade) VALUES (3,1,'B')")
cur.execute("INSERT INTO grades (student_id, course_id, grade) VALUES (3,2,'C')")

conn.commit()
conn.close()
print("Database initialized successfully.")
