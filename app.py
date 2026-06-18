# ============================================
# FILE: app.py
# ============================================
from flask import Flask, render_template, request, redirect, url_for, flash
import os
import json
from datetime import datetime

app = Flask(__name__)
app.secret_key = 'your-secret-key-here-change-in-production'  # Required for flashing messages

# Path to store messages (simple JSON file)
MESSAGES_FILE = 'messages.json'

# Ensure the messages file exists
if not os.path.exists(MESSAGES_FILE):
    with open(MESSAGES_FILE, 'w') as f:
        json.dump([], f)

def load_messages():
    """Load messages from JSON file."""
    try:
        with open(MESSAGES_FILE, 'r') as f:
            return json.load(f)
    except (json.JSONDecodeError, FileNotFoundError):
        return []

def save_messages(messages):
    """Save messages to JSON file."""
    with open(MESSAGES_FILE, 'w') as f:
        json.dump(messages, f, indent=2)

@app.route('/')
def index():
    """Homepage – shows portfolio and about section."""
    return render_template('index.html')

@app.route('/contact', methods=['GET', 'POST'])
def contact():
    """Contact page with a form to send a message."""
    if request.method == 'POST':
        name = request.form.get('name', '').strip()
        email = request.form.get('email', '').strip()
        message = request.form.get('message', '').strip()

        if not name or not email or not message:
            flash('All fields are required.', 'danger')
        else:
            # Save the message
            messages = load_messages()
            messages.append({
                'name': name,
                'email': email,
                'message': message,
                'timestamp': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            })
            save_messages(messages)
            flash('Your message has been sent! I will get back to you soon.', 'success')
            return redirect(url_for('contact'))

    return render_template('contact.html')

@app.route('/messages')
def view_messages():
    """Admin-like page to view all messages (for demonstration)."""
    messages = load_messages()
    return render_template('messages.html', messages=messages)

if __name__ == '__main__':
    # Run the app in debug mode for development
    app.run(debug=True, host='0.0.0.0', port=5000)
