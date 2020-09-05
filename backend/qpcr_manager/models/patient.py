from qpcr_manager.extensions import db


class Patient(db.Model):
    """Base Patient Model
    """

    __tablename__ = 'patients'

    id = db.Column(db.Integer, primary_key=True)
    full_name = db.Column(db.String, nullable=False)
    cedula = db.Column(db.String, nullable=False)
    birth_date = db.Column(db.Date, nullable=False)
    is_male = db.Column(db.Boolean, nullable=False)

    def __repr__(self):
        return '<Patient: {}>'.format(self.id)
