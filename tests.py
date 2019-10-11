from unittest import TestCase, main, mock
from bson.objectid import ObjectId
from app import app
import flask
import json
from bson import json_util
from bson.json_util import dumps, loads

mock_image_id = ObjectId('5d9a3901243d034fd166e654')
mock_user_id = ObjectId('5d99aa61e55dd66659c60cca')

mock_image = {
    'title': 'Amazing Photo',
    'url': 'https://i.imgur.com/D3PlpYi.png',
    'user_id': mock_user_id
}

user = {
    'username': 'test',
    'email': 'test@test.com',
    'password': b'JDJiJDEyJGl2LlJHR2toaG9xekt4LnZ5U0hSZS5LQU11SnQvU0ZDc1pFS1N4U0FVSHg1UXpFUUVGQTl1'
}

class ImageStoreTest(TestCase):
    """Route tests."""
    def setUp(self):
        """Run before every test."""
        # Set up flask test client
        self.client = app.test_client()

        # Show flask errors that happen during tests
        app.config['TESTING'] = True

    
    def test_index(self):
        """Test the homepage of image store"""
        result = self.client.get('/')
        self.assertIn(b'Can\'t display images because you are not logged in. Please <a href="/login">login</a> to add photos!</h2>', result.data)
        self.assertEqual(result.status, '200 OK')


    def test_add_image(self):
        """Test adding an image route"""
        result = self.client.get('/images/new')
        self.assertEqual(result.status, '302 FOUND')

    # @mock.patch('pymongo.collection.Collection.delete_one')
    # def test_remove_image(self, mock_delete):
    #     """Test removing an image route"""
    #     form_data = {'_method': 'DELETE'}
    #     with app.test_client() as c:
    #         with c.session_transaction() as session:
    #             data = {
    #                 'username': user['username'],
    #                 'user_id': mock_user_id
    #             }

    #             session['user'] = json.loads(json_util.dumps(data))
            
    #         c.get('/')
    #         print(flask.session['user'])

    #     result = self.client.post(f'/images/{mock_image_id}/delete', data=form_data)
    #     self.assertEqual(result.status, '302 FOUND')
    #     mock_delete.assert_called_with({'_id': sample_playlist_id})


    def test_edit_image(self):
        """Test edit image route"""
        result = self.client.get(f'/images/{mock_image_id}/edit')
        self.assertEqual(result.status, '302 FOUND')


    def test_view_image(self):
        """Test view single image route"""
        result = self.client.get(f'/images/{mock_image_id}/delete')
        self.assertEqual(result.status, '302 FOUND')


    def test_login(self):
        """Test login route"""
        result = self.client.get('/login')
        self.assertEqual(result.status, '200 OK')


    def test_register(self):
        """Test register route"""
        result = self.client.get('/register')
        self.assertEqual(result.status, '200 OK')


    def test_logout(self):
        """Test logout route"""
        result = self.client.get('/logout')
        self.assertEqual(result.status, '302 FOUND')


if __name__ == '__main__':
    main()