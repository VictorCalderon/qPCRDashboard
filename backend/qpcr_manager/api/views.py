from flask import Blueprint, current_app, jsonify
from flask_restful import Api
from marshmallow import ValidationError

from qpcr_manager.extensions import apispec, jwt
from qpcr_manager.api.resources import *
from qpcr_manager.api.resources import UserSchema


blueprint = Blueprint("api", __name__, url_prefix="/api/v1")
api = Api(blueprint)

# Single and multiple record queries for users
api.add_resource(UserList, "/users")
api.add_resource(UserResource, "/users/<int:user_id>")

# Single and multiple resources for experiments
api.add_resource(ExperimentList, "/experiments")
api.add_resource(ExperimentResource, "/experiments/<int:experiment_id>")
api.add_resource(LastExperimentResource, "/experiments/lastexperiment")

# Single Experiment utilities
api.add_resource(ExperimentsQuery, "/experiments/query")
api.add_resource(ExperimentResults, "/experiments/<int:experiment_id>/results")
api.add_resource(ExperimentSamplesList, "/experiments/<int:experiment_id>/samples")

# Single and multiple records queries for qpcrs
api.add_resource(SampleList, "/samples")
api.add_resource(SampleResource, "/samples/<int:sample_id>")
api.add_resource(SampleFluorescenceResource, "/samples/<int:sample_id>/fluorescences")
api.add_resource(SamplesQuery, "/samples/query")

# Import/Export functionality for experiments
api.add_resource(ImportExperiment, '/experiments/import')
api.add_resource(ExportExperiment, '/experiments/export/<int:experiment_id>')

# Simple and multiple records queries for Sample Location
api.add_resource(LocationList, '/dashboard/samplelocation')
api.add_resource(LocationResource, '/dashboard/samplelocation/<int:location_id>')

# Amplification time series and other dashboard data
# api.add_resource(AmplificationTimeSeriesResource, "/timeseries")
# api.add_resource(MarkerSpecificDataset, "/dataset")
# api.add_resource(MarkerList, '/markers')
api.add_resource(ProjectBrief, '/dashboard/briefing')
api.add_resource(AmpStatData, '/dashboard/ampstatdata')
api.add_resource(TagDistribution, '/dashboard/tagdistrib')
api.add_resource(LocatedSamples, '/dashboard/locatedsamples')


@blueprint.before_app_first_request
def register_views():
    apispec.spec.components.schema("UserSchema", schema=UserSchema)
    apispec.spec.path(view=UserResource, app=current_app)
    apispec.spec.path(view=UserList, app=current_app)


@blueprint.errorhandler(ValidationError)
def handle_marshmallow_error(e):
    """Return json error for marshmallow validation errors.

    This will avoid having to try/catch ValidationErrors in all endpoints, returning
    correct JSON response with associated HTTP 400 Status (https://tools.ietf.org/html/rfc7231#section-6.5.1)
    """
    return jsonify(e.messages), 400
