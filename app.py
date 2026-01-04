from flask import Flask, render_template, request, redirect, session
import sqlite3

app = Flask(__name__)
app.secret_key = 'secret_key'


def get_db():
    return sqlite3.connect('feedback.db')


@app.route('/', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        conn = get_db()
        cur = conn.cursor()
        cur.execute("SELECT student_id FROM student WHERE username=? AND password=?",
                    (username, password))
        user = cur.fetchone()
        conn.close()

        if user:
            session['student_id'] = user[0]
            return redirect('/feedback')
        return "Invalid credentials"

    return render_template('login.html')


@app.route('/feedback', methods=['GET', 'POST'])
def feedback():
    if 'student_id' not in session:
        return redirect('/')

    student_id = session['student_id']
    conn = get_db()
    cur = conn.cursor()

    message = None

    if request.method == 'POST':
        faculty_id = request.form['faculty_id']
        rating = request.form['rating']
        comments = request.form['comments']

        # Check if feedback already exists
        cur.execute(
            "SELECT * FROM feedback WHERE student_id=? AND faculty_id=?",
            (student_id, faculty_id)
        )
        exists = cur.fetchone()

        if exists:
            message = "You have already submitted feedback for this subject."
        else:
            cur.execute(
                "INSERT INTO feedback (student_id, faculty_id, rating, comments) VALUES (?, ?, ?, ?)",
                (student_id, faculty_id, rating, comments)
            )
            conn.commit()
            message = "Feedback submitted successfully."

    # Get faculty list
    cur.execute("SELECT * FROM faculty")
    faculty = cur.fetchall()

    # Get faculties already reviewed by this student
    cur.execute(
        "SELECT faculty_id FROM feedback WHERE student_id=?",
        (student_id,)
    )
    submitted_faculty = [row[0] for row in cur.fetchall()]

    conn.close()

    return render_template(
        'feedback.html',
        faculty=faculty,
        submitted_faculty=submitted_faculty,
        message=message
    )


@app.route('/admin')
def admin():
    # 🔐 Admin session check
    if 'admin' not in session:
        return redirect('/admin_login')

    conn = get_db()
    cur = conn.cursor()

    cur.execute("""
    SELECT s.username, f.subject, f.faculty_name, fb.rating, fb.comments
    FROM feedback fb
    JOIN student s ON fb.student_id = s.student_id
    JOIN faculty f ON fb.faculty_id = f.faculty_id
    """)

    data = cur.fetchall()
    conn.close()

    return render_template('admin.html', data=data)


@app.route('/admin_login', methods=['GET', 'POST'])
def admin_login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        conn = get_db()
        cur = conn.cursor()
        cur.execute("SELECT * FROM admin WHERE username=? AND password=?",
                    (username, password))
        admin = cur.fetchone()
        conn.close()

        if admin:
            session['admin'] = True
            return redirect('/admin')
        return "Invalid admin credentials"

    return render_template('admin_login.html')


@app.route('/logout')
def logout():
    session.clear()
    return redirect('/')


if __name__ == '__main__':
    app.run(debug=True)