import unittest
import base64
import json
from datetime import datetime

from peewee import *
from werkzeug.exceptions import NotFound

import app
import config
import models
from resources import todos

CLIENT = app.app.test_client()


# TESTS GO HERE


class ModelsTestCase(unittest.TestCase):
    def test_create_todo(self):
        self.assertEqual(app.models.Todo.select().count(), 0)
        todo = models.Todo.create(name="Unittest your code!")
        self.assertEqual(app.models.Todo.select().count(), 1)
        todo = todos.get_todo_or_404(1)
        todo.delete_instance()

    def test_create_todo_defaults(self):
        models.initialize()

    def test_get_or_404(self):
        with self.assertRaises(NotFound):
            todos.get_todo_or_404(30)
        models.Todo.create(name="Unittest your code!")
        self.assertEqual(todos.get_todo_or_404(1).id, 1)
        
    def test_ZZ_tearDown(self):
        for todo in app.models.Todo.select():
            todo.delete_instance()


class TodoTestResources(unittest.TestCase):
    def testViewRoutes(self):
        rv = CLIENT.get('/')
        self.assertEqual(rv.status_code, 200)

    def testTodosAPIRoutesGet(self):
        rv = CLIENT.get('/api/v1/todos')
        self.assertEqual(rv.status_code, 200)

        rv = CLIENT.get('/api/v1/todos/1')
        self.assertEqual(rv.status_code, 200)

    def testTodosAPIRoutesPost(self):
        rv = CLIENT.post('/api/v1/todos', data=dict(name='Unit Test your App'))
        self.assertEqual(rv.status_code, 201)

    def testTodosAPIRoutesPut(self):
        rv = CLIENT.put('/api/v1/todos/1', data=dict(name='Unit Test Your App'))
        self.assertEqual(rv.status_code, 200)

    def testTodosAPIRoutes_Delete(self):
        rv = CLIENT.delete('/api/v1/todos/1')
        self.assertEqual(rv.status_code, 204)






if __name__ == '__main__':
    unittest.main()
