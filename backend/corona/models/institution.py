from corona.extensions import db
from datetime import datetime


class Institution(db.Model):
    """Base Institution Model
    """

    __tablename__ = 'institutions'

    id = db.Column(db.Integer, primary_key=True)
    institution = db.Column(db.String, unique=True, nullable=False)

    def __repr__(self):
        return '<Institution: {}>'.format(self.institution)