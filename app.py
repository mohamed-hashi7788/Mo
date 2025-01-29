from flask import Flask, request, jsonify, send_from_directory
import sqlite3
import os

app = Flask(__name__)

# Database initialization
def init_db():
    with sqlite3.connect('data.db') as conn:
        cursor = conn.cursor()
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS amounts (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                amount REAL
            )
        ''')
        conn.commit()

# Serve the frontend HTML file
@app.route('/')
def index():
    return send_from_directory('.', 'index.html')  # Serve index.html from the root folder

@app.route('/add', methods=['POST'])
def add_amount():
    amount = request.json.get('amount')
    if amount is not None:
        with sqlite3.connect('data.db') as conn:
            cursor = conn.cursor()
            cursor.execute('INSERT INTO amounts (amount) VALUES (?)', (amount,))
            conn.commit()
        return jsonify({"message": "Amount saved successfully!"}), 201
    return jsonify({"message": "Invalid amount!"}), 400

@app.route('/data', methods=['GET'])
def get_data():
    with sqlite3.connect('data.db') as conn:
        cursor = conn.cursor()
        cursor.execute('SELECT amount FROM amounts')
        data = cursor.fetchall()
    return jsonify({"amounts": [row[0] for row in data]})

if __name__ == '__main__':
    init_db()
    app.run(debug=True)
