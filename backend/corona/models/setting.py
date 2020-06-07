from corona.extensions import db
from datetime import datetime


class Setting(db.Model):
    """Base Setting Model
    """

    __tablename__ = 'settings'

    id = db.Column(db.Integer, primary_key=True)
    setting_name = db.Column(db.String, nullable=False)
    setting_value = db.Column(db.Boolean, default=False)

    def __repr__(self):
        return f'<Setting(setting_name={self.setting_name},setting_value={self.setting_value})>'