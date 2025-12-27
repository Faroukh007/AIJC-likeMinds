import os
import sqlite3
from flask import Flask, render_template, request

app = Flask(__name__)
app.secret_key = "aijc_key_2025"

@app.route('/admin_portal_2025')
def admin_portal():
    # Simple security: check for a password in the URL
    # Access this via: yoursite.com/admin_portal_2025?password=AIJC123
    password = request.args.get('password')
    if password != "AIJC123": # Change "AIJC123" to your secret password
        return "Unauthorized Access", 403

    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM members ORDER BY id DESC')
    members = cursor.fetchall()
    conn.close()
    
    return render_template('admin.html', members=members)

# Database path setup
BASE_DIR = os.path.abspath(os.path.dirname(__file__))
DB_PATH = os.path.join(BASE_DIR, 'database.db')

def init_db():
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS members (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            full_name TEXT, gender TEXT, dob TEXT, phone TEXT,
            email TEXT, address TEXT, state TEXT, lga TEXT,
            ward TEXT, polling_unit TEXT, voter_id TEXT
        )
    ''')
    conn.commit()
    conn.close()

@app.route('/')
def landing():
    return render_template('landing.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        data = (
            request.form.get('full_name'), request.form.get('gender'),
            request.form.get('dob'), request.form.get('phone'),
            request.form.get('email'), request.form.get('address'),
            request.form.get('state'), request.form.get('lga'),
            request.form.get('ward'), request.form.get('polling_unit'),
            request.form.get('voter_id')
        )
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()
        cursor.execute('''INSERT INTO members (full_name, gender, dob, phone, email, 
                          address, state, lga, ward, polling_unit, voter_id) 
                          VALUES (?,?,?,?,?,?,?,?,?,?,?)''', data)
        conn.commit()
        conn.close()
        return render_template('register.html', success=True)
    return render_template('register.html')

if __name__ == '__main__':
    init_db()
    app.run(debug=True)