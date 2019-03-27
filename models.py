from datetime import datetime as dt
import json

from flask import jsonify
from itsdangerous import (TimedJSONWebSignatureSerializer as Serializer,
                          BadSignature, SignatureExpired)
import peewee

import config

DATABASE = peewee.SqliteDatabase('todos.db')


class Todo(peewee.Model):
    name = peewee.CharField()
    created_at = peewee.DateTimeField(default=dt.now)
    # created_by = ForeignKeyField(User, related_name='todo_set')

    class Meta:
        database = DATABASE


def initialize(test=False):
    DATABASE.connect(reuse_if_open=True)
    DATABASE.create_tables([Todo], safe=True)
    # if there aren't and todos in the database,
    print("{} Todos today".format(Todo.select().count()))
    if Todo.select().count() < 1:
        # open the mock json file
        mock_file = open('mock/todos.json', "r")
        # load json from the mock file
        data = json.loads(mock_file.read())
        # for each todo in the json data
        for todo in data:
            # create a new todo
            Todo.create(name=todo['name'])
        mock_file.close()
    DATABASE.close()
