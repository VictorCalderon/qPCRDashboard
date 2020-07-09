"""Preprocessing module with parsing and data prep tools
"""

# Database and models
from qpcr_manager.models import *
from flask_jwt_extended import current_user
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
from collections import defaultdict, deque, Counter

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
    return pd.read_sql(query, con=db.session.bind).to_dict(orient='records')


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

    try:

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
            results_columns = ['Well Position', 'Sample', 'Target', 'Amp Status', 'Cq']

            # Make them the correct datatype
            amp_data = amp_data.astype({
                'Well Position': str, 'Sample': str,
                'Cycle Number': int, 'Target': str, 'Rn': float
            })

            results = results.astype({
                'Well Position': str, 'Sample': str, 'Target': str,
                'Amp Status': str, 'Cq': float
            })

    except:
        raise 'Data could not be parsed'

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
        results = [record.split(sep) for record in data_container['Results']]
        results = pd.DataFrame.from_records(data=results[1:], columns=results[0])

    except KeyError:
        raise('[Sample Setup] header was not found in file')

    # Get qPCR data and instantiate dataframe
    try:
        amp = [record.split(sep) for record in data_container['Amplification']]
        amp = pd.DataFrame.from_records(data=amp[1:], columns=amp[0])

    except KeyError:
        raise('[Amplification Data] header not found in file')

    # Merge data
    try:
        amp_with_results = pd.merge(amp, results, how='inner', on=['Well', 'Target Name'])

    except:
        raise('Both [Results] and [Amplification Data] must share columns `Well` and `Target Name`')

    # Filter necessary data
    amp = amp_with_results[['Well', 'Sample Name', 'Cycle', 'Target Name', 'Rn']]  # 'ΔRn'

    # Remove empty spaces
    amp = amp.replace('', pd.NA).dropna()

    # Change amp dtype
    amp = amp.astype({
        'Well': str, 'Sample Name': str,
        'Cycle': int, 'Target Name': str, 'Rn': float
    })

    # Change amp column names for consistency
    amp.columns = ['Well Position', 'Sample', 'Cycle Number', 'Target', 'Rn']

    # Extract columns from results
    results = results[['Well', 'Sample Name', 'Target Name', 'Cт']]

    # Change Undetermined to 0
    results = results.replace('Undetermined', 0)

    # Remove empty spaces
    results = results.replace('', pd.NA).dropna()

    # Generate Amplification Status column
    amp_status = results['Cт'].astype('float').apply(lambda x: 'Amp' if x > 0 else 'No Amp')

    # Insert into dataframe
    results.insert(3, 'Amp Status', amp_status)

    # Rename columns for consistency
    results.columns = ['Well Position', 'Sample', 'Target', 'Amp Status', 'Cq']

    # Change dtypes
    results = results.astype({'Well Position': str, 'Sample': str, 'Target': 'category',
                              'Amp Status': 'category', 'Cq': float})

    # Remove empty spaces and NaNs and
    return amp, results


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
                amp_status=amp_status(result[4]), amp_cq=round(result[5], 3), marker_id=marker_id, sample=sample
            )

    # Add experiment to DB
    db.session.add(current_experiment)
    db.session.commit()


def feed_7500(filebuffer, current_experiment, current_user):
    """Add data to database
    """
    # Import data
    data_container = import_7500(filebuffer)

    # Parse Fluorescence and Results
    amp, results = parse_7500(data_container)

    # Get unique samples
    unique_samples = results['Sample'].unique()

    # Unique Markers
    unique_markers = results['Target'].unique()

    # Get Marker Hash
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
                amp_status=amp_status(result[4]), amp_cq=round(result[5], 3), marker_id=marker_id, sample=sample
            )

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


def export_results(experiment_id, current_user, params={'sep': ','}):
    """Export experiment
    """

    try:
        query = f"""
        SELECT name, date, sample, marker, amp_status, amp_cq FROM experiments
        JOIN samples on samples.experiment_id = experiments.id
        JOIN results on results.sample_id = samples.id
        JOIN markers on results.marker_id = markers.id
        WHERE experiments.user_id = {current_user.id} and experiments.id = {experiment_id};
        """

        # Get results
        query = pd.read_sql(query, db.session.bind)

        if query is None:
            raise ValueError('This experiment could not be exported')

    except:
        raise ValueError('You can only export your own experiments')

    # Set Amplification Name
    query['amp_status'] = query['amp_status'].apply(lambda x: 'Amp' if x else 'No Amp')

    # Apply to queried df
    return query.to_csv(index=False, sep=params['sep'])


def experiment_statistics(experiment_id, current_user):
    """Analyze experiment
    """

    # Write query
    query = f"""
    SELECT sample, marker, amp_status, amp_cq FROM samples
    JOIN experiments on samples.experiment_id = experiments.id
    JOIN results on results.sample_id = samples.id
    JOIN markers on results.marker_id = markers.id
    WHERE experiments.user_id = {current_user.id} AND experiments.id = {experiment_id}
    """

    # Run query on pandas
    results = pd.read_sql(query, db.session.bind)

    # Build extended Cq dataframe
    results_df = results.pivot_table(
        index='sample', columns='marker', values='amp_cq').reset_index()

    amped_df = results.pivot_table(
        index='sample', columns='marker', values='amp_status').to_dict('list')

    # Remove controls
    results_df = results_df.dropna()

    # Get samples
    samples = list(results_df.pop('sample'))

    # Build PCA pipeline
    pipe = Pipeline([('scaler', StandardScaler()),
                     ('reducer', PCA(n_components=2))])

    # Process cq matrix
    pca = pipe.fit_transform(results_df)

    # Add PCA components to dataframe
    results_df['PCA 1'] = np.round(pca[:, 0], 4)
    results_df['PCA 2'] = np.round(pca[:, 1], 4)

    # [SUGGESTION] preprocessing.py Find a better way of dealing with this
    # Data
    cq_raw = results_df.to_dict('list')

    # Count amplifications
    amp_status = results.groupby('marker')['amp_status'].agg([np.mean, np.sum]).reset_index().to_dict('records')
    amped_cq = results[results['amp_status'] > 0]
    amped_cq = amped_cq.groupby('marker')['amp_cq'].agg([np.mean, np.std]).reset_index().to_dict('records')

    # Jsonify results
    return {'samples': samples, 'cq_raw': cq_raw, 'amp_status': amp_status, 'amped_cq': amped_cq, 'amp_raw': amped_df}


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
    query = f"""
    SELECT date, CAST(COUNT(CASE WHEN amp_status THEN 1 END) as decimal) / COUNT(amp_status), COUNT(DISTINCT(sample)), COUNT(DISTINCT(name))
    FROM samples AS s
    JOIN experiments as p on s.experiment_id = p.id
    JOIN results as r on r.sample_id = s.id
    JOIN markers as m on r.marker_id = m.id
    WHERE m.id = {marker_id} AND p.user_id = {current_user.id}
    GROUP BY date
    """

    # Run query
    data = db.session.execute(query)

    # Parse data
    data = [(str(d[0]), round(float(d[1]), 2), d[2], d[3]) for d in data]

    # Insert into dataframe
    data = pd.DataFrame(data=data, columns=['Date', 'Amp Fraction', 'Total Samples', 'Total Experiments'])

    # Return data
    return data.to_dict('list')


def marker_dataset(marker_id, current_user):
    """Query dashboard data (date, perc_cases, total_samples, total_experiments)
    """

    # [SUGGESTION] (preprocessing.py) This should be a postgreSQL view
    query = f"""
    SELECT name, date, methodology, sample, amp_status, amp_cq
    FROM samples AS s
    JOIN experiments as p on s.experiment_id = p.id
    JOIN results as r on r.sample_id = s.id
    JOIN markers as m on r.marker_id = m.id
    WHERE m.id = {marker_id} AND p.user_id = {current_user.id}
    """

    # Run query in pandas
    dataset = pd.read_sql(query, db.session.bind)

    # Make Amp Status Binary
    dataset['amp_status'] = dataset['amp_status'].apply(lambda x: 1 if x else 0)

    # Return dataset as a csv
    return dataset.to_csv(index=False)


def get_brief():
    """Count the number of experiments and samples processed
    """

    query = f"""
    SELECT s.sample, e.name FROM samples AS s
    JOIN experiments AS e ON s.experiment_id = e.id
    WHERE e.user_id = {current_user.id}
    """

    # Run query
    dataset = pd.read_sql(query, db.session.bind)

    # Make unique
    exps, samples = len(dataset['name'].unique()), len(dataset['sample'])

    # Return dataset
    return {"experiments": exps, "samples": samples}


def amp_stat_data():
    """ Return the following data structure:
        {
            labels: ["26 Jun", "27 Jun", "28 Jun", "29 Jun"],
            datasets: [
                {
                    label: "Marker 1",
                    data: [19, 18, 19, 22]
                },
                {
                    label: 'Marker 2',
                    data: [21, 23, 27, 26],
                },
                {
                    label: 'Marker 3',
                    data: [99, 98, 99, 99],
                }, ...
            ]
        }

        The order of datasets must be decreasing by mean data
    """

    # Prepare query
    query = f"""
        SELECT date, sample, amp_status, amp_cq, marker
        FROM samples
        JOIN experiments ON experiments.id = samples.experiment_id
        JOIN results ON results.sample_id = samples.id
        JOIN markers ON results.marker_id = markers.id
        WHERE experiments.user_id = {current_user.id}
        """

    # Run query
    dataset = pd.read_sql(query, db.session.bind)

    # Parse date as datetime
    dataset['date'] = pd.to_datetime(dataset['date'])

    # # Resample if length is >100 days
    # if len(dataset) > 2:

    #     # Run resample
    #     dataset = dataset.resample('W', on='date')['amp_status'].mean().reset_index()

    # Group by date and marker and calculate amplification (binary mean) percentages
    dataset = dataset.groupby(['date', 'marker'])['amp_status'].mean().reset_index()

    # Parse dates
    dataset['day'] = dataset['date'].dt.day
    dataset['month'] = dataset['date'].dt.month_name()

    # Make then pretty
    dataset['day-month'] = dataset['day'].astype(str) + '-' + dataset['month'].astype(str)

    # Instantiate data struct [{'marker': 'example 1, 'data': [1, 2, 3]}]
    datasets = []

    # Generate parsed dataset
    for marker in dataset['marker'].unique():

        # Mask dataset to keep marker specific
        df = dataset[dataset['marker'] == marker]

        # Get dataset
        percs = df['amp_status'] * 100

        # Add data to struct
        datasets.append({'marker': marker, 'data': percs.to_list()})

    # Sort list of dictionaries
    datasets = sorted(datasets, key=lambda i: np.mean(i['data']))

    # Use last iteration day-month column
    return {'dates': df['day-month'].to_list(), 'datasets': datasets}


def tag_distrib():
    """ Return the following data structure:
        {
            labels: ["Tag1", "Tag2", "Tag3", "Tag4"],
            dataset: [2000, 1232, 1232, 412, 10]
            ]
        }

        dataset order: decreasing
    """

    # Prepare query
    query = f"""
    SELECT tags FROM experiments
    WHERE experiments.user_id = {current_user.id}
    """

    # Run query with pandas
    dataset = pd.read_sql(query, db.session.bind)

    # Get split list of lists
    tags = [t.split(';') for t in dataset['tags']]

    # Flatten tags
    tags = [item for sublist in tags for item in sublist]

    # Count data
    tag_counter = Counter(tags)

    # Sorted count data
    tag_counter = dict(tag_counter.most_common(len(tag_counter.keys())))

    return {'labels': list(tag_counter.keys()), 'dataset': list(tag_counter.values())}


def location_moficiations(locations):
    """Manipulate location data from a single user
    """

    # Iterate over locations
    for loc in locations:

        # Get location id
        loc_id = loc.get('id', 0)

        if loc_id:

            # Query that specific entry
            location_entry = Location.query.get_or_404(loc_id)

            # Change all values
            for k in loc:
                setattr(location_entry, k, loc[k])

        # If new
        else:

            # Add to database
            new_loc = Location(**loc)
            db.session.add(new_loc)

    # Commit changes
    db.session.commit()

    return 1


def get_located_samples():
    """ Combine sample name data to map each sample to a sampling site
        Output format:

        [
            {
                'loc': [18.4358, -69.9853],
                'name': "Sede Central",
                'totalSamples': 19800,
                'bgColor': '#C81D25'
            },
            ...
        ]

    """

    # Get sample data
    sample_query = f"""
    SELECT sample FROM samples
    JOIN experiments ON samples.experiment_id = experiments.id
    WHERE experiments.user_id = {current_user.id}
    """

    # Run sample query
    sample_df = pd.read_sql(sample_query, db.session.bind)

    # Get location data
    location_query = f"""
    SELECT key, location, latitude, longitude, color FROM locations
    WHERE locations.user_id = {current_user.id}
    """

    # Run location query
    location_df = pd.read_sql(location_query, db.session.bind)

    # Find key inside sample names
    counter = Counter(x[2:5] for x in sample_df['sample'])

    # Filter counter for unwanted locations
    locs = {k: v for k, v in counter.items() if k in list(location_df['key'])}

    # Add to location dataframe
    location_df['count'] = location_df['key'].apply(lambda x: locs.get(x, 0))

    # Transform to json structure
    rv = [
        {
            'loc': [x['latitude'], x['longitude']],
            'name': x['location'],
            'count': x['count'],
            'bgColor': x['color']
        }
        for i, x in location_df.iterrows()
        if x['count'] > 0
    ]

    # Sort by largest count
    return sorted(rv, key=lambda x: x['count'], reverse=True)
