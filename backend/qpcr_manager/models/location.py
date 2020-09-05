from qpcr_manager.extensions import db


class Location(db.Model):
    """Base Location Model
    """

    __tablename__ = 'locations'

    id = db.Column(db.Integer, primary_key=True)
    key = db.Column(db.String, nullable=False)
    location = db.Column(db.String, nullable=False)
    longitude = db.Column(db.String, nullable=False)
    latitude = db.Column(db.String, nullable=False)
    color = db.Column(db.String, nullable=False)

    # User
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    user = db.relationship('User', backref='locations', lazy=True)

    def __repr__(self):
        return '<Location: {}>'.format(self.id)
