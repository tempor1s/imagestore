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

app = Flask(__name__)
app.config['SECRET_KEY'] = SECRET_KEY

host = os.environ.get('MONGODB_URI', 'mongodb://localhost:27017/imagestore')

client = MongoClient(host=f"{host}?retryWrites=false")
db = client.get_default_database()
images = db.images
users = db.users

# TODO: Implement file upload image hosting? - could be for intensive
# TODO: Implement static stying of photo on non-single-view page.

@app.route('/', methods=['GET'])
def index():
    user = None
    authenticated = None
    user_images = None
    if 'user' in session:    
        # Hacky thing to get this to work lmao
        user = session['user']
        # dumped_user = dumps(user)
        loaded_user = loads(dumps(user))

        user_images = images.find({'user_id': loaded_user['user_id']})

    return render_template('index.html', user=user, user_images=user_images)


@app.route('/images/new', methods=['POST', 'GET'])
def add_image():
    """Add a new image to a user storage."""
    if 'user' not in session:
        return redirect(url_for('login'))

    user = session['user']
    # dumped_user = dumps(user)
    loaded_user = loads(dumps(user))

    if request.method == 'POST':
        image = {
            'title': request.form['title'],
            'url': request.form['url'],
            'user_id': loaded_user['user_id']
        }

        image_id = images.insert_one(image).inserted_id
        return redirect(url_for('view_image', image_id=image_id))

    return render_template('add_image.html', user=user)


@app.route('/images/<image_id>/delete', methods=['GET'])
def remove_image(image_id):
    if 'user' not in session:
        return redirect(url_for('login'))

    user = session['user']

    images.delete_one({'_id': ObjectId(image_id)})
    return redirect(url_for('index'))


@app.route('/images/<image_id>/edit', methods=['GET', 'POST'])
def edit_image(image_id):
    if 'user' not in session:
        return redirect(url_for('login'))
    
    user = session['user']
        
    if request.method == 'POST':
        updated_image = {
            'title': request.form['title'],
            'url': request.form['url']
        }

        images.update_one({'_id': ObjectId(image_id)}, {'$set': updated_image})
        
        return redirect(url_for('view_image', image_id=image_id, user=user))

    image = images.find_one({'_id': ObjectId(image_id)})
    return render_template('edit_image.html', image=image)


@app.route('/images/<image_id>', methods=['GET'])
def view_image(image_id):
    if 'user' not in session:
        return redirect(url_for('login'))
    
    user = session['user']
    # TODO: Improve this
    image = images.find_one({'_id': ObjectId(image_id)})
    return render_template('single_image.html', image=image, user=user)


@app.route('/login', methods=['POST', 'GET'])
def login():
    if 'user' in session:
        return redirect(url_for('index'))

    if request.method == 'POST':
        login_user = users.find_one({'username': request.form['username']})

        if login_user:
            if bcrypt.hashpw(request.form['password'].encode('utf-8'), login_user['password']) == login_user['password']:
                data = {
                    'username': request.form['username'],
                    'user_id': login_user['_id']
                }

                session['user'] = json.loads(json_util.dumps(data))
                return redirect(url_for('index'))

    return render_template('login.html')


@app.route('/register', methods=['GET', 'POST'])
def register():
    if 'user' in session:
        return redirect(url_for('index'))

    if request.method == 'POST':
        exisiting_user = users.find_one({'username': request.form['username']})

        if exisiting_user is None:
            hashpass = bcrypt.hashpw(
                request.form['password'].encode('utf-8'), bcrypt.gensalt())
            doc_id = users.insert_one(
                {'username': request.form['username'], 'email': request.form['email'], 'password': hashpass}).inserted_id

            data = {
                'username': request.form['username'],
                'user_id': ObjectId(doc_id)
            }
            session['user'] = json.loads(json_util.dumps(data))

            return redirect(url_for('index'))
            # TODO: Handle username already taken

        return redirect(url_for('index'))

    return render_template('register.html')


@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('index'))


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=os.environ.get('PORT', 5000))
