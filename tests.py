from unittest import TestCase, main, mock
from bson.objectid import ObjectId
from app import app

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
        pass


    def test_add_image(self):
        """Test adding an image route"""
        pass


    def test_remove_image(self):
        """Test removing an image route"""
        pass


    def test_edit_image(self):
        """Test edit image route"""
        pass


    def test_view_image(self):
        """Test view single image route"""
        pass


    def test_login(self):
        """Test login route"""
        pass


    def test_register(self):
        """Test register route"""


    def test_logout(self):
        """Test logout route"""
        pass


if __name__ == '__main__':
    main()