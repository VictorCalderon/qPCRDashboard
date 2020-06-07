from corona.extensions import db
import datetime


class Sample(db.Model):
    """Base Results Model
    """

    __tablename__ = 'samples'

    id = db.Column(db.Integer, primary_key=True)
    sample = db.Column(db.String, nullable=False)

    project_id = db.Column(db.Integer, db.ForeignKey(
        'projects.id', ondelete='CASCADE'))

    project = db.relationship(
        'Project', backref='samples', cascade='all,delete', lazy=True)

    def __repr__(self):
        return '<Project: {}>'.format(self.id)
