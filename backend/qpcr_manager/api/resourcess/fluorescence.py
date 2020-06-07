from flask import request
from flask_restful import Resource
from flask_jwt_extended import jwt_required

from qpcr_manager.extensions import db, ma
from qpcr_manager.commons.pagination import paginate
from qpcr_manager.models import Fluorescence, Marker
from qpcr_manager.helpers import query_fluorescence


class FluorescenceSchema(ma.SQLAlchemyAutoSchema):

    id = ma.auto_field()
    marker_id = ma.auto_field()
    cycle = ma.auto_field()
    rn = ma.auto_field()
    sample_id = ma.auto_field()

    class Meta:
        model = Fluorescence
        sqla_session = db.session


class FluorescenceSampleResource(Resource):
    """Get patients Fluorescence data
    """

    method_decorators = [jwt_required]

    def get(self, sample_id):
        qpcrs = query_fluorescence(sample_id)
        return {'qpcrs': qpcrs}
