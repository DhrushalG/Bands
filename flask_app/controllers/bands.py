from flask_app import app
from flask import render_template, redirect, request, flash, session
from flask_app.models.user import User
from flask_app.models.band import Band

@app.route('/dashboard')
def dashboard():
    if 'user_id' not in session:
        flash("This page is only available to logged in users.")
        return redirect("/")
    user_id = {
        'user_id' : session['user_id']
    }
    bands = Band.get_all_bands(user_id)
    return render_template("dashboard.html", bands = bands)

@app.route("/bands/new")
def new_band():
    return render_template("create.html")

@app.route("/bands/create", methods=['POST'])
def create_band():
    if Band.validate_band(request.form):
        data = {
            'name': request.form['name'],
            'genre' : request.form['genre'],
            'home_city': request.form['home_city'],
            'user_id': session['user_id'],
            'first_name' : session['first_name'],
            'last_name' : session['last_name']
        }
        Band.create_new_band(data)
        return redirect("/dashboard")
    else:
        return redirect('/bands/new')

@app.route("/bands/<int:user_id>")
def my_bands(user_id):
    data = {
        'user_id': user_id
    }
    # bands = Band.my_bands(data)
    bands = Band.get_all_bands(data)
    return render_template("my_bands.html", bands = bands)

@app.route("/bands/edit/<int:bands_id>")
def edit_band(bands_id):
    data = {
        'bands_id': bands_id
    }
    band = Band.edit_bands(data)
    return render_template("edit_band.html", band = band)

@app.route("/band/edit/<int:bands_id>", methods=["POST"])
def update_band(bands_id):
    if Band.validate_band(request.form):
        data = {
            'id': bands_id,
            'name': request.form['name'],
            'genre': request.form['genre'],
            'home_city': request.form['home_city'],
            'user_id': session['user_id']
        }
        Band.update_band(data)
        return redirect('/dashboard')
    else:
        return redirect(f"/bands/edit/{bands_id}")

@app.route('/bands/<int:bands_id>/delete')
def delete_band(bands_id):
    data = {
        'id': bands_id
    }
    Band.delete_band(data)
    return redirect('/dashboard')

@app.route('/add/member/<int:bands_id>')
def join_band(bands_id):
    data = {
        'users_id' : session['user_id'],
        'bands_id' : bands_id
    }
    Band.join_band(data)
    return redirect("/dashboard")

@app.route("/delete/member/<bands_id>")
def leave_band(bands_id):
    data = {
        'users_id' : session['user_id'],
        'bands_id': bands_id
    }
    Band.leave_band(data)
    return redirect("/dashboard")