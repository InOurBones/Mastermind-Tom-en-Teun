import sqlite3
import json
import os
import random
import requests
from datetime import datetime
from flask import Flask, session, request, Response, g, redirect, url_for, abort, render_template, flash, make_response

app = Flask(__name__)
app.secret_key = b'\xd4\xc6\x14\xd4\xe3\xce\x04\xe5\x15\xa5\xf7Z$\x8e \x1a'

# CLASSES
class Options:
    def __init__(self):
        self.currentround = 0

    def raiseround(self):
        self.currentround += 1

    def reset(self):
        self.currentround = 0

class Playfield:
    colour_types = ('black', 'grey', 'yellow', 'red', 'blue', 'green', 'brown', 'pink', 'orange', 'purple')

    def __init__(self, num_rows, num_colour):
        self.colours = random.sample(Playfield.colour_types, num_colour)
        self.colours.sort()
        self._field = [[0] * 4 for _ in range(num_rows)]

    def placepin(self, row, cell, colour):
        self._field[row][cell] = colour

    def isrowfull(self, row):
        return 0 not in self._field[row]

    def reset(self, num_rows):
        self._field = [[0] * 4 for _ in range(num_rows)]

# OBJECTS
my_options = Options()
my_playfield = Playfield(10, 6)

# ROUTES
@app.route('/')
@app.route('/home')
def home():  
    if 'error' not in session:
        session['error'] = ''
    return render_template('index.html',
        year=datetime.now().year,
        my_opt = my_options,
        my_pf = my_playfield,
        error = session['error'] or '')

@app.route('/settings')
def settings():
    return render_template('settings.html',
        my_opt = my_options,
        my_pf = my_playfield,)

@app.route('/stats')
def stats():
    return render_template('stats.html')

@app.route('/nextround/', methods=['POST'])
def nextround():
    if (my_playfield.isrowfull(my_options.currentround)):
        my_options.raiseround()
        session['error'] = ''
    else:
        session['error'] = 'Niet alle vakjes zijn gevuld'
    return redirect(url_for('home'))

@app.route('/reset/', methods=['POST'])
def reset():
    my_options.reset()
    my_playfield.reset(10)
    return redirect(url_for('home'))

@app.route('/handleplacement')
def test():
    colour = request.args.get('colour', type = str)
    cell = request.args.get('cell', type = int)
    my_playfield.placepin(my_options.currentround, cell, colour)
    print(my_playfield._field)
    return "succes", 200