import sqlite3
import json
import os
import random
import requests
import hashlib
from datetime import datetime
from collections import Counter
from flask import Flask, session, request, Response, g, redirect, url_for, abort, render_template, flash, make_response

app = Flask(__name__)
app.secret_key = b'\xd4\xc6\x14\xd4\xe3\xce\x04\xe5\x15\xa5\xf7Z$\x8e \x1a'

# CLASSES
class Options:
    def __init__(self, column=4, colour=4, unique=True):
        self.num_column = column
        self.num_colour = colour
        self.unique = unique

class Playfield:
    colour_types = ('black', 'grey', 'yellow', 'red', 'blue', 'green', 'brown', 'pink', 'orange', 'purple')

    def __init__(self):
        self.colours = random.sample(Playfield.colour_types, my_options.num_colour)
        self.colours.sort()
        self._field = []
        self._field.append([0] * my_options.num_column)
        self._response = []
        self._response.append([0] * my_options.num_column)
        self._finished = False
        if my_options.unique:
            self.secretcode = random.sample(self.colours, my_options.num_column)
        else:
            self.secretcode = []
            for _ in range(my_options.num_colour):
                self.secretcode.append(random.choice(self.colours))                

    def placepin(self, cell, colour):
        self._field[-1][cell] = colour

    def checkcode(self):
        for i in range(len(self._field[-1])):
            if self._field[-1][i] == self.secretcode[i]:
                self._response[-1][i] = 'black'
            elif self._field[-1][i] in self.secretcode:
                self._response[-1][i] = 'white'
            else:
                self._response[-1][i] = ''

    def checkrow(self):
        if 0 in self._field[-1]:
            session['error'] = 'Niet alle vakjes zijn gevuld'
            return False
        if my_options.unique and len(Counter(self._field[-1]).keys()) != my_options.num_column:
            session['error'] = 'Niet alle kleuren zijn unique'
            return False
        session['error'] = ''
        return True

    def next_round(self):
        if (self.checkrow()):
            self.checkcode()
            if self.is_won():
                self._finished = True
            else:
                self._response.append([0] * my_options.num_column)
                self._field.append([0] * my_options.num_column)

    def is_won(self):
        if len(Counter(self._response[-1])) == 1 and "black" in self._response[-1]:
            return True
        return False

# OBJECTS
my_options = Options(4, 4)
my_playfield = Playfield()

# ROUTES
def requires_auth(origfunc):
    def authenticator(*args, **kwargs):
        if 'user' in session:
            return origfunc(*args, **kwargs)

        session['nexturl'] = request.full_path.rstrip('?')
        return redirect(url_for('login'))

    return authenticator

@app.route('/')
@app.route('/login/', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['user']
        password = request.form['pass']
        user = next_row(do_query("SELECT * FROM users WHERE name = ?", (username,)))
        print(user)
        digest = hashlib.sha512(password.encode('utf-8')).hexdigest()
        if user and digest == user['password']:
            del user['password']
            session['user'] = user
            if 'nexturl' in session:
                response = redirect(session['nexturl'])
                del session['nexturl']
                return response
            else:
                return redirect("/home")
        else:
            render_template('login.html')
    return render_template('login.html')

@app.route('/logout/')
def logout():
    if 'user' in session:
        del session['user']
    return redirect(url_for('login'))

@app.route('/home')
@requires_auth
def home():
    return render_template('index.html',
        year=datetime.now().year,
        my_opt = my_options,
        my_pf = my_playfield,
        name = session['user']['name'],
        error = session['error'] or '',)

@app.route('/accountdetails', methods=['GET', 'POST'])
def accountdetails():
    global my_playfield
    if request.method == 'POST':
        print(request.form['duplicate'])
        if request.form['duplicate'] == 'duplicate_no':
            if int(request.form['colours_used']) < int(request.form['columns_used']):
                return render_template('accountdetails.html',
                    my_opt = my_options,
                    error = 'Je kan niet minder kleuren hebben dan het aantal kolommen zonder dubbele kleuren',)
        my_options.num_colour = int(request.form['colours_used'])
        my_options.num_column = int(request.form['columns_used'])
        my_options.unique = False if request.form['duplicate'] == 'duplicate_yes' else True
        my_playfield = Playfield()
        return redirect("/home")
    return render_template('accountdetails.html',
        name = session['user']['name'],
        my_opt = my_options,
        error = '')

@app.route('/stats')
def stats():
    print(next_row(do_query("SELECT COUNT(id) FROM games WHERE user_id = ?", (session['user']['id'],))),)
    return render_template('stats.html',
        name = session['user']['name'],
        games = get_resultset("SELECT * FROM games WHERE user_id = ?", (session['user']['id'],)),)

# REDIRECTS
@app.route('/nextround/')
def nextround():
    my_playfield.next_round()
    return redirect('/home')

@app.route('/reset/')
def reset():
    global my_playfield 
    save_game()
    my_playfield = Playfield()
    session['error'] = ''
    return redirect('/home')

# FUNCTIONS
@app.route('/handleplacement')
def test():
    colour = request.args.get('colour', type = str)
    cell = request.args.get('cell', type = int)
    my_playfield.placepin(cell, colour)
    return "succes", 200

# DATABASE
def next_row(generator):
    try:
        return dict(generator.__next__())
    except StopIteration:
        return {}

def do_query(query, bindings=None):
    """
    Generator function, yielding a single database row
    """
    cursor = get_db().cursor()
    if bindings:
        cursor.execute(query, bindings)
    else:
        cursor.execute(query)

        while True:
            row = cursor.fetchone()
            if not row:
                return None
            yield row

def get_resultset(query, bindings=None):
    cursor = get_db().cursor()
    if bindings:
        cursor.execute(query, bindings)
    else:
        cursor.execute(query)

    return cursor.fetchall()

def insert_data(query, bindings=None):
    con = get_db()
    cursor = con.cursor()
    if bindings:
        cursor.execute(query, bindings)
    else:
        cursor.execute()
    con.commit()        

def connect_db():
    rv = sqlite3.connect('mastermind_db.db')
    rv.row_factory = sqlite3.Row
    return rv

def get_db():
    if 'sqlite_db' not in g:
        g.sqlite_db = connect_db()
    return g.sqlite_db

def save_game():
    if len(my_playfield._field) > 1:
        save_query_sql = "INSERT INTO games VALUES (null, null, ?, ?, ?, ?, ?)"
        insert_data(save_query_sql, (my_playfield._finished, my_options.num_column, my_options.num_colour, len(my_playfield._field), session['user']['id']))
        print(next_row(do_query("SELECT * FROM games ORDER BY id DESC")))

@app.teardown_appcontext
def close_db(error):
    db = g.pop('sqlite_db', None)
    if db:
        db.close()