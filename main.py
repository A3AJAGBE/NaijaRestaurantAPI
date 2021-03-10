from flask import Flask, render_template, jsonify, request
from flask_sqlalchemy import SQLAlchemy

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


db.create_all()


@app.route('/')
def index():
    return render_template('index.html')


@app.route("/add", methods=["POST"])
def post_new_cafe():
    new_restaurant = Restaurants(
        name=request.form.get("name"),
        map_url=request.form.get("map_url"),
        img_url=request.form.get("img_url"),
        location=request.form.get("location"),
        eat_in=bool(int(request.form.get("eat_in"))),
        delivers=bool(int(request.form.get("delivers"))),
    )
    db.session.add(new_restaurant)
    db.session.commit()
    return jsonify(response={"success": "Successfully added the new restaurant."})


if __name__ == '__main__':
    app.run(debug=True)
