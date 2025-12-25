from flask import Flask, render_template, request, redirect, url_for, flash
import sqlite3

app = Flask(__name__)
app.secret_key = "aijc_secret_key"

# Database Initialization
def init_db():
    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS members (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            full_name TEXT NOT NULL,
            gender TEXT,
            dob TEXT,
            phone TEXT,
            email TEXT,
            address TEXT,
            state TEXT,
            lga TEXT,
            ward TEXT,
            polling_unit TEXT,
            voter_id TEXT
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
        # Collect form data
        data = (
            request.form['full_name'], request.form['gender'], request.form['dob'],
            request.form['phone'], request.form['email'], request.form['address'],
            request.form['state'], request.form['lga'], request.form['ward'],
            request.form['polling_unit'], request.form['voter_id']
        )
        
        # Insert into Database
        conn = sqlite3.connect('database.db')
        cursor = conn.cursor()
        cursor.execute('''INSERT INTO members (full_name, gender, dob, phone, email, 
                          address, state, lga, ward, polling_unit, voter_id) 
                          VALUES (?,?,?,?,?,?,?,?,?,?,?)''', data)
        conn.commit()
        conn.close()
        
        return "<h1>Registration Successful! Thank you for joining the movement.</h1>"
    
    return render_template('register.html')

if __name__ == '__main__':
    init_db()
    app.run(debug=True)