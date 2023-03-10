import os
import tempfile
import unittest

from kanban import create_app
from kanban.db import init_db


class KanbanTestCase(unittest.TestCase):

    def setUp(self):
        self.db_fd, self.db_path = tempfile.mkstemp()
        self.app = create_app({
            'TESTING': True,
            'DATABASE': self.db_path,
        })
        self.client = self.app.test_client()

        with self.app.app_context():
            init_db()

    def tearDown(self):
        os.close(self.db_fd)
        os.unlink(self.db_path)
         

    def test_register(self):
        with self.client:

            #users can access landing page, sign up & log in without authentication
            response = self.client.get('/kanban')
            self.assertEqual(response.status_code, 200)

            response = self.client.get('/auth/register')
            self.assertEqual(response.status_code, 200)

            response = self.client.get('/auth/login')
            self.assertEqual(response.status_code, 200)

            #trying to access the index page redirects to landing page
            response = self.client.get('/')
            self.assertEqual(response.status_code, 302)
            self.assertIn('Location', response.headers)
            self.assertEqual(response.headers['Location'], '/kanban') 
                        
            #registering redirects to log in page            
            response = self.client.post('/auth/register', data={
                'username': 'testuser',
                'password': 'testpassword'
            })
            self.assertEqual(response.status_code, 302)
            self.assertIn('Location', response.headers)
            self.assertEqual(response.headers['Location'], '/auth/login')

            #registering with the same username flashes error username is taken
            response = self.client.post('/auth/register', data={
                'username': 'testuser',
                'password': 'testpassword'
            })
            self.assertIn(b'already taken', response.data)

    def test_login(self):
        with self.client:
            #sign up as a test user
            self.client.post('/auth/register', data={
                'username': 'testuser',
                'password': 'testpassword'
            })

            #logging in with non-existent username flashes corresponding error
            response = self.client.post('/auth/login', data={
                'username': 'testuser1',
                'password': 'testpassword'
            })
            self.assertIn(b'Incorrect username', response.data)

            #logging in with wrong password flashes corresponding error
            response = self.client.post('/auth/login', data={
                'username': 'testuser',
                'password': 'testpassword1'
            })
            self.assertIn(b'Incorrect password.', response.data)

            # logging in redirects to index page
            response = self.client.post('/auth/login', data={
                'username': 'testuser',
                'password': 'testpassword'
            })
            self.assertEqual(response.status_code, 302)
            self.assertIn('Location', response.headers)
            self.assertEqual(response.headers['Location'], '/')

    def test_logout(self):
            #sign up & log in as a test user
            self.client.post('/auth/register', data={
                'username': 'testuser',
                'password': 'testpassword'
            })
            self.client.post('/auth/login', data={
                'username': 'testuser',
                'password': 'testpassword'
            })

            #logging out redirects to landing page
            response = self.client.get('/auth/logout')
            self.assertEqual(response.status_code, 302)
            self.assertIn('Location', response.headers)
            self.assertEqual(response.headers['Location'], '/kanban')

    def test_task(self):
        with self.client:
            #sign up & log in as a test user
            self.client.post('/auth/register', data={
                'username': 'testuser',
                'password': 'testpassword'
            })
            self.client.post('/auth/login', data={
                'username': 'testuser',
                'password': 'testpassword'
            })
            
            #creating a to-do task
            response = self.client.post('/create', data={
                'title': 'Test Task',
                'description': 'This is a test task',
                'status': 'todo',
                'priority': 'low',
            }, follow_redirects=True)

            #check task exists and is under 'To-do' ("Move to Doing" exists)
            self.assertIn(b'Test Task', response.data)
            self.assertIn(b'Move to Doing', response.data)
            self.assertEqual(response.status_code, 200)

            #markdoing
            response = self.client.post('/1/markdoing', follow_redirects=True)
            self.assertIn(b'Mark Done', response.data) #proxy for status "Doing"

            #markdone
            response = self.client.post('/1/markdone', follow_redirects=True)
            self.assertNotIn(b'Move to Doing', response.data) and self.assertNotIn(b'Mark Done', response.data) #proxy for status "Done"
           

            #updating title, status & priority
            response = self.client.post('/1/update', data={
                'title': 'Test Task updated',
                'description': 'This is a test task',
                'status': 'doing',
                'priority': 'high',
            }, follow_redirects=True)

            #check title, status and priority are updated
            self.assertIn(b'Test Task updated', response.data)
            self.assertNotIn(b'Move to Doing', response.data) #proxy for not status "To Do"
            self.assertIn(b'Mark Done', response.data) #proxy for status "Doing"
            self.assertEqual(response.status_code, 200)

            #deleting task
            response = self.client.post('/1/delete', follow_redirects=True)

            #check title, status and priority are updated
            self.assertNotIn(b'Test Task updated', response.data)
            self.assertEqual(response.status_code, 200)

if __name__ == '__main__':
    unittest.main()