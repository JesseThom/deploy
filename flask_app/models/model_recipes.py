from flask_app.config.mysqlconnection import connectToMySQL
from flask import flash
from flask_app import DATABASE
from flask_app.models import model_users


class Recipe:
    def __init__(self,data:dict):
        #for every column in table from db, must have an attribute
        self.id = data['id']
        self.name = data['name']
        self.under_30 = data['under_30']
        self.instructions = data['instructions']
        self.description = data['description']
        self.date_made = data['date_made']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']
        self.user_id = data['user_id']


#validation
    @staticmethod
    def validate(data):
        is_valid = True

        if len(data["name"]) < 3:
            flash("Name must be at least 3 characters.","err_recipes_name")
            is_valid=False

        if len(data["description"]) < 3:
            flash("Description must be at least 3 characters.","err_recipes_description")
            is_valid=False
    
        if len(data["instructions"]) < 3:
            flash("Instructions must be at least 3 characters.","err_recipes_instructions")
            is_valid=False

        return is_valid

#C
    @classmethod
    def create(cls,data):
        query = "INSERT INTO recipes (name, under_30, instructions, description, date_made, user_id) VALUES (%(name)s,%(under_30)s,%(instructions)s,%(description)s,%(date_made)s,%(user_id)s);"
        user_id = connectToMySQL(DATABASE).query_db(query, data) 

        return user_id
#R
    @classmethod
    def get_one(cls, data):
        query = "SELECT * FROM recipes WHERE id = %(id)s;"
        results = connectToMySQL(DATABASE).query_db(query,data)
        
        if not results:
            return False

        return cls(results[0])

    @classmethod
    def get_one_with_creator(cls, data):
        query = "SELECT * FROM recipes JOIN users ON users.id = recipes.user_id WHERE recipes.id = %(id)s;"
        results = connectToMySQL(DATABASE).query_db(query,data)
        # print(results)

        for dict in results:
            recipe_data = {
                'id' :dict['id'],
                'name' :dict['name'],
                'under_30' :dict['under_30'],
                'instructions' :dict['instructions'],
                'description' :dict['description'],
                'date_made' :dict['date_made'],
                'created_at' :dict['created_at'],
                'updated_at' :dict['updated_at'],
                'user_id' :dict['user_id'],
            }

            user_data = {
                'id' : dict['id'],
                'first_name' : dict['first_name'],
                'last_name' : dict['last_name'],
                'email' : dict['email'],
                'password' : dict['password'],
                'created_at' : dict['created_at'],
                'updated_at' : dict['updated_at'],
            }

            recipe = Recipe(recipe_data)
            recipe.user = model_users.User(user_data)

        return recipe

    @classmethod
    def get_all_with_users(cls):
        query = "SELECT * FROM users  JOIN recipes ON users.id = recipes.user_id ;"
        results = connectToMySQL(DATABASE).query_db(query)

        if not results:
            return False

        all_recipes = []
        for dict in results:
            recipe_data = {
                'id' : dict['recipes.id'],
                'name' : dict['name'],
                'under_30' : dict['under_30'],
                'instructions' : dict['instructions'],
                'description' : dict['description'],
                'date_made' : dict['date_made'],
                'created_at' : dict['recipes.created_at'],
                'updated_at' : dict['recipes.updated_at'],
                'user_id' : dict['user_id'],
            }
            
            user_data = {
                'id' : dict['id'],
                'first_name' : dict['first_name'],
                'last_name' : dict['last_name'],
                'email' : dict['email'],
                'password' : dict['password'],
                'created_at' : dict['created_at'],
                'updated_at' : dict['updated_at'],
            }

            recipe = Recipe(recipe_data)
            recipe.users = model_users.User(user_data)
            all_recipes.append(recipe)
            
        return all_recipes

    @classmethod
    def get_all(cls):
        query = "SELECT * FROM recipes"
        results = connectToMySQL(DATABASE).query_db(query)

        all_recipes = []
        for dict in results:
            all_recipes.append(cls(dict))

        return all_recipes

#U
    @classmethod
    def update_one(cls,data):
        query = "UPDATE recipes SET name = %(name)s, under_30 = %(under_30)s, instructions = %(instructions)s, description = %(description)s, date_made = %(date_made)s WHERE id = %(id)s;"

        return connectToMySQL(DATABASE).query_db(query,data)
#D
    @classmethod
    def delete_one(cls,data):
        query = "DELETE FROM recipes WHERE id = %(id)s;"

        return connectToMySQL(DATABASE).query_db(query,data)