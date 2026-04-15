from flask import Flask, render_template, request, redirect, url_for
import sqlite3
import os

app = Flask(__name__)

# -------- DATABASE PATH FIX --------
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
db_path = os.path.join(BASE_DIR, "database.db")

# -------- DATABASE INIT --------
def init_db():
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS students (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT,
        usn TEXT,
        password TEXT,
        lang1 INTEGER,
        lang2 INTEGER,
        lang3 INTEGER,
        core1 INTEGER,
        core2 INTEGER,
        core3 INTEGER
    )
    """)

    conn.commit()
    conn.close()

# -------- HOME --------
@app.route('/')
def home():
    return render_template('index.html')

# -------- ADMIN LOGIN --------
@app.route('/admin', methods=['GET', 'POST'])
def admin():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        if username == "admin" and password == "admin123":
            return redirect(url_for('admin_dashboard'))
        else:
            return "Invalid Admin Login ❌"

    return render_template('admin_login.html')

# -------- ADMIN DASHBOARD --------
@app.route('/admin/dashboard')
def admin_dashboard():
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM students")
    students = cursor.fetchall()

    conn.close()

    return render_template('admin_dashboard.html', students=students)

# -------- ADD STUDENT --------
@app.route('/add_student', methods=['POST'])
def add_student():
    name = request.form['name']
    usn = request.form['usn']
    password = request.form['password']

    lang1 = request.form['lang1']
    lang2 = request.form['lang2']
    lang3 = request.form['lang3']

    core1 = request.form['core1']
    core2 = request.form['core2']
    core3 = request.form['core3']

    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    cursor.execute("""
    INSERT INTO students (name, usn, password, lang1, lang2, lang3, core1, core2, core3)
    VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
    """, (name, usn, password, lang1, lang2, lang3, core1, core2, core3))

    conn.commit()
    conn.close()

    return redirect(url_for('admin_dashboard'))

# -------- DELETE STUDENT --------
@app.route('/delete/<int:id>')
def delete_student(id):
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    cursor.execute("DELETE FROM students WHERE id=?", (id,))

    conn.commit()
    conn.close()

    return redirect(url_for('admin_dashboard'))

# -------- STUDENT LOGIN --------
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        usn = request.form['usn']
        password = request.form['password']

        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()

        cursor.execute("SELECT * FROM students WHERE usn=? AND password=?", (usn, password))
        student = cursor.fetchone()

        conn.close()

        if student:
            return render_template('result.html', student=student)
        else:
            return "Invalid USN or Password ❌"

    return render_template('login.html')

# -------- RUN --------
if __name__ == '__main__':
    init_db()
    app.run()