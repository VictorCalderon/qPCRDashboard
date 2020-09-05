from qpcr_manager.extensions import db


class Sample(db.Model):
    """Base Sample Model
    """

    __tablename__ = 'samples'

    id = db.Column(db.Integer, primary_key=True)
    sample = db.Column(db.String, nullable=False)
    tmpl_well = db.Column(db.String)
    priority_level = db.Column(db.Integer, nullable=False)
    collection_date = db.Column(db.Date)
    description = db.Column(db.Text)

    # Experiment
    experiment_id = db.Column(db.Integer, db.ForeignKey('experiments.id',))
    experiment = db.relationship('Experiment', backref='samples',  lazy=True)
    
    # Patient
    patient_id = db.Column(db.Integer, db.ForeignKey('patients.id'))
    patient = db.relationship('Patient', backref="samples", lazy=True)

    # Location
    location_id = db.Column(db.Integer, db.ForeignKey('locations.id'))
    location = db.relationship('Location', backref="samples", lazy=True)


    def __repr__(self):
        return '<Sample: {}>'.format(self.id)
