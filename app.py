"""Flask app for Cupcakes"""

from flask import Flask, render_template, request, redirect, flash, jsonify
from flask_debugtoolbar import DebugToolbarExtension
from models import db, connect_db, Cupcake


app = Flask(__name__)

app.config["SECRET_KEY"] = "cupc9k3s"
app.config["DEBUG_TB_INTERCEPT_REDIRECTS"] = False
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///cupcakes'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ECHO'] = True

debug = DebugToolbarExtension(app)
connect_db(app)


####################### Api Routes ####################

@app.route("/")
def homepage():
    """This view function renders the hompage for this cupcake app"""

    return render_template("index.html")

@app.route("/api/cupcakes")
def get_cupcakes():
    """This view function returns JSON for all cupcakes in the cupcakes db"""

    cupcakes = Cupcake.query.all()
    serialized = [c.serialize_cupcake() for c in cupcakes]

    return jsonify(cupcakes=serialized)

@app.route("/api/cupcakes/<int:cupcake_id>")
def get_cupcake(cupcake_id):
    """This view function returns JSON for a particular cupcake in the cupcakes db given cupcake id"""

    cupcake = Cupcake.query.get_or_404(cupcake_id)
    serialized = cupcake.serialize_cupcake()

    return jsonify(cupcake=serialized)

@app.route("/api/cupcakes", methods=["POST"])
def create_cupcake():
    """This view function creates cupcake in the cupcakes db and returns JSON"""

    flavor = request.json["flavor"]
    size = request.json["size"]
    rating = request.json["rating"]
    image = request.json["image"]

    new_cupcake = Cupcake(flavor=flavor, size=size, rating=rating, image=image)

    db.session.add(new_cupcake)
    db.session.commit()

    serialized = new_cupcake.serialize_cupcake()

    # We return with status code 201 ---- return tuple (json, status_code)
    return (jsonify(cupcake=serialized), 201)


@app.route("/api/cupcakes/<int:cupcake_id>", methods=["PATCH"])
def update_cupcake(cupcake_id):
    """This view function updates and existing cupcake in the cupcakes db and returns JSON """

    cupcake = Cupcake.query.get_or_404(cupcake_id)

    cupcake.flavor = request.json.get("flavor", cupcake.flavor)
    cupcake.size = request.json.get("size", cupcake.size)
    cupcake.rating = request.json.get("rating", cupcake.rating)
    cupcake.image = request.json.get("image", cupcake.image)

    db.session.commit()

    serialized = cupcake.serialize_cupcake()

    return jsonify(cupcake=serialized)

@app.route("/api/cupcakes/<int:cupcake_id>", methods=["DELETE"])
def delete_cupcake(cupcake_id):
    """This view function deletes an existing cupcake from the cupcakes db and returns JSOn"""

    cupcake = Cupcake.query.get_or_404(cupcake_id)
    db.session.delete(cupcake)
    db.session.commit()

    return jsonify(message="Deleted")