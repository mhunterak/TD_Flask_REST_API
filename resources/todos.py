'''
resources.todos - the API engine
This module contains the functions that power the API.
'''
from flask import abort, jsonify, Blueprint, url_for
from flask_restful import (
    Resource, Api, reqparse, fields, marshal, marshal_with)
from requests import Response

import models

todo_fields = {
    'id': fields.Integer,
    'name': fields.String,
}


def get_todo_or_404(id):
    '''
This function either gets a Todo by ID, or raises a 404 error.
    '''
    try:
        # get the Todo by ID
        todo = models.Todo.get(models.Todo.id == id)
    # if the Todo doesn't exist,
    except models.Todo.DoesNotExist:
        # raise a 404 error
        abort(404)
    # if no error is raised,
    else:
        # return the todo
        return todo


class TodoList(Resource):
    '''
    This class is the Resource for the TodoList API endpoint.
    methods: GET, POST
    '''

    def __init__(self):
        self.reqparse = reqparse.RequestParser()
        self.reqparse.add_argument(
            'name',
            required=True,
            help='No todo title provided',
            location=['form', 'json']
        )
        super().__init__()

    def get(self):
        '''
        The GET method returns a list of all Todos in the database with the
        marshal function.
        '''
        todos = [
            marshal(todo, todo_fields)
            for todo in models.Todo.select().order_by(-models.Todo.id)]
        return todos

    @marshal_with(todo_fields)
    def post(self):
        '''
        The POST method uses the @marshal_with decorator to create new Todos.
        '''
        # get the request arguments
        args = self.reqparse.parse_args()
        # create a new Todo from the POST arguments
        todo = models.Todo.create(**args)
        # return a Location for the new todo
        return (todo, 201,
                {'Location': url_for('resources.todos.todo', id=todo.id)}
                )


class Todo(Resource):
    def __init__(self):
        self.reqparse = reqparse.RequestParser()
        self.reqparse.add_argument(
            'name',
            required=True,
            help='No todo title provided',
            location=['form', 'json']
        )
        super().__init__()

    @marshal_with(todo_fields)
    def get(self, id):
        '''
        The GET method uses the @marshal_with decorator to return a Todo,
        selected by ID.
        '''
        return get_todo_or_404(id)

    @marshal_with(todo_fields)
    def put(self, id):
        '''
        The PUT method uses the @marshal_with decorator to update Todos.
        '''
        # get the request arguments
        args = self.reqparse.parse_args()
        # build the update query
        query = models.Todo.update(**args).where(models.Todo.id == id)
        # execute the query
        query.execute()
        # return the model in a response
        return (models.Todo.get(models.Todo.id == id), 200,
                {'Location': url_for('resources.todos.todo', id=id)})

    def delete(self, id):
        '''
        The DELETE method deletes a Todo.
        '''
        # build the delete query
        query = models.Todo.delete().where(models.Todo.id == id)
        # execute the query
        query.execute()
        # return the location for all todos
        return ('', 204, {'Location': url_for('resources.todos.todos')})

# build the API Blueprint
todos_api = Blueprint('resources.todos', __name__)
# build the api object
api = Api(todos_api)
# add the todos endpoint
api.add_resource(
    TodoList,
    '/todos',
    endpoint='todos'
)
# add the todo endpoint
api.add_resource(
    Todo,
    '/todos/<int:id>',
    endpoint='todo',
)
