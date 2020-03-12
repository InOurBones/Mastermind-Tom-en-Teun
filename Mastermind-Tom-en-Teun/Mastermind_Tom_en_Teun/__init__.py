import sqlite3
import json
import os
from datetime import datetime
from flask import Flask, session, request, Response, g, redirect, url_for, abort, render_template, flash, make_response
from pprint import pprint

app = Flask(__name__)
app.secret_key = b'\xd4\xc6\x14\xd4\xe3\xce\x04\xe5\x15\xa5\xf7Z$\x8e \x1a'

@app.route('/')
@app.route('/home')
def home():
    if 'cr' not in session:
        opt = Options()
        #session['options'] = json.dumps(opt,default=convert_to_dict)
        session['cr'] = opt.currentround
    return render_template(
        'index.html',
        year=datetime.now().year,
        #currentround = session['options']['currentround'],
        currentround = session['cr'],
    )

@app.route('/settings')
def settings():
    return render_template(
        'settings.html',
    )

@app.route('/stats')
def stats():
    return render_template(
        'stats.html'
    )

def convert_to_dict(obj):
  obj_dict = {
    "__class__": obj.__class__.__name__,
    "__module__": obj.__module__
  }

  obj_dict.update(obj.__dict__)
  
  return obj_dict

class Options:

    def __init__(self):
        self.currentround = 2
