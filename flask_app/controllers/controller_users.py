from flask import render_template, redirect, session, request
from flask_app import app, bcrypt

from flask_app.models.model_users import User #TODO import model file here
from flask_app.models.model_recipes import Recipe


#route to submit create user form
@app.route('/user/create',methods=['post'])
def user_create():
    if not User.validate(request.form):
        return redirect('/')
    
    hash_pw = bcrypt.generate_password_hash(request.form['password'])
    data = {
        **request.form,
        'password': hash_pw
    }

    user_id = User.create(data)    
    if user_id == False:
        print("Failed to create user")
    else:
        print(f"User Created at {user_id} id")

    session['uuid'] = user_id
    session['first_name'] = request.form['first_name']

    return redirect(f'/user/{user_id}')

#login
@app.route('/user/login', methods = ['post'])
def user_login():
    data = request.form
    user = User.get_one_by_email({'email':data['email']})

    if not User.validate_login(data,user):
        return redirect('/')

    session['uuid'] = user.id
    session['first_name'] = user.first_name
    return redirect(f'/user/{user.id}')

#route to show individual user
@app.route('/user/<int:id>')
def user_show(id):
    if 'uuid' not in session:
        return redirect('/')
    user = {
        'id': session['uuid'],
        'first_name': session['first_name'],
    }
    recipes = Recipe.get_all_with_users()
    return render_template("user_show.html",user=user,recipes=recipes)

#logout
@app.route('/user/logout')
def logout():
    session.clear()
    return redirect('/')


#route to new user form page
# @app.route('/user/new')
# def user_new():
#     return render_template("user_new.html")

#route to show all users
# @app.route('/user/all')
# def user_all():
#     users = User.get_all()
    
#     return render_template('user_show.html',users=users)


#route to edit user form
# @app.route('/user/<int:id>/edit')
# def user_edit(id):
#     data = {'id': id}
#     user = User.get_one(data)
#     return render_template("user_edit.html", user=user)

#route to submit edit form
# @app.route('/user/<int:id>/update',methods=['post'])
# def user_update(id):
#     data = {
#         **request.form,
#         'id':id
#         }
#     User.update_one(data)
#     return redirect('/')

#delete user route
# @app.route('/user/<int:id>/delete')
# def user_delete(id):
#     data = {'id': id}
#     User.delete_one(data)
#     return redirect("/user/all")