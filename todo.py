#!/usr/bin/env python3

import psycopg2
import time

from psycopg2 import sql
from datetime import datetime


conn = None

with open('settings.txt', 'r') as f:
    PASSWORD = f.read().strip('\n')
    f.close()


class Todo(object):
    '''id: integer, title: string, content: string, due: datetime, complete: bool'''
    def __init__(self, year, month, day, hour, minute, *args, **kwargs):
        self.__dict__.update(kwargs)
        due = datetime(year, month, day, hour, minute)
        self.due = time.mktime(due.timetuple())

def connect():
    global conn
    try:
        conn = psycopg2.connect('dbname=todos user=postgres password={}'.format(PASSWORD))
        cur = conn.cursor()
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
    finally:
        if conn is not None:
            return conn


def create_todo(year, month, day, hour, minute, **kwargs):
    todo = Todo(year, month, day, hour, minute, **kwargs)
    cur = conn.cursor()
    cur.execute('''INSERT INTO todo (title, content, due, complete)
                   values ('{}', '{}', {}, {})'''.format(todo.title, todo.content,
                       todo.due, todo.complete))

    conn.commit()
    cur.close()
    print('todo added')


def update_todo(todo_id):
    pass


def get_todos():
    curr = conn.cursor()
    try:
        sql = '''SELECT * FROM todo'''
        curr.execute(sql)
        row = curr.fetchone()
        while row is not None:
            todo_id, title, content, is_complete, due = row
            due_date = time.ctime(due)
            complete = 'complete' if is_complete else 'incomplete'
            print(todo_id, title, content, complete, due_date)
            row = curr.fetchone()
    except Exception as e:
        print('Error: ', e)
    curr.close()


def get_complete_todos():
    curr = conn.cursor()
    try:
        sql = 'SELECT * FROM todo WHERE complete = true'
        curr.execute(sql)
        row = curr.fetchone()

        while row is not None:
            todo_id, title, content, is_complete, due = row
            due_date = time.ctime(due)
            complete = 'complete' if is_complete else 'incomplete'
            # TODO: Make this format pretty
            print(todo_id, title, content, complete, due_date)
            row = curr.fetchone()
        if row is None:
            print('No todos marked complete')
    except Exception as e:
        print('Error', e)
    curr.close()


def get_not_complete_todos():
    curr = conn.cursor()
    try:
        sql = 'SELECT * FROM todo WHERE complete = false'
        curr.execute(sql)
        row = curr.fetchone()

        while row is not None:
            todo_id, title, content, is_complete, due = row
            due_date = time.ctime(due)
            complete = 'complete' if is_complete else 'incomplete'
            print(todo_id, title, content, complete, due_date)
            row = curr.fetchone()
    except Exception as e:
        print('Error', e)
    curr.close()


def delete_todo(todo_id):
    curr = conn.cursor()
    try:
        curr.execute(sql.SQL('''delete from todo where {} = id'''.format(todo_id)))
        conn.commit()
        print('todo deleted')
    except Exception:
        print('No todo found for ID')
    curr.close()


def mark_complete(todo_id):
    curr = conn.cursor()
    try:
        curr.execute(sql.SQL('update todo set complete = true where id = {}'.format(todo_id)))
        conn.commit()
        print('marked todo complete')
    except Exception as e:
        print('No todo found for ID')
    curr.close()

def main():
    global conn
    if conn is None:
        conn = connect()

    view_option = False
    while True:
        if not view_option:
            print('------------------------------')
            get_todos()
        view_option = False
        print('------------------------------')
        action = input('1. Create\n2. Delete\n3. Options\n')
        try:
            action = int(action)
        except Exception:
            print('Invalid Argument')
            continue
        if action == 1:
            year = int(input('year (YYYY) : '))
            month = int(input('month (MM) : '))
            day = int(input('day (dd) : '))
            hour = int(input('hour (hh) : '))
            minute = int(input('minute (mm) : '))
            title = input('title: ')
            content = input('content: ')
            todo = create_todo(year, month, day, hour, minute, title=title,
                    content=content, complete=False)
        elif action == 2:
            todo_id = int(input('id: '))
            delete_todo(todo_id)
        elif action == 3:
            view_action = input('1. Get Complete\n2. Get Incomplete\n3. Mark Complete\n4. Back\n')
            view_option = True
            try:
                view_action = int(view_action)
            except Exception:
                print('Invalid Argument')
            if view_action == 1:
                get_complete_todos()
            elif view_action == 2:
                get_not_complete_todos()
            elif view_action == 3:
                todo_id = input('Enter todo id: ')
                mark_complete(todo_id)
            elif view_action == 4:
                pass
            else:
                print('Invalid Argument')

        else:
            print('Invalid Argument')


if __name__ == '__main__':
    main()

