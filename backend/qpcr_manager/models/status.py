from qpcr_manager.extensions import db


class Status(db.Model):
    """Base Sample Status Model
    """

    __tablename__ = 'status'

    id = db.Column(db.Integer, primary_key=True)
    step = db.Column(db.Integer, nullable=False)

    # Status ID
    sample_id = db.Column(db.Integer, db.ForeignKey('samples.id'))
    sample = db.relationship('Sample', backref="status", lazy=True)

    def __repr__(self):
        return '<Status: {}>'.format(self.id)
