from qpcr_manager.extensions import db


class Experiment(db.Model):
    """Base Experiment Model
    """

    __tablename__ = 'experiments'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable=False)
    experiment_date = db.Column(db.Date, nullable=False)
    observations = db.Column(db.Text)
    methodology = db.Column(db.Text)
    analyzed = db.Column(db.Boolean, default=False)

    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    user = db.relationship('User', backref='experiments', lazy=True)

    def __repr__(self):
        return '<Experiment: {}>'.format(self.id)
