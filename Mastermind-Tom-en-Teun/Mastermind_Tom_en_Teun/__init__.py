import sqlite3
import json
import os
import random
import requests
from datetime import datetime
from collections import Counter
from flask import Flask, session, request, Response, g, redirect, url_for, abort, render_template, flash, make_response

app = Flask(__name__)
app.secret_key = b'\xd4\xc6\x14\xd4\xe3\xce\x04\xe5\x15\xa5\xf7Z$\x8e \x1a'

# CLASSES
class Options:
    def __init__(self, column=4, colour=4):
        self.num_column = column
        self.num_colour = colour
        self.unique = True

class Playfield:
    colour_types = ('black', 'grey', 'yellow', 'red', 'blue', 'green', 'brown', 'pink', 'orange', 'purple')

    def __init__(self):
        self.colours = random.sample(Playfield.colour_types, my_options.num_colour)
        self.colours.sort()
        self._field = []
        self._field.append([0] * my_options.num_column)
        self._response = []
        self.secretcode = random.sample(self.colours, my_options.num_column)

    def placepin(self, cell, colour):
        self._field[-1][cell] = colour

    def checkcode(self):
        self._response.append([0] * my_options.num_column)
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
        if my_options.unique and len(Counter(self._field[-1]).keys()) != 4:
            session['error'] = 'Niet alle kleuren zijn unique'
            return False
        session['error'] = ''
        return True

    def next_round(self):
        if (self.checkrow()):
            self.checkcode()
            self._field.append([0] * my_options.num_column)

    def reset(self):
        self._response = []
        self._field = []
        self._field.append([0] * my_options.num_column)

# OBJECTS
my_options = Options(4)
my_playfield = Playfield()

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
    my_playfield.next_round()
    return redirect(url_for('home'))

@app.route('/reset/', methods=['POST'])
def reset():
    my_playfield.reset()
    return redirect(url_for('home'))

# FUNCTIONS
@app.route('/handleplacement')
def test():
    colour = request.args.get('colour', type = str)
    cell = request.args.get('cell', type = int)
    my_playfield.placepin(cell, colour)
    print(my_playfield._field)
    return "succes", 200