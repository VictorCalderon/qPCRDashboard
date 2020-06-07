from flask import request, send_file, jsonify
from flask_restful import Resource
from flask_jwt_extended import jwt_required, current_user

from corona.models import Project
from corona.extensions import db, ma
from corona.commons.pagination import paginate
from corona.helpers import feed_qpcrs, export_results, feed_zip, analyze_project, dashboard_data, available_markers


class ProjectSchema(ma.SQLAlchemyAutoSchema):

    id = ma.auto_field()
    name = ma.auto_field()
    experiment_date = ma.auto_field()
    analyzed = ma.auto_field()
    observations = ma.auto_field()

    class Meta:
        model = Project
        sqla_session = db.session


class ProjectResource(Resource):
    """Single Object Resource
    """

    method_decorators = [jwt_required]

    def get(self, project_id):
        schema = ProjectSchema()
        project = Project.query.get_or_404(project_id)
        return {"project": schema.dump(project)}

    def put(self, project_id):
        schema = ProjectSchema(partial=True)
        project = Project.query.get_or_404(project_id)

        # Change name
        if request.json.get('name'):
            project.name = request.json.get('name')

        # Change experiment_date
        if request.json.get('experiment_date'):
            project.experiment_date = request.json.get('experiment_date')

        # Change analyzed to true
        if request.json.get('analyzed') == 'true':
            project.analyzed = True

        # Change analyzed to false
        if request.json.get('analyzed') == 'false':
            project.analyzed = False

        # Change observation
        if request.json.get('observations'):
            project.observations = request.json.get('observations')

        # Add project to session and commit change
        db.session.add(project)
        db.session.commit()

        return {"msg": "Experiment updated!", "project": schema.dump(project)}

    def delete(self, project_id):
        project = Project.query.get_or_404(project_id)

        if project.user_id != current_user.id:
            return {"msg": "You can only delete your own projects"}

        db.session.delete(project)
        db.session.commit()

        return {"msg": "Experiment deleted!"}


class ProjectList(Resource):
    """Creation and get all objects Resource
    """

    method_decorators = [jwt_required]

    def get(self):
        schema = ProjectSchema(many=True)
        query = Project.query.filter_by(user_id=current_user.id)
        return paginate(query, schema)

    def post(self):
        schema = ProjectSchema()
        project = Project(**schema.load(request.json))

        db.session.add(project)
        db.session.commit()

        return {"msg": "project created", "project": schema.dump(project)}, 201


class LastProjectResource(Resource):
    """Return the last project registered
    """

    method_decorators = [jwt_required]

    def get(self):
        schema = ProjectSchema()
        project = Project.query.filter_by(user_id=current_user.id).order_by(Project.id.desc()).first()
        return {'project': schema.dump(project)}


class ImportProject(Resource):
    """Import a qPCR project from raw data
    """

    method_decorators = [jwt_required]

    def post(self):

        # Get data from post
        file = request.files.get('experiment_file', None)

        # Experiment name and experiment Date
        name = request.form.get('experiment_name', None)
        date = request.form.get('experiment_date', None)
        fmt = request.form.get('experiment_format', None)

        if (name is None) or (date is None) or (file is None) or (fmt is None):
            return {'msg': 'Experiment is missing information'}, 400

        # Project instantiation
        current_project = Project(name=name, experiment_date=date, user=current_user)

        try:
            if fmt == 'QuantStudio':
                feed_zip(file, current_project, current_user)
                return {'msg': 'Project added successfully'}

            if fmt == 'ABI7500':
                feed_qpcrs(file, current_project, current_user)
                return {'msg': 'Project Successfully Added'}

            if fmt == 'default':
                raise NotImplementedError

        except NotImplementedError:
            return {'msg': 'This format option is not implemented yet!'}, 400

        except ValueError:
            return {'msg': 'Invalid format type'}, 400

        except:
            return {'msg': 'There was a problem importing your project'}, 400


class ProjectResults(Resource):
    """Get project results
    """

    method_decorators = [jwt_required]

    def get(self, project_id):
        """Get results from project.
        """

        # Get projects
        project_samples = Project.query.get_or_404(project_id).samples

        # Process data for visualization
        samples, data, statistics = analyze_project(project_samples)

        # Return processed project results
        return {'data': data, 'samples': samples, 'statistics': statistics}


class QueryProjects(Resource):
    """Query projects from database
    """

    method_decorators = [jwt_required]

    def post(self):

        # Set schema
        schema = ProjectSchema(many=True)

        # Parse params
        project_name = request.args.get('project_name')
        experiment_date = request.args.get('experiment_date')
        analyzed = request.args.get('analyzed')

        # Query db for users projects
        query = Project.query.filter_by(user_id=current_user.id)

        # Filter by date
        if analyzed:

            # Apply filter
            query = query.filter_by(analyzed=analyzed)

        # Filter by project name
        if project_name:

            # Apply filter
            query = query.filter(Project.name.like(f'%{project_name}%'))

        # Filter by date
        if experiment_date:

            # Apply filter
            query = query.filter_by(experiment_date=experiment_date)

        # Return query
        return paginate(query, schema)


class ExportProject(Resource):
    """Export project to AS
    """

    method_decorators = [jwt_required]

    def get(self, project_id):
        """Get all sample from a sigle project
        """

        # Result file
        result_file = export_results(project_id, current_user)

        # Return response
        return {'file': result_file}


class MarkerList(Resource):
    """Get a list of all my markers
    """

    method_decorators = [jwt_required]

    def get(self):
        """All markers resource
        """

        return {'markers': available_markers(current_user)}


class DashboardData(Resource):
    """Get Dashboard Results
    """

    method_decorators = [jwt_required]

    def get(self, marker_id):
        """Get Dashboard data
        """
        return dashboard_data(marker_id, current_user)
