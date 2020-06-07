from flask import Blueprint, current_app, jsonify
from flask_restful import Api
from marshmallow import ValidationError

from corona.api.resources.user import UserSchema
# from corona.api.resources.project import ProjectSchema


from corona.extensions import apispec, jwt

from corona.api.resources import (
    UserResource, UserList, ProjectResource, ProjectList,
    ImportProject, qPCRList, qPCRResource, qPCRSampleResource,
    SampleList, SampleResource, SamplesProjectList, LastProjectResource,
    ExportProject, QueryProjects, ProjectResults, DashboardData, MarkerList
)


blueprint = Blueprint("api", __name__, url_prefix="/api/v1")
api = Api(blueprint)

# Single and multiple record queries for users
api.add_resource(UserList, "/users")
api.add_resource(UserResource, "/users/<int:user_id>")

# Single and multiple records queries for projects
api.add_resource(ProjectList, "/projects")
api.add_resource(ProjectResource, "/projects/<int:project_id>")
api.add_resource(QueryProjects, "/projects/query")
api.add_resource(ProjectResults, "/projects/<int:project_id>/results")

# Single and multiple records queries for qpcrs
api.add_resource(qPCRList, "/qpcrs")
api.add_resource(qPCRResource, "/qpcrs/<int:qpcr_id>")

# Single and multiple records queries for qpcrs
api.add_resource(SampleList, "/samples")
api.add_resource(SampleResource, "/samples/<int:sample_id>")

# qPCR for each sample
api.add_resource(qPCRSampleResource, "/samples/<int:sample_id>/qpcrs")

# Import/Export functionality for proejcts
api.add_resource(ImportProject, '/projects/import')
api.add_resource(ExportProject, '/projects/export/<int:project_id>')

# Get a projects samples
api.add_resource(SamplesProjectList, "/projects/<int:project_id>/samples")

# Last project loaded by the user
api.add_resource(LastProjectResource, "/projects/lastproject")

# Dashboard information
api.add_resource(DashboardData, "/dashboard/<int:marker_id>")
api.add_resource(MarkerList, '/markers')


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
