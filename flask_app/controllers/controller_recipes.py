from flask import render_template, redirect, session, request
from flask_app import app, bcrypt

from flask_app.models.model_recipes import Recipe #TODO import model file here
from flask_app.models.model_users import User

#route to new recipe form page
@app.route('/recipe/new')
def recipe_new():
    if 'uuid' not in session:
        return redirect('/')

    user ={'id': session['uuid']}
    return render_template("recipe_new.html",user=user)

#route to submit create recipe form
@app.route('/recipe/create',methods=['post'])
def recipe_create():
    if not Recipe.validate(request.form):
        return redirect('/recipe/new')

    user_id = session['uuid']
    data = {
        **request.form,
        'user_id': user_id
    }
    
    recipe_id = Recipe.create(data)
    
    if recipe_id == False:
        print("Failed to create recipe")
    else:
        print(f"recipe Created at {recipe_id} id")
        
    return redirect(f'/user/{user_id}')

#route to show individual recipe
@app.route('/recipe/<int:id>')
def recipe_show(id):
    if 'uuid' not in session:
        return redirect('/')

    user ={
        'id': session['uuid'],
        'first_name': session['first_name'],
    }

    # recipe = Recipe.get_one({'id': id})
    recipe = Recipe.get_one_with_creator({'id': id})

    return render_template("recipe_show.html",user=user,recipe=recipe)

#route to edit recipe form
@app.route('/recipe/<int:id>/edit')
def recipe_edit(id):
    if 'uuid' not in session:
        return redirect('/')

    recipe = Recipe.get_one({'id': id})
    user_id = session['uuid']
    return render_template("recipe_edit.html", recipe=recipe,user_id=user_id)

#route to submit edit form
@app.route('/recipe/<int:id>/update',methods=['post'])
def recipe_update(id):
    if not Recipe.validate(request.form):
        return redirect(f'/recipe/{id}/edit')

    user_id = session['uuid']
    data = {
        **request.form,
        'id':id
        }
    Recipe.update_one(data)
    return redirect(f'/user/{user_id}')

#delete recipe route
@app.route('/recipe/<int:id>/delete')
def recipe_delete(id):
    user_id = session['uuid']
    Recipe.delete_one({'id': id})
    return redirect(f'/user/{user_id}')

#route to show all recipes
# @app.route('/recipe/all')
# def recipe_all():
#     recipes = Recipe.get_all()
    
#     return render_template('recipe_show.html',recipes=recipes)