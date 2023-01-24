from flask import render_template,session,redirect
from flask_app import app

from flask_app.models.model_users import User

#landing page
@app.route('/')
def landing_page():
    if 'uuid' in session:
        return redirect('/dashboard')
    return render_template("index.html")
