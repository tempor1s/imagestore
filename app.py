from flask import Flask, render_template, request, redirect, url_for, session
from pymongo import MongoClient
import bcrypt
import json
from bson import json_util
from bson.json_util import loads, dumps
from bson.objectid import ObjectId
import os
from dotenv import load_dotenv
load_dotenv()

SECRET_KEY = os.getenv('SECRET_KEY')

# Setup flask
app = Flask(__name__)
app.config['SECRET_KEY'] = SECRET_KEY

# Mongo URI
host = os.environ.get('MONGODB_URI', 'mongodb://localhost:27017/imagestore')

# Setup Mongo
client = MongoClient(host=f"{host}?retryWrites=false")
db = client.get_default_database()
images = db.images
users = db.users


@app.route('/', methods=['GET'])
def index():
    # So that we get no null errors if not logged in
    user = None
    authenticated = None
    user_images = None

    # Check if user is logged in
    if 'user' in session:
        # pull user from local session
        user = session['user']

        # Clean up session code to access user id
        loaded_user = loads(dumps(user))

        # Pull image from user_id
        user_images = images.find({'user_id': loaded_user['user_id']})

    # Render template while passing user and user_images
    return render_template('index.html', user=user, user_images=user_images)


@app.route('/images/new', methods=['POST', 'GET'])
def add_image():
    """Add a new image to a user storage."""
    # Check if user logged in, if not redirect to login
    if 'user' not in session:
        return redirect(url_for('login'))

    # pull user from local session
    user = session['user']
    loaded_user = loads(dumps(user))

    # Only if request is post we insert data, otherwise just render edit html page
    if request.method == 'POST':
        # Data to be put into the database
        image = {
            'title': request.form['title'],
            'url': request.form['url'],
            'user_id': loaded_user['user_id']
        }

        # Get image id after inserting it into db, and pass it into view_image with redirect url for
        image_id = images.insert_one(image).inserted_id
        return redirect(url_for('view_image', image_id=image_id))

    # Render html page with user passed in
    return render_template('add_image.html', user=user)


@app.route('/images/<image_id>/delete', methods=['GET'])
def remove_image(image_id):
    # Check if user logged in, if not redirect to login
    if 'user' not in session:
        return redirect(url_for('login'))

    # pull user from local session
    user = session['user']

    # Delete image from database and then redirect to home page
    images.delete_one({'_id': ObjectId(image_id)})
    return redirect(url_for('index'))


@app.route('/images/<image_id>/edit', methods=['GET', 'POST'])
def edit_image(image_id):
    # Check if user logged in, if not redirect to login
    if 'user' not in session:
        return redirect(url_for('login'))
    
    # pull user from local session
    user = session['user']
    
    # Check if method is post, if it is then send data, otherwise show them the edit image page.
    if request.method == 'POST':
        # Data to update image with
        updated_image = {
            'title': request.form['title'],
            'url': request.form['url']
        }

        # Update image with new data and redirect to view image with user and image_id
        images.update_one({'_id': ObjectId(image_id)}, {'$set': updated_image})
        return redirect(url_for('view_image', image_id=image_id, user=user))

    # Get image to edit and render template
    image = images.find_one({'_id': ObjectId(image_id)})
    return render_template('edit_image.html', image=image)


@app.route('/images/<image_id>', methods=['GET'])
def view_image(image_id):
    # Check if user logged in, if not redirect to login
    if 'user' not in session:
        return redirect(url_for('login'))
    
    # gets user from local session
    user = session['user']

    image = images.find_one({'_id': ObjectId(image_id)})
    return render_template('single_image.html', image=image, user=user)


@app.route('/login', methods=['POST', 'GET'])
def login():
    # Check if user logged in, if so redirect to home page
    if 'user' in session:
        return redirect(url_for('index'))

    # Check if post to login route, if so then try to log user in otherwise render login
    if request.method == 'POST':
        # Find user from database
        login_user = users.find_one({'username': request.form['username']})

        # Only login if user is found in db
        if login_user:
            # Check if db password is same as submitted password
            if bcrypt.hashpw(request.form['password'].encode('utf-8'), login_user['password']) == login_user['password']:

                # Data to be inserted into session
                data = {
                    'username': request.form['username'],
                    'user_id': login_user['_id']
                }

                # Load user into session
                session['user'] = json.loads(json_util.dumps(data))
                return redirect(url_for('index'))

    return render_template('login.html')


@app.route('/register', methods=['GET', 'POST'])
def register():
    # Check if user logged in, if so redirect to home page
    if 'user' in session:
        return redirect(url_for('index'))

    if request.method == 'POST':
        exisiting_user = users.find_one({'username': request.form['username']})

        if exisiting_user is None:
            hashpass = bcrypt.hashpw(
                request.form['password'].encode('utf-8'), bcrypt.gensalt())
            doc_id = users.insert_one(
                {'username': request.form['username'], 'email': request.form['email'], 'password': hashpass}).inserted_id

            # data to be inserted into session
            data = {
                'username': request.form['username'],
                'user_id': ObjectId(doc_id)
            }

            # Load user into session
            session['user'] = json.loads(json_util.dumps(data))

            return redirect(url_for('index'))
            # TODO: Handle username already taken

        return redirect(url_for('index'))

    return render_template('register.html')


@app.route('/logout')
def logout():
    # Clear session to logout and redirect to home page
    session.clear()
    return redirect(url_for('index'))


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=os.environ.get('PORT', 5000))
