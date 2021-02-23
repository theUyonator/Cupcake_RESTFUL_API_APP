"""Models for Cupcake app."""

from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

# Connect to database 

def connect_db(app):
    """This function connects the app to the cupcakes db"""
    db.app=app
    db.init_app(app)


Generic_cupcake_img = "https://tinyurl.com/demo-cupcake"
class Cupcake(db.Model):
    """This model holds information on the structure of the cupcakes table in the cupcakes db"""

    __tablename__ = "cupcakes"

    id = db.Column(db.Integer,
                    primary_key=True,
                    autoincrement=True)

    flavor = db.Column(db.Text,
                     nullable=False)
    
    size = db.Column(db.Text,
                        nullable=False)

    rating = db.Column(db.Float,
                        nullable=False)

    image = db.Column(db.Text,
                        nullable=False,
                        default=Generic_cupcake_img)
    

    def __repr__(self):
        """This method shows a representation of a particular instance of the Cupcake class"""

        s = self

        return f"flavor = {s.flavor} size = {s.size} rating = {s.rating}"

    def serialize_cupcake(self):
        """Serialize a particular instance of cupcake to dictionary"""

        s = self

        return {

            "id": s.id,
            "flavor": s.flavor,
            "size": s.size,
            "rating": s.rating,
            "image": s.image
        }