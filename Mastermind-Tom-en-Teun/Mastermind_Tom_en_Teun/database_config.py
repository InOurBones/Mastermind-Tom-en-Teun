import sqlite3
import os
import hashlib
import datetime

from sqlite3 import Error

def delete_db():
    try:
        os.remove('mastermind_db.db')
        print("Database removed")
    except Exception as ex:
        print(ex.args)

# DATABASE
def connect_db():
    try:
        con = sqlite3.connect('mastermind_db.db')
        print("Database connected")
        return con
    except Error:
        print(Error)

def hash_password(password):
    return hashlib.sha512(password.encode('utf-8')).hexdigest()

def sql_table(con):
    cursor = con.cursor()

    # users
    create_users_sql = """
    CREATE TABLE users (
        id integer PRIMARY KEY AUTOINCREMENT,
        name text NOT NULL,
        password text NOT NULL)"""
    cursor.execute(create_users_sql)
    insert_users_sql = "INSERT INTO users (id, name, password) VALUES (null, ?, ?)"
    cursor.execute(insert_users_sql, ('admin', hash_password('admin')))

    # games
    create_game_sql = """
    CREATE TABLE games (
        id integer PRIMARY KEY AUTOINCREMENT,
        date_played datetime NOT NULL,
        finished boolean NOT NULL,
        turns int NOT NULL,
        user_id integer,
        FOREIGN KEY (user_id) REFERENCES users (id))"""
    cursor.execute(create_game_sql)
    
    con.commit()
    print("Database created")

delete_db()
con = connect_db()
sql_table(con)