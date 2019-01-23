#!/usr/bin/env python3

import time
import psycopg2
import os
import sys

from clint.textui import colored, puts
from psycopg2 import sql
from datetime import datetime


conn = None

with open('settings.txt', 'r') as f:
    PASSWORD = f.read().strip('\n')
    f.close()


class Todo(object):
    '''id: integer, title: string, content: string,
    due: datetime, complete: bool'''
    def __init__(self, year, month, day, hour, minute, *args, **kwargs):
        self.__dict__.update(kwargs)
        due = datetime(year, month, day, hour, minute)
        self.due = time.mktime(due.timetuple())


def connect():
    global conn
    try:
        conn = psycopg2.connect('dbname=todos user=postgres ' +
                                'password={}'.format(PASSWORD))
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
    finally:
        if conn is not None:
            return conn


def create_todo(year, month, day, hour, minute, **kwargs):
    try:
        todo = Todo(year, month, day, hour, minute, **kwargs)
        cur = conn.cursor()
        cur.execute('''INSERT INTO todo (title, content, due, complete)
                    values ('{}', '{}', {}, {})'''.format(todo.title,
                    todo.content, todo.due, todo.complete))

        conn.commit()
        cur.close()
        print('todo added')
    except (Exception, psycopg2.DatabaseError) as error:
        print('Error: ', error)
        print('Rolling back transaction')
        conn.rollback()


def filter_rows(rows):
    for row in rows:
        todo_id, title, content, is_complete, due = row
        due_date = time.ctime(due)
        complete = 'complete' if is_complete else 'incomplete'
        print('{}\t{}\t{}\t{}\t{}'.format(todo_id, title, content,
              complete, due_date))


def get_rows(curr):
    rows = []
    row = curr.fetchone()
    if row is None:
        print('No todos')
    while row is not None:
        rows.append(row)
        row = curr.fetchone()
    filter_rows(rows)


def get_todos():
    curr = conn.cursor()
    try:
        sql = '''SELECT * FROM todo'''
        curr.execute(sql)
        get_rows(curr)
    except Exception as e:
        print('Error: ', e)
    curr.close()


def get_complete_todos():
    curr = conn.cursor()
    try:
        sql = 'SELECT * FROM todo WHERE complete = true'
        curr.execute(sql)
        get_rows(curr)
    except Exception as e:
        print('Error', e)
        print('Rolling back transaction')
        conn.rollback()

    curr.close()


def get_not_complete_todos():
    curr = conn.cursor()
    try:
        sql = 'SELECT * FROM todo WHERE complete = false'
        curr.execute(sql)
        get_rows(curr)
    except Exception as e:
        print('Error', e)
        print('Rolling back transaction')
        conn.rollback()
    curr.close()


def delete_todo(todo_id):
    curr = conn.cursor()
    try:
        curr.execute(sql.SQL('''delete from todo where {} = id'''
                             .format(todo_id)))
        conn.commit()
        print('todo deleted')
    except Exception:
        print('No todo found for ID')
    curr.close()


def mark_complete(todo_id):
    curr = conn.cursor()
    try:
        curr.execute(sql.SQL('update todo set complete = true' +
                             'where id = {}'.format(todo_id)))
        conn.commit()
        print('marked todo complete')
    except Exception:
        print('No todo found for ID')
    curr.close()


def main():
    global conn
    if conn is None:
        conn = connect()

    while True:
        os.system('clear')
        puts(colored.cyan('==================='))
        get_todos()
        puts(colored.cyan('==================='))
        action = input('1. Create\n2. Delete\n3. Options\n4. Exit\n')
        try:
            action = int(action)
        except Exception:
            puts(colored.red('INVALID ARGUMENT'))
            continue
        if action == 1:
            puts(colored.cyan('--- CREATE ---'))
            os.system('clear')
            # TODO: Indiv check for bad answers
            # Dont want to waste time if year is bad input
            year = int(input('year (YYYY) : '))
            month = int(input('month (MM) : '))
            day = int(input('day (dd) : '))
            hour = int(input('hour (hh) : '))
            minute = int(input('minute (mm) : '))
            title = input('title: ')
            content = input('content: ')
            create_todo(year, month, day, hour, minute, title=title,
                        content=content, complete=False)
        elif action == 2:
            os.system('clear')
            puts(colored.cyan('--- DELETE ---'))
            todo_id = int(input('id: '))
            delete_todo(todo_id)
        elif action == 3:
            os.system('clear')
            puts(colored.cyan('--- OPTIONS ---'))
            view_action = input('1. Get Complete\n2. Get Incomplete' +
                                '\n3. Mark Complete\n4. Back\n')
            try:
                view_action = int(view_action)
            except Exception:
                puts(colored.red('INVALID ARGUMENT'))
                puts(colored.red(input('press any key to continue ... ')))
            os.system('clear')
            if view_action == 1:
                get_complete_todos()
            elif view_action == 2:
                get_not_complete_todos()
            elif view_action == 3:
                todo_id = input('Enter todo id: ')
                mark_complete(todo_id)
            elif view_action == 4:
                continue
            else:
                print('Invalid Argument')
            input('\n press any key to continue ... ')
        elif action == 4:
            conn.close()
            sys.exit(0)
        else:
            puts(colored.red('INVALID ARGUMENT'))


if __name__ == '__main__':
    main()

conn.rollback()
