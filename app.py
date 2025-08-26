from flask import Flask, render_template, request, redirect, session, flash, url_for
import sqlite3

# ---------------- DB Connection ----------------
def get_db_connection():
    conn = sqlite3.connect('database.db')
    conn.row_factory = sqlite3.Row
    return conn

def get_db():
    conn = sqlite3.connect('database.db')
    conn.row_factory = sqlite3.Row
    return conn

# ---------------- Flask App ----------------
app = Flask(__name__)
app.secret_key = "supersecretkey"

# ---------------- Home ----------------
@app.route("/")
def index():
    return render_template("index.html")

# ---------------- Register ----------------
@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]
        role = "student"

        db = get_db()
        db.execute(
            "INSERT INTO users (username,password,role) VALUES (?,?,?)",
            (username, password, role)
        )
        db.commit()
        flash("Registration successful. Please login.", "success")
        return redirect("/login")
    return render_template("register.html")

# ---------------- Reset DB ----------------
@app.route("/reset_db", methods=["POST"])
def reset_db():
    conn = get_db_connection()
    cur = conn.cursor()

    # Hapus semua user
    cur.execute("DELETE FROM users")
    # Reset autoincrement ID
    cur.execute("DELETE FROM sqlite_sequence WHERE name='users'")
    
    # Tambah akun default lagi
    cur.execute("INSERT INTO users (username, password, role) VALUES (?, ?, ?)", 
                ("admin", "admin123", "admin"))
    cur.execute("INSERT INTO users (username, password, role) VALUES (?, ?, ?)", 
                ("teacher1", "teach123", "teacher"))
    cur.execute("INSERT INTO users (username, password, role) VALUES (?, ?, ?)", 
                ("student1", "password1", "student"))
    cur.execute("INSERT INTO users (username, password, role) VALUES (?, ?, ?)", 
                ("student2", "password2", "student"))
    
    conn.commit()
    conn.close()

    flash("Database berhasil direset ke default!", "info")
    return redirect(url_for("login"))

# ---------------- Login ----------------
@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]

        db = get_db()
        user = db.execute(
            "SELECT * FROM users WHERE username=? AND password=?",
            (username, password)
        ).fetchone()

        if user:
            session["user_id"] = user["id"]
            session["username"] = user["username"]
            session["role"] = user["role"]
            flash(f"Welcome {user['username']}!", "success")
            return redirect("/dashboard")
        else:
            flash("Invalid username or password", "danger")
    return render_template("login.html")

# ---------------- Dashboard ----------------
@app.route("/dashboard")
def dashboard():
    if "user_id" not in session:
        return redirect("/login")

    return render_template(
        "dashboard.html",
        username=session.get("username"),
        role=session.get("role"),
        user_id=session.get("user_id")
    )

# ---------------- Courses ----------------
@app.route("/courses")
def courses():
    if "user_id" not in session:
        return redirect("/login")

    db = get_db()
    courses = db.execute("SELECT * FROM courses").fetchall()
    return render_template("courses.html", courses=courses)

# ---------------- Grades ----------------
@app.route("/grades")
def grades():
    if "user_id" not in session:
        return redirect("/login")

    student_id = request.args.get("student_id")
    db = get_db()
    grades = db.execute("""
        SELECT g.id, g.grade, c.name as course_name
        FROM grades g
        JOIN courses c ON g.course_id = c.id
        WHERE g.student_id=?
    """, (student_id,)).fetchall()
    return render_template("grades.html", grades=grades)

# ---------------- Profile ----------------
@app.route("/profile")
def profile():
    user_id = request.args.get("id")
    db = get_db()
    user = db.execute("SELECT * FROM users WHERE id=?", (user_id,)).fetchone()
    if not user:
        return "User not found"
    return render_template("profile.html", user=user)

# ---------------- Edit Profile ----------------
@app.route("/edit_profile", methods=["GET", "POST"])
def edit_profile():
    if "user_id" not in session:
        return redirect("/login")

    db = get_db()

    if request.method == "GET":
        user_id = request.args.get("id")
        user = db.execute("SELECT * FROM users WHERE id=?", (user_id,)).fetchone()
        if not user:
            return "User not found"
        return render_template("edit_profile.html", user=user)

    # POST → simpan perubahan
    user_id = request.form.get("id")
    username = request.form.get("username")
    password = request.form.get("password")
    role = request.form.get("role")

    db.execute(
        "UPDATE users SET username=?, password=?, role=? WHERE id=?",
        (username, password, role, user_id)
    )
    db.commit()

    # Update session
    session["username"] = username
    session["role"] = role

    return redirect(f"/profile?id={user_id}")

# ---------------- Admin Panel ----------------
@app.route("/admin")
def admin():
    db = get_db()
    users = db.execute("SELECT * FROM users").fetchall()
    return render_template("admin.html", users=users)

# ---------------- Delete User ----------------
@app.route('/delete_user', methods=['POST'])
def delete_user():
    if 'role' not in session or session['role'] != 'admin':
        flash("Access denied: only admin can delete users.", "danger")
        return redirect('/admin')

    user_id = request.form.get('id')
    if not user_id:
        flash("No user specified.", "warning")
        return redirect('/admin')

    # Tidak boleh hapus diri sendiri
    if str(session['user_id']) == user_id:
        flash("Cannot delete yourself!", "warning")
        return redirect('/admin')

    conn = get_db_connection()
    conn.execute('DELETE FROM users WHERE id = ?', (user_id,))
    conn.commit()
    conn.close()

    flash("User deleted successfully.", "success")
    return redirect('/admin')

# ---------------- Create User ----------------
@app.route('/create_user', methods=['GET', 'POST'])
def create_user():
    if 'role' not in session or session['role'] != 'admin':
        flash("Access denied: only admin can create users.", "danger")
        return redirect('/admin')

    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        role = request.form.get('role')

        if not username or not password or not role:
            flash("All fields are required.", "warning")
            return redirect('/create_user')

        conn = get_db_connection()
        conn.execute('INSERT INTO users (username, password, role) VALUES (?, ?, ?)',
                     (username, password, role))
        conn.commit()
        conn.close()

        flash(f"User '{username}' created successfully.", "success")
        return redirect('/admin')

    return render_template('create_user.html')

# ---------------- Teacher Panel ----------------
@app.route("/teacher_panel")
def teacher_panel():
    if "user_id" not in session:
        return redirect("/login")

    db = get_db()
    students = db.execute("SELECT * FROM users WHERE role='student'").fetchall()
    return render_template("teacher_panel.html", students=students)

# ---------------- Logout ----------------
@app.route("/logout")
def logout():
    session.clear()
    flash("Logged out successfully.", "success")
    return redirect("/")

# ---------------- Main ----------------
if __name__ == "__main__":
    app.run(debug=True)
