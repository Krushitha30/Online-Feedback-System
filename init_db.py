import sqlite3

conn = sqlite3.connect("feedback.db")
cursor = conn.cursor()

# Student table
cursor.execute('''
CREATE TABLE IF NOT EXISTS student (
    student_id INTEGER PRIMARY KEY,
    username TEXT UNIQUE,
    password TEXT
)
''')

# Faculty table
cursor.execute('''
CREATE TABLE IF NOT EXISTS faculty (
    faculty_id INTEGER PRIMARY KEY,
    subject TEXT,
    faculty_name TEXT
)
''')

# Feedback table (Many-to-Many)
cursor.execute('''
CREATE TABLE IF NOT EXISTS feedback (
    feedback_id INTEGER PRIMARY KEY AUTOINCREMENT,
    student_id INTEGER,
    faculty_id INTEGER,
    rating INTEGER,
    comments TEXT,
    UNIQUE(student_id, faculty_id)
)
''')


cursor.execute('''
CREATE TABLE IF NOT EXISTS admin (
    admin_id INTEGER PRIMARY KEY,
    username TEXT UNIQUE,
    password TEXT
)
''')

cursor.execute("INSERT OR IGNORE INTO admin VALUES (1, 'admin', 'admin123')")

# Sample data
cursor.execute("INSERT OR IGNORE INTO student VALUES (1, 'student1', 'pass123')")
cursor.execute("INSERT OR IGNORE INTO student VALUES (2, 'student2', 'pass456')")
cursor.execute("INSERT OR IGNORE INTO student VALUES (3, 'student3', 'pass789')")
cursor.execute("INSERT OR IGNORE INTO student VALUES (4, 'student4', 'pass123')")
cursor.execute("INSERT OR IGNORE INTO faculty VALUES (1, 'DBMS', 'Mr. Rao')")
cursor.execute("INSERT OR IGNORE INTO faculty VALUES (2, 'OS', 'Ms. Anita')")

conn.commit()
conn.close()
print("Database initialized")
