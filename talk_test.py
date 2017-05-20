import os
import talk
import unittest
import tempfile

class TalkTestCase(unittest.TestCase):
    def setUp(self):
        self.db_fd, talk.app.config['DATABASE'] = tempfile.mkstemp()
        talk.app.config['TESTING'] = True
        self.app = talk.app.test_client()
        self.testuser = 'eszter'
        self.testpassword = 'secret'
        with talk.app.app_context():
            talk.init_db()

    def tearDown(self):
        os.close(self.db_fd)
        os.unlink(talk.app.config['DATABASE'])

    def login(self, username, password):
        return self.app.post('/login', data=dict(
            username=username,
            password=password
        ), follow_redirects=True)

    def logout(self):
        return self.app.get('/logout', follow_redirects=True)

    def test_login_logout(self):
        rv = self.login(self.testuser, self.testpassword)
        self.assertIn('Welcome', rv.data)
        rv = self.logout()
        self.assertIn('You were logged out', rv.data)

    def test_show_messages(self):
        rv = self.login(self.testuser, self.testpassword)
        self.assertIn('You are talking to', rv.data)

    def test_send_message(self):
        pass


if __name__ == '__main__':
    unittest.main()
