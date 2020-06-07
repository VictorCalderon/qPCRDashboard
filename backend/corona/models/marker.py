from corona.extensions import db
from datetime import datetime


class Marker(db.Model):
    """Base Marker Model
    """

    __tablename__ = 'markers'

    id = db.Column(db.Integer, primary_key=True)
    marker = db.Column(db.String, unique=True, nullable=False)

    def __repr__(self):
        return '<Marker: {}>'.format(self.marker)