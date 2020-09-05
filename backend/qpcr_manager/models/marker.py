from qpcr_manager.extensions import db


class Marker(db.Model):
    """Base Marker Model
    """

    __tablename__ = 'markers'

    id = db.Column(db.Integer, primary_key=True)
    marker = db.Column(db.String, unique=True, nullable=False)

    # Targets
    target_id = db.Column(db.Integer, db.ForeignKey('targets.id'))
    target = db.relationship('Target', backref='marker', lazy=True)

    # Users
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    user = db.relationship('User', backref='markers', lazy=True)

    def __repr__(self):
        return '<Marker: {}>'.format(self.marker)
