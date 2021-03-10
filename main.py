import os
import random
from flask import Flask, render_template, jsonify, request
from flask_sqlalchemy import SQLAlchemy
from dotenv import load_dotenv
load_dotenv()

app = Flask(__name__)

# Database Config
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///restaurants.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

# Restaurants TABLE Configuration


class Restaurants(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(250), unique=True, nullable=False)
    map_url = db.Column(db.String(500), nullable=False)
    img_url = db.Column(db.String(500), nullable=False)
    location = db.Column(db.String(250), nullable=False)
    eat_in = db.Column(db.Boolean, nullable=False)
    delivers = db.Column(db.Boolean, nullable=False)

    def __repr__(self):
        return f'Restaurant Name: {self.name}'

    def to_dict(self):
        # Dictionary Comprehension to loop through the table
        return {column.name: getattr(self, column.name) for column in self.__table__.columns}


db.create_all()


@app.route('/')
def index():
    return render_template('index.html')


@app.route("/add", methods=["POST"])
def new_restaurant():
    """Add a new restaurant."""
    api_key = request.args.get("api-key")
    if api_key == os.environ.get('api-key'):
        add_restaurant = Restaurants(
            name=request.form.get("name"),
            map_url=request.form.get("map_url"),
            img_url=request.form.get("img_url"),
            location=request.form.get("location"),
            eat_in=bool(int(request.form.get("eat_in"))),
            delivers=bool(int(request.form.get("delivers"))),
        )
        db.session.add(add_restaurant)
        db.session.commit()
        return jsonify(response={"success": "Successfully added the new restaurant."})
    else:
        return jsonify(error={"Forbidden": "Invalid API Key, provide the correct api_key."}), 403


@app.route("/random", methods=["GET"])
def random_restaurant():
    """A random restaurant is retrieve from the database."""
    restaurants = Restaurants.query.all()
    restaurant = random.choice(restaurants)
    return jsonify(cafe=restaurant.to_dict())


@app.route("/all", methods=["GET"])
def all_restaurants():
    """Returns all the restaurants in the database."""
    restaurants = Restaurants.query.all()
    return jsonify(restaurants=[restaurant.to_dict() for restaurant in restaurants])


@app.route("/search", methods=["GET"])
def search_by_location():
    """Search the database by location"""
    query_location = request.args.get("location")
    restaurant = Restaurants.query.filter_by(location=query_location).first()
    if restaurant:
        return jsonify(restaurant=restaurant.to_dict())
    else:
        return jsonify(error={"Not Found": "We don't have a restaurant at that location."})


@app.route("/update_delivers/<int:id>", methods=["PATCH"])
def patch_delivers(id):
    """Update the delivers field"""
    api_key = request.args.get("api-key")
    if api_key == os.environ.get('api-key'):
        update_delivers = request.args.get("delivers")
        restaurant = Restaurants.query.get(id)
        if restaurant:
            restaurant.delivers = bool(int(update_delivers))
            db.session.commit()
            return jsonify(response={"success": "Successfully updated the delivers service."}), 200
        else:
            return jsonify(error={"Not Found": "A restaurant with that id does not exist."}), 404
    else:
        return jsonify(error={"Forbidden": "Invalid API Key, provide the correct api_key."}), 403


@app.route("/delete/<int:id>", methods=["DELETE"])
def delete_restaurant(id):
    """Delete a restaurant from the database"""
    api_key = request.args.get("api-key")
    if api_key == os.environ.get('api-key'):
        restaurant = Restaurants.query.get(id)
        if restaurant:
            db.session.delete(restaurant)
            db.session.commit()
            return jsonify(response={"success": "Deleted the restaurant from the database successfully."}), 200
        else:
            return jsonify(error={"Not Found": "A restaurant with that id does not exist."}), 404
    else:
        return jsonify(error={"Forbidden": "Invalid API Key, provide the correct api_key."}), 403


if __name__ == '__main__':
    app.run(debug=True)
