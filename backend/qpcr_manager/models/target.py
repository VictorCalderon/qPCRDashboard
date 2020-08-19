from qpcr_manager.extensions import db


class Target(db.Model):
    """Base Target Model
    """

    __tablename__ = 'targets'

    id = db.Column(db.Integer, primary_key=True)
    key = db.Column(db.String)
    name = db.Column(db.String, unique=True, nullable=False)
    description = db.Column(db.Text)

    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    user = db.relationship('User', backref='targets', lazy=True)

    def __repr__(self):
        return '<Target: {}>'.format(self.marker)
