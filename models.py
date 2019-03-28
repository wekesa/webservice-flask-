from flask_sqlalchemy import SQLAlchemy
import datetime

db = SQLAlchemy()


class BaseModel(db.Model):
    """Base data model for all objects"""

    __abstract__ = True

    def __init__(self, *args):
        super().__init__(*args)

    def __repr__(self):
        """Define a base way to print models"""
        return "%s(%s)" % (
            self.__class__.__name__,
            {column: value for column, value in self._to_dict().items()},
        )

    def json(self):
        """
        Define a base way to jsonify models, dealing with datetime objects
        """
        return {
            column: value
            if not isinstance(value, datetime.date)
            else value.strftime("%Y-%m-%d")
            for column, value in self._to_dict().items()
        }


class VehicleMake(db.Model):
    """model for one of vehicleMakes table"""

    __tablename__ = "vehicleMake"

    @property
    def serialize(self):
        """Return object data in easily serializable format"""
        return {"id": self.id, "name": self.name, "description": self.description}

    id = db.Column("make_id", db.Integer, primary_key=True)
    name = db.Column(db.String(80), unique=True, nullable=False)
    description = db.Column(db.String(255), nullable=True)
    make_models = db.relationship("VehicleModel", backref="vehicleMake", lazy="dynamic")


class VehicleModel(db.Model):
    """Model for the vehicleModels table"""

    __tablename__ = "vehicleModel"

    @property
    def serialize(self):
        """Return object data in easily serializable format"""
        return {
            "id": self.id,
            "name": self.name,
            "make_id": self.make_id,
            "year": self.year,
            "price": self.price,
            "description": self.description,
        }

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120), nullable=False)
    make_id = db.Column(
        db.Integer, db.ForeignKey("vehicleMake.make_id"), nullable=False
    )
    year = db.Column(db.String(50), nullable=False)
    price = db.Column(db.String(100), nullable=False)
    vehicle_make = db.relationship("VehicleMake", backref="models")
    description = db.Column(db.String(100), nullable=True)
