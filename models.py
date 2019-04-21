from datetime import datetime as dt
import json

from flask import jsonify
from itsdangerous import (TimedJSONWebSignatureSerializer as Serializer,
                          BadSignature, SignatureExpired)
import peewee

import config

DATABASE = peewee.SqliteDatabase('todos.db')


class Todo(peewee.Model):
    '''
    The Todo model holds the name of each todo in the database.
    '''
    name = peewee.CharField()
    # XXC: this isn't included in instructions, but this handles if a box is checked
    completed = peewee.BooleanField(default=False)

    class Meta:
        database = DATABASE


def initialize():
    '''
    Initializes the database and adds the mock entries, if none exist.
    '''
    # connect to the DATABASE
    DATABASE.connect(reuse_if_open=True)
    # connect the tables for Todo in the DATABASE
    DATABASE.create_tables([Todo], safe=True)
    # if there aren't and Todos in the database,
    if not Todo.select().count():
        # open the mock json file
        mock_file = open('mock/todos.json', "r")
        # load json from the mock file
        data = json.loads(mock_file.read())
        # for each todo in the json data,
        for todo in data:
            # create a new todo
            Todo.create(name=todo['name'])
        # close the mock file
        mock_file.close()
    # close the DATABASE connection
    DATABASE.close()
