from corona.extensions import db
from datetime import datetime


class qPCR(db.Model):
    """Base Project Model
    """

    __tablename__ = 'qpcrs'

    id = db.Column(db.Integer, primary_key=True)
    well = db.Column(db.String, nullable=False)
    marker_id = db.Column(db.Integer, db.ForeignKey('markers.id'))
    cycle = db.Column(db.SmallInteger)
    rn = db.Column(db.Float, nullable=False)

    sample_id = db.Column(db.Integer, db.ForeignKey('samples.id'))
    sample = db.relationship('Sample', backref='qpcrs', lazy=True)

    def __repr__(self):
        return '<qPCR: {}>'.format(self.id)