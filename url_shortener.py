import string
import random
import sqlite3
from flask import Flask, request, redirect, jsonify, render_template
import threading
import webbrowser


def short_url_generator():
    characters = string.ascii_letters + string.digits
    short_url = ''.join(random.choice(characters) for _ in range(6))
    return short_url


def create_connection():
    connekt = sqlite3.connect('urls.db')
    return connekt


def create_table():
    connekt = create_connection()
    connekt_cursor = connekt.cursor()
    connekt_cursor.execute('''CREATE TABLE IF NOT EXISTS urls (short_url TEXT, long_url TEXT)''')
    connekt.commit()
    connekt.close()


app = Flask(__name__)


@app.route('/api/shorten', methods=['POST'])
def shorten_url_api():
    create_table()
    long_url = request.json['url']
    short_url = short_url_generator()

    connekt = create_connection()
    connekt_cursor = connekt.cursor()
    connekt_cursor.execute("INSERT INTO urls (short_url, long_url) VALUES (?, ?)", (short_url, long_url))
    connekt.commit()
    connekt.close()

    complete_short_url = f'http://127.0.0.1:5000/{short_url}'       # Replace with domain/IP of web server
    return jsonify({'short_url': complete_short_url})


@app.route('/<short_url>')
def redirect_url(short_url):
    connekt = create_connection()
    connekt_cursor = connekt.cursor()
    connekt_cursor.execute("SELECT long_url FROM urls WHERE short_url = ?", (short_url,))
    long_url = connekt_cursor.fetchone()

    if long_url:
        return redirect(long_url[0])
    else:
        return "URL not found.", 404


@app.route('/')
def index():
    return render_template('index.html')


def run_flask_app():
    app.run()


flask_thread = threading.Thread(target=run_flask_app)
flask_thread.daemon = True
flask_thread.start()

stop_event = threading.Event()
try:
    stop_event.wait()
except KeyboardInterrupt:
    pass

webbrowser.open_new('http://127.0.0.1:5000/')



