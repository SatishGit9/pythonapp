from flask import Flask, request, render_template, redirect, url_for
import sqlite3
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Create a new Flask web application instance
app = Flask(__name__)
app.config['SECRET_KEY'] = os.getenv('SECRET_KEY', 'my_secret_key')  # Make sure you have a SECRET_KEY for Flask session

# Specify the path to the SQLite database file
DATABASE = os.path.join(os.path.dirname(__file__), 'data.db')

# Function to initialize the database and create the necessary table if not already present
def init_db():
    with sqlite3.connect(DATABASE) as conn:
        conn.execute('''
            CREATE TABLE IF NOT EXISTS users (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                first_name TEXT,
                last_name TEXT,
                email TEXT UNIQUE,
                phone_number TEXT UNIQUE,
                company TEXT,
                job_role TEXT
            )
        ''')
        conn.commit()

# Define the route for the root URL, supporting both GET and POST requests
@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        # Extract data from form fields sent with the POST request
        first_name = request.form['first_name']
        last_name = request.form['last_name']
        email = request.form['email']
        phone_number = request.form['phone_number']
        company = request.form['company']
        job_role = request.form['job_role']

        # Connect to the SQLite database and try inserting the new user data
        try:
            with sqlite3.connect(DATABASE) as conn:
                conn.execute('INSERT INTO users (first_name, last_name, email, phone_number, company, job_role) VALUES (?, ?, ?, ?, ?, ?)',
                             (first_name, last_name, email, phone_number, company, job_role))
                conn.commit()
            # Redirect with success=true to display the success dialog
            return redirect(url_for('index', success='true'))
        except sqlite3.IntegrityError as e:
            # Determine the error type based on the exception message
            if 'email' in str(e):
                error_message = "This email address is already registered. Please use a different email."
            elif 'phone_number' in str(e):
                error_message = "This phone number is already registered. Please use a different phone number."
            else:
                error_message = "An unknown error occurred. Please try again."

            # Redirect back with the error message and form data
            return redirect(url_for('index', error=error_message, first_name=first_name, last_name=last_name, email=email, phone_number=phone_number, company=company, job_role=job_role))

    # Render the HTML form page if the request method is GET
    return render_template('index.html')
