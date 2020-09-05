from qpcr_manager.extensions import db


class Process(db.Model):
    """Base Process Model
    """

    __tablename__ = 'process'

    id = db.Column(db.Integer, primary_key=True)
    process = db.Column(db.String, unique=True)
    description = db.Column(db.Text)

    def __repr__(self):
        return '<Process: {}>'.format(self.process)
