from flask import request, jsonify
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
            experiment.tags = ','.join(request.json.get('tags'))

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
        expfile = request.files.get('file', None)

        # Experiment name and experiment Date
        name = request.form.get('name', 'DefaultName')
        date = request.form.get('date', '1996-05-25')

        # Experiment tags
        tags = request.form.get('tags', None)
        if isinstance(tags, list):
            tags = ';'.join(tags)

        fmt = request.form.get('format', None)

        # Check if required data is not present
        if (expfile is None) or (fmt is None):
            return {'msg': 'Experiment is missing information'}, 400

        # Experiment instantiation
        current_experiment = Experiment(name=name, date=date, user=current_user, tags=tags)

        try:
            if fmt == 'ds2':
                load_DA2(expfile, current_experiment)
                return {'msg': 'Experiment added successfully'}

            if fmt == '7500':
                load_7500(expfile, current_experiment)
                return {'msg': 'Experiment Added Successfully'}

            if fmt == 'q2000':
                load_q2000(expfile, current_experiment)
                return {'msg': 'Experiment Added Successfully'}

            if fmt == 'default':
                raise NotImplementedError

        except NotImplementedError:
            return {'msg': 'This format option is not implemented yet!'}, 400

        except ValueError:
            return {'msg': 'Invalid Format'}, 400

        except TypeError:
            return {'msg': 'There was a problem importing your experiment'}, 400

        except AssertionError as e:
            return {'msg': str(e)}, 400

        except BadZipFile:
            return {'msg': 'File must be zipped'}, 400

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


class MarkerSchema(ma.SQLAlchemyAutoSchema):

    id = ma.Int(dump_only=True)
    marker = ma.String(required=True)
    target_id = ma.String(required=True)

    class Meta:
        model = Marker
        sqla_session = db.session


class MarkerList(Resource):
    """Get a list of all my markers
    """

    method_decorators = [jwt_required]

    def get(self):
        """All markers resource"""

        # Get available markers
        return available_markers()

    def post(self):
        """Modify markers"""

        # Load schema
        schema = MarkerSchema(many=True)

        # Check if already in database
        old_markers = request.json.get('markers', None)

        if old_markers:

            # Iterate over markers
            for marker in old_markers:

                # Search for old Marker
                marker_ = Marker.query.get_or_404(marker.pop('id'))

                # Run modifications
                for k, v in marker.items():
                    setattr(marker_, k, v)

                # Commit modifications
                db.session.add(marker_)
                db.session.commit()

            return {"msg": "markers modified", "markers": schema.dump(old_markers)}, 201

        else:

            # No markers sent
            return {"msg": "No markers sent"}, 400


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


class LocationSchema(ma.SQLAlchemyAutoSchema):

    id = ma.Int(dump_only=True)
    location = ma.String(required=True)
    latitude = ma.Float(required=True)
    longitude = ma.Float(required=True)
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

        # Load schema
        schema = LocationSchema()

        # Check if already in database
        old_id = request.json.get('id', None)

        if old_id:

            # Get location
            location = Location.query.get_or_404(old_id)

            # Run modifications
            for k, v in request.json.items():
                setattr(location, k, v)

            # Commit modification
            db.session.add(location)
            db.session.commit()

            return {"msg": "location modified", "location": schema.dump(location)}, 201

        else:

            # Location schema
            location = Location(**request.json)

            # Add user
            location.user_id = current_user.id

            db.session.add(location)
            db.session.commit()

            return {"msg": "location created", "location": schema.dump(location)}, 201


class TargetSchema(ma.SQLAlchemyAutoSchema):

    id = ma.Int(dump_only=True)
    name = ma.String(required=True)
    key = ma.String(required=True)
    description = ma.String(required=True)

    class Meta:
        model = Target
        sqla_session = db.session


class TargetList(Resource):
    """Sample target modification and multiple entries query
    """

    method_decorators = [jwt_required]

    def get(self):
        schema = TargetSchema(many=True)
        targets = Target.query.filter_by(user_id=current_user.id).order_by('id')
        return schema.dump(targets)

    def post(self):

        # Load schema
        schema = TargetSchema()

        # Check if already in database
        old_id = request.json.get('id', None)

        if old_id:

            # Get target
            target = Target.query.get_or_404(old_id)

            # Run modifications
            for k, v in request.json.items():
                setattr(target, k, v)

            # Commit modification
            db.session.add(target)
            db.session.commit()

            return {"msg": "target modified", "target": schema.dump(target)}, 201

        else:

            # Target schema
            target = Target(**request.json)

            # Add user
            target.user_id = current_user.id

            db.session.add(target)
            db.session.commit()

            return {"msg": "target created", "target": schema.dump(target)}, 201


class TargetResource(Resource):
    """Single resource for targets
    """

    def delete(self, target_id):

        # Run delete
        target = Target.query.get_or_404(target_id)
        db.session.delete(target)
        db.session.commit()

        # Return message
        return {"msg": "target deleted"}, 204


class LocationResource(Resource):
    """ Single resource for locations
    """

    method_decorators = [jwt_required]

    def delete(self, location_id):
        location = Location.query.get_or_404(location_id)
        db.session.delete(location)
        db.session.commit()

        return {"msg": "location deleted"}, 204


class LocatedSamples(Resource):
    """ Locate samples within the map thought locations and sample name
    """

    method_decorators = [jwt_required]

    def get(self):
        """Count samples per sampling site
        """

        # Run location function
        located_samples = get_located_samples()

        # Return data
        return located_samples


class ExperimentSamplesList(Resource):
    """Get all samples from a certain experiment
    """

    method_decorators = [jwt_required]

    def get(self, experiment_id):
        schema = SampleSchema(many=True)
        samples = Sample.query.filter_by(experiment_id=experiment_id).order_by('id')
        return {'samples': schema.dump(samples)}


class ExperimentFluorescenceList(Resource):
    """Get patients fluorescence data
    """

    method_decorators = [jwt_required]

    def get(self, experiment_id):
        """Get a single patient's raw Fluorescence data
        """
        fluorescence_data = experiment_fluorescences(experiment_id)
        return {'fluorescence_data': fluorescence_data}


class ExperimentSampleTable(Resource):
    """Get all samples from an experiment with their results
    """

    method_decorators = [jwt_required]

    def get(self, experiment_id):
        """Get samples from experiment"""

        return {'samples': sample_table(experiment_id)}


class ExperimentMaxGradient(Resource):
    """Compute the maximum gradient and respective cycle of a project
    """

    method_decorators = [jwt_required]

    def get(self, experiment_id):
        """Get grads and cycles
        """

        return maximum_gradient(experiment_id)


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

        return jsonify(amp_stat_data())


class ExperimentPCA(Resource):
    """Experiment results PCA based on amplification cycle
    """

    method_decorators = [jwt_required]

    def get(self, experiment_id):
        """Principal Component Analysis of Threshold Cycle data
        """

        try:
            return experiment_pca_kmeans(experiment_id)

        except AssertionError:
            return {'msg': 'Duplicate sample/marker pairs found in your experiment.'}, 400

        except:
            raise RuntimeError('ExperimentPCA analysis failed.')


class TagDistribution(Resource):
    """Get tag distribution from experiments
    """

    method_decorators = [jwt_required]

    def get(self):
        return tag_distrib()


# Wilcard export overwrite
__all__ = [
    'UserResource', 'UserList',
    'ExperimentResource', 'ExperimentList', 'LastExperimentResource',
    'ExperimentsQuery', 'ExperimentResults', 'ExperimentSamplesList',
    'SampleResource', 'SampleList', 'SamplesQuery', 'ExperimentPCA',
    'ImportExperiment', 'AmplificationTimeSeriesResource',
    'MarkerList', 'MarkerSpecificDataset', 'ProjectBrief', 'AmpStatData', 'TagDistribution',
    'LocatedSamples', 'LocationList', 'LocationResource', 'ExperimentSampleTable', 'ExperimentFluorescenceList',
    'TargetList', 'TargetResource', 'ExperimentMaxGradient'
]
