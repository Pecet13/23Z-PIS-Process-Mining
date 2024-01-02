import unittest
from unittest.mock import patch

from flask import json
from app import app, db, Log


class FlaskAppTestCase(unittest.TestCase):

    def setUp(self):
        app.config['TESTING'] = True
        app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'
        self.app = app.test_client()
        with app.app_context():
            db.create_all()

    def tearDown(self):
        with app.app_context():
            db.drop_all()

    def test_index_route(self):
        response = self.app.get('/')
        self.assertEqual(response.status_code, 200)

    def test_data_page_route(self):
        response = self.app.get('/data')
        self.assertEqual(response.status_code, 200)

    def test_get_data_route_returns_data(self):
        with app.app_context():
            db.session.add(Log(case_id=1, activity_code='A', start_time=None, end_time=None))
            db.session.commit()

            # Test the /api/data route
            response = self.app.get('/api/data')
            self.assertEqual(response.status_code, 200)
            data = json.loads(response.data.decode('utf-8'))
            self.assertTrue(isinstance(data, list))
            self.assertEqual(len(data), 1)
            self.assertEqual(data[0]['case_id'], 1)
            self.assertEqual(data[0]['activity_code'], 'A')

    def test_get_data_route_no_data(self):
        # Test the /api/data route with no data in the database
        response = self.app.get('/api/data')
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.data.decode('utf-8'))
        self.assertTrue(isinstance(data, list))
        self.assertEqual(len(data), 0)

    def test_receive_data_route_success(self):
        # Test the /api/endpoint route with valid data
        data = {
            'CaseID': 1,
            'ActivityCode': 'A',
            'StartTime': 1638537600000,
            'EndTime': 1638541200000
        }
        response = self.app.post('/api/endpoint', json=data)
        self.assertEqual(response.status_code, 200)
        data_received = json.loads(response.data.decode('utf-8'))
        self.assertEqual(data_received['status'], 'success')

        # Check if the data is stored in the database
        with app.app_context():
            logs = Log.query.all()
            self.assertEqual(len(logs), 1)
            self.assertEqual(logs[0].case_id, 1)
            self.assertEqual(logs[0].activity_code, 'A')

    def test_receive_data_route_invalid_data(self):
        # Test the /api/endpoint route with invalid data
        data = {
            'CaseID': 'InvalidValue',
            'ActivityCode': 'A',
            'StartTime': 1638537600000,
            'EndTime': 1638541200000
        }
        response = self.app.post('/api/endpoint', json=data)
        self.assertEqual(response.status_code, 200)
        data_received = json.loads(response.data.decode('utf-8'))
        self.assertEqual(data_received['status'], 'success')

    def test_view_data_route(self):
        response = self.app.get('/admin/data')
        self.assertEqual(response.status_code, 200)


if __name__ == '__main__':
    unittest.main()
