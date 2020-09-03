from qpcr_manager.extensions import db


class SampleStatus(db.Model):
    """Base Sample Status Model
    """

    __tablename__ = 'sample_status'

    id = db.Column(db.Integer, primary_key=True)
    step = db.Column(db.Integer, nullable=False)

    # Status ID
    sample_id = db.Column(db.Integer, db.ForeignKey('samples.id'))
    sample = db.relationship('Sample', backref="sample_status", lazy=True)

    def __repr__(self):
        return '<SampleStatus: {}>'.format(self.id)
