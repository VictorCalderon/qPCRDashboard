from qpcr_manager.extensions import db


class Fluorescence(db.Model):
    """Base Fluorescence Model
    """

    __tablename__ = 'fluorescences'

    id = db.Column(db.Integer, primary_key=True)
    well = db.Column(db.String, nullable=False)
    marker_id = db.Column(db.Integer, db.ForeignKey('markers.id'))
    cycle = db.Column(db.SmallInteger)
    rn = db.Column(db.Float, nullable=False)

    sample_id = db.Column(db.Integer, db.ForeignKey('samples.id'))
    sample = db.relationship('Sample', backref='fluorescence', lazy=True)

    def __repr__(self):
        return '<Fluorescence: {}>'.format(self.id)
