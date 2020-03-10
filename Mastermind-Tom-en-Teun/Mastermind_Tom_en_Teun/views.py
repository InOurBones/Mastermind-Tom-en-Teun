"""
Routes and views for the flask application.
"""

from datetime import datetime
from flask import render_template
from Mastermind_Tom_en_Teun import app

@app.route('/')
@app.route('/home')
def home():
    """Renders the home page."""
    return render_template(
        'index.html',
        title='Home Page',
        year=datetime.now().year,
    )

@app.route('/settings')
def settings():
    """Renders the settings page."""
    return render_template(
        'settings.html',
    )

@app.route('/stats')
def stats():
    """Renders the stats page."""
    return render_template(
        'stats.html'
    )
