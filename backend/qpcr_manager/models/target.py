from qpcr_manager.extensions import db


class Target(db.Model):
    """Base Target Model
    """

    __tablename__ = 'targets'

    id = db.Column(db.Integer, primary_key=True)
    key = db.Column(db.String)
    target = db.Column(db.String)
    description = db.Column(db.Text)

    # Users
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    user = db.relationship('User', backref='targets', lazy=True)

    __table_args__ = (db.UniqueConstraint('target', 'user_id', name='target_user_unique'),)

    def __repr__(self):
        return '<Target: {}>'.format(self.target)
