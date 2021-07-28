#!/usr/bin/python

import sqlite3
import re

def db_setup(fn):
    global conn
    global cursor
    conn = sqlite3.connect(fn)
    conn.execute("PRAGMA journal_mode=WAL")
    cursor = conn.cursor()

def db_cursor():
    global cursor
    return cursor

def db_close():
    global conn
    conn.close()

def db_query(string):
    global cursor
    cursor.execute(string)
    return cursor.fetchall()

def db_query_first(string):
    global cursor
    cursor.execute(string)

def db_lastrowid():
    global cursor
    return cursor.lastrowid

def db_create_table(name, pattern):
    return db_query('CREATE TABLE %s (%s)' % (name, pattern))

def db_commit():
    global conn
    return conn.commit()

def db_insert(name, values):
    db_query("INSERT INTO %s VALUES (%s)" % (name, values))
    return db_commit()

def db_delete(name):
    db_query('DELETE FROM %s' % name)
    return db_commit()

def db_show(string):
    for row in db_query(string):
        print(row)

def db_show_table(name):
    db_show('SELECT * FROM %s' % name)

def db_checkTalbeExists(name):
    m_exist = db_query('SELECT * FROM %s' % (name))
    return len(m_exist) >= 1


