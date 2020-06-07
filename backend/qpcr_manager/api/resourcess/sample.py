from flask import request
from flask_restful import Resource
from flask_jwt_extended import jwt_required, current_user

from corona.models import Sample
from corona.extensions import db, ma
from corona.commons.pagination import paginate

import datetime


class SampleSchema(ma.SQLAlchemyAutoSchema):

    id = ma.auto_field()
    sample = ma.auto_field()
    project_id = ma.auto_field()

    class Meta:
        include_fk = True
        model = Sample
        sqla_session = db.session


class SampleResource(Resource):
    """Single Object Resource
    """

    method_decorators = [jwt_required]

    def get(self, sample_id):
        schema = SampleSchema()
        sample = Sample.query.get_or_404(sample_id)
        return {"sample": schema.dump(sample)}

    def put(self, sample_id):
        schema = SampleSchema(partial=True)
        sample = Sample.query.get_or_404(sample_id)

        db.session.commit()
        return {"msg": "sample updated", "sample": schema.dump(sample)}

    def delete(self, sample_id):
        sample = Sample.query.get_or_404(sample_id)
        db.session.delete(sample)
        db.session.commit()

        return {"msg": "sample deleted"}


class SampleList(Resource):
    """Creation and get all objects Resource
    """
    method_decorators = [jwt_required]

    def get(self):
        schema = SampleSchema(many=True)
        query = Sample.query
        return paginate(query, schema)

    def post(self):
        schema = SampleSchema()
        sample = Sample(**schema.load(request.json))

        db.session.add(sample)
        db.session.commit()

        return {"msg": "sample created", "sample": schema.dump(sample)}, 201


class SamplesExperimentList(Resource):
    """Get all samples from a certain project
    """

    method_decorators = [jwt_required]

    def get(self, project_id):
        schema = SampleSchema(many=True)
        samples = Sample.query.filter_by(
            project_id=project_id).order_by('id')
        return {'samples': schema.dump(samples)}
