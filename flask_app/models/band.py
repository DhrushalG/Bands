from flask_app.config.mysqlconnection import connectToMySQL
from flask import flash
from flask_app.models import user

class Band:
    def __init__(self, data):
        self.id = data['id']
        self.name = data['name']
        self.genre = data['genre']
        self.home_city = data['home_city']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']
        self.user_id = data['user_id']
        self.first_name = data['first_name']
        self.last_name = data['last_name']
        self.bands_id = data['bands_id']

    @classmethod
    def get_all_bands(cls, data):
        query = "SELECT * FROM bands JOIN users ON users.id = bands.user_id LEFT JOIN (SELECT * FROM members WHERE users_id = %(user_id)s) as members ON members.bands_id = bands.id;"
        results = connectToMySQL('bands_schema').query_db(query, data)
        bands = []
        for item in results:
            new_band = cls(item)
            new_user_data = {
                'id' : item['users.id'],
                'first_name' : item['first_name'],
                'last_name' : item['last_name'],
                'email' : item['email'],
                'password' : item['password'],
                'created_at' : item['users.created_at'],
                'updated_at' : item['users.updated_at'],
                'users_id' : item['users_id']
            }
            new_user = user.User(new_user_data)
            new_band.user = new_user
            bands.append(new_band)

        return bands

    @classmethod
    def create_new_band(self, data):
        query = "INSERT INTO bands (name, genre, home_city, user_id) VALUES(%(name)s,%(genre)s,%(home_city)s,%(user_id)s);"
        result = connectToMySQL('bands_schema').query_db(query, data)
        return result


    @staticmethod
    def validate_band(data):
        is_valid = True

        if len(data['name']) < 3:
            is_valid = False
            flash("Band name needs to be greater than 3 characters")

        if len(data['genre']) < 3:
            is_valid = False
            flash("Band's genre' needs to be greater than 3 characters")

        if len(data['home_city']) < 3:
            is_valid = False
            flash("Band's home city needs to be greater than 3 characters")

        return is_valid

    @classmethod
    def edit_bands(cls, data):
        query = "SELECT * FROM bands JOIN users ON bands.user_id = users.id LEFT JOIN members ON bands.id = members.bands_id WHERE bands.id = %(bands_id)s;"
        result = connectToMySQL('bands_schema').query_db(query, data)
        single_band = cls(result[0])
        # like = 0;
        # for item in result:
        #     if item['bands_id']:
        #         like += 1;
        # single_band.num_of_likes += like;

        return single_band

    @classmethod
    def update_band(cls,data):
        query = "UPDATE bands SET name = %(name)s, genre = %(genre)s, home_city = %(home_city)s WHERE bands.id = %(id)s;"
        connectToMySQL('bands_schema').query_db(query, data)

    @classmethod
    def delete_band(cls, data):
        query = "DELETE FROM bands WHERE id = %(id)s;"
        connectToMySQL('bands_schema').query_db(query, data)

    @classmethod
    def join_band(cls, data):
        query = "INSERT INTO members(users_id, bands_id) SELECT %(users_id)s, %(bands_id)s WHERE  NOT EXISTS (SELECT * FROM members WHERE users_id = %(users_id)s and bands_id = %(bands_id)s);"
        result = connectToMySQL('bands_schema').query_db(query, data)
        return result

    @classmethod
    def leave_band(cls,data):
        query = "DELETE FROM members WHERE users_id= %(users_id)s AND bands_id= %(bands_id)s;"
        result = connectToMySQL('bands_schema').query_db(query, data)
        return result