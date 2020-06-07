from flask import request
from flask_restful import Resource
from flask_jwt_extended import jwt_required

from corona.extensions import db, ma
from corona.commons.pagination import paginate
from corona.models import qPCR, Marker
from corona.helpers import query_qpcrs


class qPCRSchema(ma.SQLAlchemyAutoSchema):

    id = ma.auto_field()
    marker_id = ma.auto_field()
    cycle = ma.auto_field()
    rn = ma.auto_field()
    sample_id = ma.auto_field()

    class Meta:
        model = qPCR
        sqla_session = db.session


class qPCRResource(Resource):
    """Single Object Resource
    """

    method_decorators = [jwt_required]

    def get(self, qpcr_id):
        schema = qPCRSchema()
        qpcrs = qPCR.query.get_or_404(qpcr_id)
        return {"qpcrs": schema.dump(qpcrs)}

    def put(self, qpcr_id):
        schema = qPCRSchema(partial=True)
        qpcr = qPCR.query.get_or_404(qpcr_id)
        qpcr = schema.load(request.json, instance=qpcr)

        db.session.commit()
        return {"msg": "qpcr updated", "qpcr": schema.dump(qpcr)}

    def delete(self, qpcr_id):
        qpcr = qPCR.query.get_or_404(qpcr_id)
        db.session.delete(qpcr)
        db.session.commit()

        return {"msg": "qpcr deleted"}


class qPCRList(Resource):
    """Creation and get all objects Resource
    """

    method_decorators = [jwt_required]

    def get(self):
        schema = qPCRSchema(many=True)
        query = qPCR.query
        return paginate(query, schema)

    def post(self):
        schema = qPCRSchema()
        qpcr = schema.load(request.json)

        db.session.add(qpcr)
        db.session.commit()

        return {"msg": "qpcr created", "qpcr": schema.dump(qpcr)}, 201


class qPCRSampleResource(Resource):
    """Get patients qPCR data
    """

    method_decorators = [jwt_required]

    def get(self, sample_id):
        qpcrs = query_qpcrs(sample_id)
        return {'qpcrs': qpcrs}
