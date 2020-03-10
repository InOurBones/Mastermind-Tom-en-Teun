from datetime import datetime
from flask import render_template
from Mastermind_Tom_en_Teun import app

@app.route('/')
@app.route('/home')
def home():
    return render_template(
        'index.html',
        year=datetime.now().year,
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
