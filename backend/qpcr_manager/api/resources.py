from flask import request
from flask_restful import Resource
from flask_jwt_extended import jwt_required, current_user

from qpcr_manager.models import *
from qpcr_manager.helpers import *
from qpcr_manager.extensions import ma, db
from qpcr_manager.commons.pagination import paginate


class UserSchema(ma.SQLAlchemyAutoSchema):

    id = ma.Int(dump_only=True)
    password = ma.String(load_only=True, required=True)

    class Meta:
        model = User
        sqla_session = db.session


class UserResource(Resource):
    """Single object resource
    """

    method_decorators = [jwt_required]

    def get(self, user_id):
        schema = UserSchema()
        user = User.query.get_or_404(user_id)
        return {"user": schema.dump(user)}

    def put(self, user_id):
        schema = UserSchema(partial=True)
        user = User.query.get_or_404(user_id)
        user = schema.load(request.json, instance=user)

        db.session.commit()

        return {"msg": "user updated", "user": schema.dump(user)}

    def delete(self, user_id):
        user = User.query.get_or_404(user_id)
        db.session.delete(user)
        db.session.commit()

        return {"msg": "user deleted"}


class UserList(Resource):
    """Creation and get_all
    """

    def post(self):
        schema = UserSchema()
        user = schema.load(request.json)

        db.session.add(user)
        db.session.commit()

        return {"msg": "We've sent you an Email to complete your registration"}, 201


class ExperimentSchema(ma.SQLAlchemyAutoSchema):

    id = ma.auto_field()
    name = ma.auto_field()
    date = ma.auto_field()
    analyzed = ma.auto_field()
    observations = ma.auto_field()
    tags = ma.auto_field()

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

        # Change date
        if request.json.get('date'):
            experiment.date = request.json.get('date')

        # Change analyzed to true
        if request.json.get('analyzed') == True:
            experiment.analyzed = True

        # Change analyzed to false
        if request.json.get('analyzed') == False:
            experiment.analyzed = False

        # Change observations
        if request.json.get('observations'):
            experiment.observations = request.json.get('observations')

        # Changes or add tags
        if request.json.get('tags'):
            experiment.tags = ';'.join(request.json.get('tags'))

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
        file = request.files.get('file', None)

        # Experiment name and experiment Date
        name = request.form.get('name', None)
        date = request.form.get('date', None)
        observations = request.form.get('observations', None)
        fmt = request.form.get('format', None)

        if (name is None) or (date is None) or (file is None) or (fmt is None):
            return {'msg': 'Experiment is missing information'}, 400

        # Experiment instantiation
        current_experiment = Experiment(name=name, date=date, user=current_user, observations=observations)

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

        # Return processed experiment results
        return experiment_statistics(experiment_id, current_user)


class ExperimentsQuery(Resource):
    """Query experiments from database
    """

    method_decorators = [jwt_required]

    def post(self):

        # Set schema
        schema = ExperimentSchema(many=True)

        # Parse params
        name = request.args.get('name', None)
        date = request.args.get('date', None)
        analyzed = request.args.get('analyzed', None)
        observations = request.args.get('observations', None)

        # Query db for users experiments
        query = Experiment.query.filter_by(user_id=current_user.id).order_by(Experiment.id.desc())

        # Filter by date
        if analyzed:

            # Apply filter
            query = query.filter_by(analyzed=analyzed)

        # Filter by experiment name
        if name:

            # Apply filter
            query = query.filter(Experiment.name.like(f'%{name}%'))

        # Filter by date
        if date:

            # Apply filter
            query = query.filter_by(date=date)

        # Filter by date
        if observations:

            # Apply filter
            query = query.filter_by(observations=observations)

        # Return query
        return paginate(query, schema)


class ExportExperiment(Resource):
    """Export experiment data and results as a csv file
    """

    method_decorators = [jwt_required]

    def get(self, experiment_id):
        """Get all sample from a sigle experiment
        """

        # Define parameters
        sep = request.args.get('sep', ',')
        columns = request.args.get('columns', None)

        # Parse columns
        if columns:
            columns = columns.split(',')

        # Result file
        result_file = export_results(experiment_id, current_user, params={'sep': sep, 'columns': columns})

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


class AmplificationTimeSeriesResource(Resource):
    """Get Overview of Experiment Results
    """

    method_decorators = [jwt_required]

    def get(self):
        """Query for such data
        """

        # Get query configuration
        marker_id = request.args.get('marker_id')

        return amped_timeseries(marker_id, current_user)


class MarkerSpecificDataset(Resource):
    """Get a marker specific dataset
    """

    method_decorators = [jwt_required]

    def get(self):
        """Download specific dataset
        """

        # Get marker
        marker_id = request.args.get('marker_id', None)

        # Check for errors
        if None:
            return {'msg': 'Marker id required'}, 400

        # Get dataset
        return {'file': marker_dataset(marker_id, current_user)}


class SampleSchema(ma.SQLAlchemyAutoSchema):

    id = ma.auto_field()
    sample = ma.auto_field()
    experiment_id = ma.auto_field()

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


class SamplesQuery(Resource):
    """Query samples from database
    """

    method_decorators = [jwt_required]

    def post(self):

        # Parse params
        sample = request.args.get('sample')

        # Run query and return data
        return query_samples(current_user, sample)


class ExperimentSamplesList(Resource):
    """Get all samples from a certain experiment
    """

    method_decorators = [jwt_required]

    def get(self, experiment_id):
        schema = SampleSchema(many=True)
        samples = Sample.query.filter_by(
            experiment_id=experiment_id).order_by('id')
        return {'samples': schema.dump(samples)}


class SampleFluorescenceResource(Resource):
    """Get patients Fluorescence data
    """

    method_decorators = [jwt_required]

    def get(self, sample_id):
        """Get a single patient's raw Fluorescence data
        """
        fluorescence_data = query_fluorescence(sample_id)
        return {'fluorescence_data': fluorescence_data}


class ProjectBrief(Resource):
    """Get Project Briefing of amount of experiments and samples performed
    """

    method_decorators = [jwt_required]

    def get(self):
        """Return a two element list with total experiments and samples processed by mode (daily: 1, all-time: 0)
        """
        return get_brief()


class AmpStatData(Resource):
    """Get amplification data from experiments
    """

    method_decorators = [jwt_required]

    def get(self):
        """Time-based amplification status from each sample"""

        return amp_stat_data()


class TagDistribution(Resource):
    """Get tag distribution from experiments
    """

    method_decorators = [jwt_required]

    def get(self):
        return tag_distrib()


class LocationSchema(ma.SQLAlchemyAutoSchema):

    id = ma.Int(dump_only=True)
    name = ma.String(required=True)
    latitude = ma.String(required=True)
    longitude = ma.String(required=True)
    color = ma.String(required=True)

    class Meta:
        model = Location
        sqla_session = db.session


class LocationList(Resource):
    """Sample location manipulation
    """

    method_decorators = [jwt_required]

    def get(self):
        schema = LocationSchema(many=True)
        locations = Location.query.filter_by(user_id=current_user.id).order_by('id')
        return schema.dump(locations)

    def post(self):

        # Grab locations from request
        locations = request.args.get('locations')

        # Make necessary changes and what not
        rv = location_moficiations(locations)

        if (rv):
            return {'msg': 'Modification successful'}, 201

        else:
            return {'msg': 'Modification unsucessful'}, 400


# Wilcard export overwrite
__all__ = [
    'UserResource', 'UserList',
    'ExperimentResource', 'ExperimentList', 'LastExperimentResource',
    'ExperimentsQuery', 'ExperimentResults', 'ExperimentSamplesList',
    'SampleResource', 'SampleList', 'SampleFluorescenceResource', 'SamplesQuery',
    'ImportExperiment', 'ExportExperiment', 'AmplificationTimeSeriesResource',
    'MarkerList', 'MarkerSpecificDataset', 'ProjectBrief', 'AmpStatData', 'TagDistribution',
    'LocationList'
]
