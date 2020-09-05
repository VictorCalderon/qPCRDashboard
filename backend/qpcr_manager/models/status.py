from qpcr_manager.extensions import db


class Status(db.Model):
    """Base Sample Status Model
    """

    __tablename__ = 'status'

    id = db.Column(db.Integer, primary_key=True)
    timestamp = db.Column(db.DateTime)

    # Sample id
    sample_id = db.Column(db.Integer, db.ForeignKey('samples.id'))
    sample = db.relationship('Sample', backref="statuses", lazy=True)

    # Process name
    process_id = db.Column(db.Integer, db.ForeignKey('process.id'))
    process = db.relationship('Process', backref='processes', lazy=True)

    def __repr__(self):
        return '<Status: {}>'.format(self.id)
