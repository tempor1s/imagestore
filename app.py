from flask import Flask, render_template, request, redirect, url_for, session
from pymongo import MongoClient
import os
from dotenv import load_dotenv
load_dotenv()

SECRET_KEY = os.getenv('SECRET_KEY')

app = Flask(__name__)
host = os.environ.get('MONGODB_URI', 'mongodb://localhost:27017/imagestore')

client = MongoClient(host=host)
db = client.get_default_database()
users = db.users
images = db.images


@app.route('/')
def index():
    return render_template('index.html', msg='Hello, world!')


if __name__ == '__main__':
    app.secret_key = SECRET_KEY
    app.run(debug=True, host='0.0.0.0', port=os.environ.get('PORT', 5000))