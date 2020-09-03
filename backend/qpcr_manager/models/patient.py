from qpcr_manager.extensions import db


class Patient(db.Model):
    """Base Patient Model
    """

    __tablename__ = 'patients'

    id = db.Column(db.Integer, primary_key=True)
    full_name = db.Column(db.String, nullable=False)
    cedula = db.Column(db.String, nullable=False)
    barcode = db.Column(db.String, nullable=False)
    birth_date = db.Column(db.Date, nullable=False)
    priority = db.Column(db.Integer, nullable=False)
    suspected_illness = db.Column(db.String)
    is_male = db.Column(db.Boolean, nullable=False)
    step = db.Column(db.Integer, nullable=False)

    location_id = db.Column(db.Integer, db.ForeignKey('locations.id'))
    location = db.relationship('Location', backref="patients", lazy=True)


    def __repr__(self):
        return '<Patient: {}>'.format(self.id)
