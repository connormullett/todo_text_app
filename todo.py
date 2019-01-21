
import psycopg2
import time

from psycopg2 import sql
from datetime import datetime


with open('settings.txt', 'r') as f:
    PASSWORD = f.read().strip('\n')
    f.close()


class Todo(object):
    '''id: integer, title: string, content: string, due: datetime, complete: bool'''
    def __init__(self, year, month, day, hour, minute, *args, **kwargs):
        self.__dict__.update(kwargs)
        due = datetime(year, month, day, hour, minute)
        self.due = time.mktime(due.timetuple())

    def __str__(self):
        return f'{self.title} {self.content} {self.due}'


def connect():
    conn = None
    try:
        conn = psycopg2.connect(f'dbname=todos user=postgres password={PASSWORD}')
        cur = conn.cursor()

        print('POSTGRESQL DATABASE VERSION: ')
        cur.execute('SELECT version()')

        db_version = cur.fetchone()
        print(db_version)
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
    finally:
        if conn is not None:
            return conn


def create_todo(year, month, day, hour, minute, **kwargs):
    todo = Todo(year, month, day, hour, minute, **kwargs)
    conn = connect()
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
    conn = connect()
    curr = conn.cursor()
    try:
        sql = '''SELECT * FROM todo'''
    except Exception as e:
        print('Error: ', e)


def get_complete_todos():
    pass


def get_not_complete_todos():
    pass


def delete_todo(todo_id):
    conn = connect()
    curr = conn.cursor()
    try:
        sql = '''delete from todo where {todo_id} = id'''
        curr.execute(sql)
        conn.commit()
        print('todo deleted')
    except Exception:
        print('No todo found for ID')
    curr.close()


def mark_complete(**kwargs):
    pass


def main():
    while True:



if __name__ == '__main__':
    main()

