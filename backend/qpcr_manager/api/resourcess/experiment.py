from flask import request, send_file, jsonify
from flask_restful import Resource
from flask_jwt_extended import jwt_required, current_user

from qpcr_manager.models import Experiment
from qpcr_manager.extensions import db, ma
from qpcr_manager.commons.pagination import paginate
from qpcr_manager.helpers import feed_DA2, feed_7500, export_results, analyze_experiment, dashboard_data, available_markers


class ExperimentSchema(ma.SQLAlchemyAutoSchema):

    id = ma.auto_field()
    name = ma.auto_field()
    experiment_date = ma.auto_field()
    analyzed = ma.auto_field()
    observations = ma.auto_field()

    class Meta:
        model = Experiment
        sqla_session = db.session


class ExperimentResource(Resource):
    """Single Object Resource
    """

    method_decorators = [jwt_required]

    def get(self, experiment_id):
        schema = ExperimentSchema()
        experiment = Experiment.query.get_or_404(experiment_id)
        return {"experiment": schema.dump(experiment)}

    def put(self, experiment_id):
        schema = ExperimentSchema(partial=True)
        experiment = Experiment.query.get_or_404(experiment_id)

        # Change name
        if request.json.get('name'):
            experiment.name = request.json.get('name')

        # Change experiment_date
        if request.json.get('experiment_date'):
            experiment.experiment_date = request.json.get('experiment_date')

        # Change analyzed to true
        if request.json.get('analyzed') == 'true':
            experiment.analyzed = True

        # Change analyzed to false
        if request.json.get('analyzed') == 'false':
            experiment.analyzed = False

        # Change observation
        if request.json.get('observations'):
            experiment.observations = request.json.get('observations')

        # Add experiment to session and commit change
        db.session.add(experiment)
        db.session.commit()

        return {"msg": "Experiment updated!", "experiment": schema.dump(experiment)}

    def delete(self, experiment_id):
        experiment = Experiment.query.get_or_404(experiment_id)

        if experiment.user_id != current_user.id:
            return {"msg": "You can only delete your own experiments"}

        db.session.delete(experiment)
        db.session.commit()

        return {"msg": "Experiment deleted!"}


class ExperimentList(Resource):
    """Creation and get all objects Resource
    """

    method_decorators = [jwt_required]

    def get(self):
        schema = ExperimentSchema(many=True)
        query = Experiment.query.filter_by(user_id=current_user.id)
        return paginate(query, schema)

    def post(self):
        schema = ExperimentSchema()
        experiment = Experiment(**schema.load(request.json))

        db.session.add(experiment)
        db.session.commit()

        return {"msg": "experiment created", "experiment": schema.dump(experiment)}, 201


class LastExperimentResource(Resource):
    """Return the last experiment registered
    """

    method_decorators = [jwt_required]

    def get(self):
        schema = ExperimentSchema()
        experiment = Experiment.query.filter_by(user_id=current_user.id).order_by(Experiment.id.desc()).first()
        return {'experiment': schema.dump(experiment)}


class ImportExperiment(Resource):
    """Import a qPCR experiment from raw data
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

        # Experiment instantiation
        current_experiment = Experiment(name=name, experiment_date=date, user=current_user)

        try:
            if fmt == 'DA2':
                feed_DA2(file, current_experiment, current_user)
                return {'msg': 'Experiment added successfully'}

            if fmt == '7500':
                feed_7500(file, current_experiment, current_user)
                return {'msg': 'Experiment Successfully Added'}

            if fmt == 'default':
                raise NotImplementedError

        except NotImplementedError:
            return {'msg': 'This format option is not implemented yet!'}, 400

        except ValueError:
            return {'msg': 'Invalid format type'}, 400

        except:
            return {'msg': 'There was a problem importing your experiment'}, 400


class ExperimentResults(Resource):
    """Get experiment results
    """

    method_decorators = [jwt_required]

    def get(self, experiment_id):
        """Get results from experiment.
        """

        # Get experiments
        experiment_samples = Experiment.query.get_or_404(experiment_id).samples

        # Process data for visualization
        samples, data, statistics = analyze_experiment(experiment_samples)

        # Return processed experiment results
        return {'data': data, 'samples': samples, 'statistics': statistics}


class QueryExperiments(Resource):
    """Query experiments from database
    """

    method_decorators = [jwt_required]

    def post(self):

        # Set schema
        schema = ExperimentSchema(many=True)

        # Parse params
        experiment_name = request.args.get('experiment_name')
        experiment_date = request.args.get('experiment_date')
        analyzed = request.args.get('analyzed')

        # Query db for users experiments
        query = Experiment.query.filter_by(user_id=current_user.id)

        # Filter by date
        if analyzed:

            # Apply filter
            query = query.filter_by(analyzed=analyzed)

        # Filter by experiment name
        if experiment_name:

            # Apply filter
            query = query.filter(Experiment.name.like(f'%{experiment_name}%'))

        # Filter by date
        if experiment_date:

            # Apply filter
            query = query.filter_by(experiment_date=experiment_date)

        # Return query
        return paginate(query, schema)


class ExportExperiment(Resource):
    """Export experiment to AS
    """

    method_decorators = [jwt_required]

    def get(self, experiment_id):
        """Get all sample from a sigle experiment
        """

        # Result file
        result_file = export_results(experiment_id, current_user)

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
