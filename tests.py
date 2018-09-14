from datetime import datetime, timedelta
import unittest
from app import app, db
from app.models import User

from app.forms import EditProfileForm
from app.routes import EditProfileForm

class UserModelCase(unittest.TestCase):
    def setUp(self):
        app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite://'
        db.create_all()

    def tearDown(self):
        db.session.remove()
        db.drop_all()

    def test_password_hashing(self):
        u = User(username='susan')
        u.set_password('cat')
        self.assertFalse(u.check_password('dog'))
        self.assertTrue(u.check_password('cat'))

    def test_avatar(self):
        u = User(username='john', email='john@example.com')
        self.assertEqual(u.avatar(128), ('https://www.gravatar.com/avatar/'
                                         'd4c74594d841139328695756648b6bd6'
                                         '?d=identicon&s=128'))

"""        
#http://flask.pocoo.org/docs/0.12/api/#flask.Flask.test_client
    @app.route('/users/john')
    def test_editprofile(self):
        u = User(username='john', email='john@example.com')
        db.session.add(u)
        db.session.commit()

        resp = json.loads
        data = json.loads(resp.data)
"""


if __name__ == '__main__':
    unittest.main(verbosity=2)
