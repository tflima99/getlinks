from app import *
import unittest

class test_app(unittest.TestCase):

    def test_index_status(self):
       resp1 = self.app.get('/')
       self.assertEqual(resp1.status_code, 200)

    def test_new_get_status(self):
       resp2 = self.app.get('/new_get')
       self.assertEqual(resp2.status_code, 200)

    def test_view_status(self):
       resp3 = self.app.get('/view')
       self.assertEqual(resp3.status_code, 200)


if __name__ == '__main__':
    unittest.main()
