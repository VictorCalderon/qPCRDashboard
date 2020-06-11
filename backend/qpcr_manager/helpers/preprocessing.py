"""Preprocessing module with parsing and data prep tools
"""

# Database and models
from qpcr_manager.models import Fluorescence, Experiment, Sample, Marker, Result
from qpcr_manager.extensions import db

# Utilities
from functools import lru_cache
from os import makedirs, remove
from shutil import rmtree
from glob import glob
from re import search
from uuid import uuid1
from datetime import date
from zipfile import ZipFile

# Data Structures
from collections import defaultdict, deque

# Data manipulation
import pandas as pd
import numpy as np

# Data processing pipeline
from sklearn.decomposition import PCA
from sklearn.preprocessing import StandardScaler
from sklearn.pipeline import Pipeline


def query_samples(current_user, sample):
    """Query database for samples based on sample name
    """

    # Build query
    query = f"""
    SELECT experiments.id, sample, name, marker, amp_status, amp_cq FROM experiments
    JOIN samples on samples.experiment_id = experiments.id
    JOIN results on results.sample_id = samples.id
    JOIN markers on results.marker_id = markers.id
    WHERE experiments.user_id = {current_user.id} and samples.sample like '%%{sample}%%';
    """

    # Run in pandas
    samples = pd.read_sql(query, con=db.session.bind)

    return samples.to_dict(orient='records')


def import_DA2(buffered_zip):
    """ Extract data from zipped qPCR experiment

    Arguments:
        buffered_zip {werkzeug.io} -- [A werkzeug file buffer]
    """

    # Make temporary file directory
    dir_uuid = f'/code/experiments/{uuid1()}'
    makedirs(dir_uuid)

    # Save file
    filename = dir_uuid + '/zipped_experiment.zip'
    buffered_zip.save(filename)

    # Open file
    with ZipFile(filename, 'r') as zippedObj:

        # Extract data to temporary dir_uuid folder
        zippedObj.extractall(dir_uuid)

        # Make a data container with relevant data
        data_container = {}

        # Get Results, Amplification and Sample data
        try:
            amp_data = glob(f'{dir_uuid}/*Amplification*')[0]
            results = glob(f'{dir_uuid}/*Results*')[0]

        except:
            raise ValueError('The Zip Folder must contain Amplification and Results csv')

        # Open dataframes
        amp_data = pd.read_csv(amp_data, comment='#').replace('', pd.NA).dropna()
        results = pd.read_csv(results, comment='#').replace('', pd.NA).dropna()

        # Change Undetermined to 0
        results = results.replace('Undetermined', 0)

        # Column order
        amp_data_columns = ['Well Position', 'Sample', 'Cycle Number', 'Target', 'Rn']
        results_columns = ['Well Position', 'Sample', 'Target', 'Amp Status', 'Cq', 'Cq Confidence']

        # Make them the correct datatype
        amp_data = amp_data.astype({
            'Well Position': str, 'Sample': str,
            'Cycle Number': int, 'Target': str, 'Rn': float
        })

        results = results.astype({
            'Well Position': str, 'Sample': str, 'Target': str,
            'Amp Status': str, 'Cq': float, 'Cq Confidence': float
        })

    # Remove files
    rmtree(dir_uuid, ignore_errors=True)

    return {'Amplification': amp_data[amp_data_columns], 'Results': results[results_columns]}


def import_7500(filebuffer, section_sep='\w+') -> dict:
    """Open qPCR csv file and saves each subdocument in dictionary of pandas DataFrames
    """

    # Create unique id
    file_uuid = f'/code/temp/{uuid1()}'

    # Save file
    filebuffer.save(file_uuid)

    # Re-open file
    with open(file_uuid) as file:

        # Empty dictionary and split by empty line
        data_container, data = dict(), file.read().split('\n\n')

        # Iterate over separated data(skip first)
        for d in data[1:]:

            # Remove trialing white space
            d = d.strip()

            # Split by new line
            split_data = d.split('\n')

            # First line as header (Remove non work characters)
            header = search(section_sep, split_data[0])

            # Check if header exists
            if header:

                # Extract matching subtring
                header = header.group(0)

            else:

                # Else raise error
                raise('Section delimiters before data')

            # Add header and data to container
            data_container[header] = split_data[1:]

    # Remove file from system
    remove(file_uuid)

    return data_container


def parse_7500(data_container, sep='\t'):
    """Parse qPCR data coming from a determined raw file
    """

    # Get Sample Data and instantiate dataframe
    try:
        samples = [record.split(sep) for record in data_container['Sample']]
        samples = pd.DataFrame.from_records(data=samples[1:], columns=samples[0])

    except KeyError:
        raise('[Sample Setup] header was not found in file')

    # Get qPCR data and instantiate dataframe
    try:
        qpcrs = [record.split(sep) for record in data_container['Amplification']]
        qpcrs = pd.DataFrame.from_records(data=qpcrs[1:], columns=qpcrs[0])

    except KeyError:
        raise('[Amplification Data] header not found in file')

    # Merge data
    try:
        qpcrs_with_samples = pd.merge(qpcrs, samples, how='inner', on=['Well', 'Target Name'])
    except:
        raise('Both [Sample Setup] and [Amplification Data] must share columns `Well` and `Target Name`')

    # Filter necessary data
    qs = qpcrs_with_samples[['Well', 'Cycle', 'Sample Name', 'Target Name', 'Rn']]  # 'ΔRn'

    # Remove empty spaces and NaNs
    return qs.replace('', pd.NA).dropna()


@lru_cache(maxsize=10)
def query_marker(marker_id):
    """ Query database for marker with marker id
    Args: marker_id: int
    Return: marker: str
    """

    # Get marker
    return Marker.query.get_or_404(marker_id).marker


def add_markers(markers):
    """ Take marker id from database if exists
    """

    # Markers hash
    m_hash = dict()

    # Iterate over markers
    for marker in markers:

        # Query marker
        m = Marker.query.filter_by(marker=marker).first()

        if m:
            # If exists add to m_hash
            m_hash[m.marker] = m.id

        else:
            # Add marker to database
            new_marker = Marker(marker=marker)
            db.session.add(new_marker)
            db.session.commit()

            # Add to m_hash
            m = Marker.query.filter_by(marker=marker).first()
            m_hash[m.marker] = m.id

    return m_hash


# Amp status
def amp_status(x, amp_keyword='Amp'):
    return True if x == amp_keyword else False


def feed_DA2(filebuffer, current_experiment, current_user):
    """Add DA2 ZIP experiment to database
    """

    # Import data
    data_container = import_DA2(filebuffer)

    # Extract data
    amp, results, details = data_container['Amplification'], data_container['Results'], None

    # Get unique samples
    unique_samples = results['Sample'].unique()

    # Unique markers
    unique_markers = amp['Target'].unique()

    # Get marker hash
    m_hash = add_markers(unique_markers)

    # Iterate over samples
    for sample_name in unique_samples:

        # Instantiate sample
        sample = Sample(sample=sample_name, experiment=current_experiment)

        # Mask dataframe for qPCRs
        sample_qpcrs = amp[amp['Sample'] == sample_name]

        # Iterate over qpcrs cycles
        for qpcr in sample_qpcrs.itertuples():

            # Get marker_id
            marker_id = m_hash[qpcr[4]]

            # Instantiate qPCR
            qpcr = Fluorescence(
                well=qpcr[1], cycle=qpcr[3],
                rn=qpcr[5], sample=sample, marker_id=marker_id)

        # Mask for results
        sample_results = results[results['Sample'] == sample_name]

        # Iterate over sample results
        for result in sample_results.itertuples():

            # Get marker_id
            marker_id = m_hash[result[3]]

            # Instantiate Result
            result = Result(
                amp_status=amp_status(result[4]), amp_cq=round(result[5], 3),
                cq_confidence=round(result[6], 3), marker_id=marker_id, sample=sample
            )

    # Add experiment to DB
    db.session.add(current_experiment)
    db.session.commit()


def feed_7500(filebuffer, current_experiment, current_user):
    """Add data to database
    """
    # Import data
    data_container = import_qpcr(filebuffer)

    # Parse qPCRs
    qs = parse_qpcr(data_container)

    # Get unique samples
    unique_samples = qs['Sample Name'].unique()

    # Unique Markers
    unique_markers = qs['Target Name'].unique()

    # Get M_Hash
    m_hash = add_markers(unique_markers)

    # Iterate over unique samples
    for sample_name in unique_samples:

        # Instantiate a sample
        sample = Sample(sample=sample_name, experiment=current_experiment)

        # Mask dataframe for sample qPCRS
        sample_qpcrs = qs[qs['Sample Name'] == sample_name]

        # Iterate over qpcrs
        for qpcr in sample_qpcrs.itertuples():

            # Get marker_id
            marker_id = m_hash[qpcr[4]]

            # Instantiate qPCR
            qpcr = Fluorescence(
                well=qpcr[1], cycle=qpcr[2],
                rn=qpcr[5], sample=sample, marker_id=marker_id)

    # Add experiment to DB
    db.session.add(current_experiment)
    db.session.commit()


@lru_cache(maxsize=100)
def query_fluorescence(sample_id):
    """ Query and return a parse qPCR for frontend display
    """

    # Query sample
    sample = Sample.query.get_or_404(sample_id)

    # Get qPCRs
    fluorescence = [(q.marker_id, q.cycle, q.rn) for q in sample.fluorescence]

    # Max cycles
    max_cycle = max([q[1] for q in fluorescence])

    # Container
    fluorescence_data = defaultdict(list)

    # Iterate over fluorescence tuples
    for q in fluorescence:

        # Check if key not in data
        if q[0] not in fluorescence_data.keys():
            fluorescence_data[q[0]] = [*range(max_cycle)]

        # Add data to container
        fluorescence_data[q[0]][q[1] - 1] = q[2]

    # Array of data
    fluorescence_array = []

    # Change dict key name
    for k in fluorescence_data:

        # Query db for key
        fluorescence_array.append({
            'marker': query_marker(k),
            'amp': fluorescence_data[k],
            'well': sample.fluorescence[0].well
        })

    return sorted(fluorescence_array, key=lambda x: x['marker'])


def export_results(experiment_id, current_user):
    """Export experiment
    """

    try:
        query = f"""
        SELECT sample, marker, amp_status, amp_cq FROM experiments
        JOIN samples on samples.experiment_id = experiments.id
        JOIN results on results.sample_id = samples.id
        JOIN markers on results.marker_id = markers.id
        WHERE experiments.user_id = {current_user.id} and experiments.id = {experiment_id};
        """

        # Get results
        query = db.session.execute(query)
        # experiment = Experiment.query.filter_by(user_id=current_user.id, id=experiment_id).first()

        if query is None:
            raise ValueError('This experiment could not be exported')

        def bool_to_string(x): return 'Amp' if x else 'No Amp'

        # Get results (samples, results)
        results = [[q[0], q[1], bool_to_string(q[2]), str(q[3])] for q in query]

    except:
        raise ValueError('You can only export your own experiments')

    # Merge into a single string
    stringed_results = [','.join(x) + '\n' for x in results]

    # One big string
    return ''.join(stringed_results)


def experiment_statistics(experiment_samples):
    """Analyze experiment
    """

    # Set column names
    column_names = ['sample', 'marker', 'amp_status', 'amp_cq', 'cq_confidence']

    # Get records from set
    records = deque()

    # Iterate over query
    for s in experiment_samples:

        # Iterate over results
        for r in s.results:

            # Add result to records
            records.append([s.sample, r.marker_id, r.amp_status, r.amp_cq, r.cq_confidence])

    # Build dataframe from deque
    results = pd.DataFrame.from_records(records)

    # Set columns
    results.columns = column_names

    # Get marker name
    results['marker'] = results['marker'].apply(query_marker)

    # Get ordered markers
    markers = list(results['marker'].unique())

    # Build extended Cq dataframe
    results_df = results.pivot_table(index='sample', columns='marker', values='amp_cq').reset_index()

    # Get samples
    samples = list(results_df.pop('sample'))

    # Lower dimensions of more than 2 markers

    # Build PCA pipeline
    pipe = Pipeline([('scaler', StandardScaler()),
                     ('reducer', PCA(n_components=2))])

    # Process cq matrix
    pca = pipe.fit_transform(results_df)

    # Add PCA components to dataframe
    results_df['PCA 1'] = np.round(pca[:, 0], 4)
    results_df['PCA 2'] = np.round(pca[:, 1], 4)

    # Data
    cq_raw = results_df.to_dict('list')

    # Count amplifications
    amp_status = results.groupby('marker')['amp_status'].agg([np.mean, np.sum]).reset_index().to_dict('records')
    amped_cq = results[results['amp_status'] > 0].groupby('marker')['amp_cq'].agg(
        [np.mean, np.std]).reset_index().to_dict('records')

    # Jsonify results
    return {'samples': samples, 'cq_raw': cq_raw, 'amp_status': amp_status, 'amped_cq': amped_cq}


def available_markers(current_user):
    """Return a list of all available markers
    """

    query = f"""
    SELECT DISTINCT(m.id)
    FROM samples AS s
    JOIN experiments AS p on s.experiment_id = p.id
    JOIN results AS r on r.sample_id = s.id
    JOIN markers as m on r.marker_id = m.id
    WHERE p.user_id = {current_user.id}
    """

    # Run query
    markers = db.session.execute(query)

    # Clean markers
    markers = [[m.id, query_marker(m.id)] for m in markers]

    # Return marker list
    return markers


def amped_timeseries(marker_id, current_user):
    """Query dashboard data (date, perc_cases, total_samples, total_experiments)
    """

    # [SUGGESTION] (preprocessing.py) This should be a postgreSQL view
    my_query = f"""
    SELECT date, CAST(COUNT(CASE WHEN amp_status THEN 1 END) as decimal) / COUNT(amp_status), COUNT(DISTINCT(sample)), COUNT(DISTINCT(name))
    FROM samples AS s
    JOIN experiments as p on s.experiment_id = p.id
    JOIN results as r on r.sample_id = s.id
    JOIN markers as m on r.marker_id = m.id
    WHERE m.id = {marker_id} AND p.user_id = {current_user.id}
    GROUP BY date
    """

    # Run query
    data = db.session.execute(my_query)

    # Parse data
    data = [(str(d[0]), round(float(d[1]), 2), d[2], d[3]) for d in data]

    # Insert into dataframe
    data = pd.DataFrame(data=data, columns=['Date', 'Amp Fraction', 'Total Samples', 'Total Experiments'])

    # Return data
    return data.to_dict('list')
