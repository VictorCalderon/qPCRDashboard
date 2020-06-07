from corona.extensions import db
from datetime import datetime


class Project(db.Model):
    """Base Project Model
    """

    __tablename__ = 'projects'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable=False)
    experiment_date = db.Column(db.Date, nullable=False)
    observations = db.Column(db.Text)
    analyzed = db.Column(db.Boolean, default=False)

    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    user = db.relationship('User', backref='projects', lazy=True)

    def __repr__(self):
        return '<Project: {}>'.format(self.id)
