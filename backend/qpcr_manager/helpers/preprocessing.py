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
import re

# Data Structures
from collections import defaultdict, deque, Counter

# Data manipulation
import pandas as pd
import numpy as np

# Data preprocessing and clusterization
from sklearn.cluster import KMeans
from sklearn.metrics import silhouette_score
from sklearn.decomposition import PCA
from sklearn.preprocessing import StandardScaler
from sklearn.neighbors import KernelDensity
from sklearn.pipeline import Pipeline


# Dye list
qs_ = {
    'Cy5.5': 'X6_M6', 'Cy5': 'X5_M5', 'MUSTANG PURPLE': 'X5_M5', 'JUN': 'X4_M4',
    'ROX': 'X4_M4', 'Texas Red': 'X4_M4', 'ABY': 'X3_M3', 'NED': 'X3_M3', 'TAMRA': 'X3_M3',
    'Cy3': 'X3_M3', 'VIC': 'X2_M2', 'JOE': 'X2_M2', 'HEX': 'X2_M2', 'TET': 'X2_M2', 'FAM': 'X1_M1',
    'SYBR': 'X1_M1'
}

abi7500 = {
    'FAM': '1', 'SYBR': '1', 'JOE': '2', 'VIC': '2',
    'NED': '3', 'TAMRA': '3', 'Cy3': '3', 'ROX': '4',
    'Texas Red': '4', 'Cy5': '5'
}

q2000 = {
    'FAM': 'Channel1', 'SYBR GREEN': 'Channel1',
    'VIC': 'Channel2', 'HEX': 'Channel2', 'JOE': 'Channel2',
    'CY3': 'Channel2', 'NED': 'Channel2', 'ROX': 'Channel3',
    'TEXAS-RED': 'Channel3', 'CY5': 'Channel3', 'CY5': 'Channel4'
}

abi7500n = {
    'FAM': 'FAM-CYBRGreen', 'JOE': 'JOE-VIC', 'VIC': 'JOE-VIC',
    'TAMRA': 'TAMRA-NED-Cy3', 'NED': 'TAMRA-NED-Cy3', 'Cy3': 'TAMRA-NED-Cy3',
    'ROX': 'ROX-TEXASRed', 'TEXASRed': 'ROX-TEXASRed'
}


def save_to_temp(filebuffer) -> str:
    """Save file to temp folder
    """

    # Generate temp directory path
    temp_ = f'temp/{uuid1()}'
    temp_filename_ = f"{temp_}/{uuid1()}"

    # Check if the correct file was sent over
    try:
        assert hasattr(filebuffer, 'save') == True

    except AssertionError:
        raise AssertionError('Input file must be of type Werkzeug and have a `save` function to write on disk.')

    try:
        # Write path to disk
        makedirs(temp_)

        # Save file
        filebuffer.save(temp_filename_)

    except FileExistsError:
        raise FileExistsError('Could not write as it already exists.')

    # Return filename
    return temp_, temp_filename_


def merge_results_fluorescence(results: pd.DataFrame, raw: pd.DataFrame) -> pd.DataFrame:
    """Merge results and fluorescence raw data into a single table
    """

    # Melt dataset
    raw = raw.melt(id_vars=['Well Position', 'Cycle Number'],
                   var_name='Reporter', value_name='Fluorescence')

    # Transform cycles to strings
    raw['Cycle Number'] = raw['Cycle Number'].astype(str)

    # Generate Indexer
    raw['Indexer'] = raw['Well Position'] + '-' + raw['Reporter']

    # Remove duplicate cycles
    raw.drop_duplicates(
        subset=['Indexer', 'Cycle Number'], inplace=True)

    # Pivot table
    raw = raw.pivot(index='Indexer',
                    columns='Cycle Number', values='Fluorescence')

    # Extract and expand indexer
    indexer = raw.reset_index()['Indexer'].str.split(
        '-', expand=True).values

    # Insert expanded indexer
    for idx, col in enumerate(['Well Position', 'Reporter']):

        # Add column
        raw.insert(idx, col, indexer[:, idx])

    # Reset Index Inplace
    raw.reset_index(drop=True, inplace=True)

    # Sort columns
    sorted_columns = ['Well Position', 'Reporter'] + [str(x) for x in range(1, len(raw.columns) - 1)]
    raw = raw[sorted_columns]

    # Merge with results table
    results = pd.merge(raw, results, on=[
        'Well Position', 'Reporter'])

    # Replace "Undetermined" to 0
    results.replace('Undetermined', 0, inplace=True)

    return results


def load_experiment(results, current_experiment):
    """ Add experiment to database
    """

    # Add markers to database
    m_hash = add_markers(results['Target'].unique())

    # Total cycles
    maxc = len(results.columns) - 5

    # Iterate over samples
    for sample in results['Sample'].unique():

        # Instantiate sample
        s_ = Sample(sample=sample, experiment=current_experiment)

        # Mask results
        for res in results[results['Sample'] == sample].itertuples(index=False):

            # Hash marker_id
            marker_id = m_hash[res[-2]]

            # Instantiate result
            Result(amp_cq=res[-1], marker_id=marker_id, sample=s_)

            # Iterate over cycles
            for i in range(1, maxc + 1):

                # Instantiate fluorescences
                Fluorescence(
                    well=res[0], cycle=i, fluorescence=res[i + 1],
                    sample=s_, marker_id=marker_id
                )

    # Commit to database
    db.session.add(current_experiment)
    db.session.commit()


def parse_DA2(zippedDA2, current_experiment):
    """Extract dataset from zipped results

    Args:
        buffered_zup {werkzeug.io} -- io.Werkzeug file buffer with a save attr
    """

    # Check if the correct file was sent over
    try:
        assert hasattr(zippedDA2, 'save') == True

    except AssertionError:
        raise AssertionError('Input file must be of type Werkzeug and have a `save` function to write on disk.')

    # Save file to dist
    filedir_, filepath = save_to_temp(zippedDA2)

    # Open ZipFile in context manager
    with ZipFile(filepath, 'r') as zippedObj:

        # Extract everything to filepath
        zippedObj.extractall(filedir_)

    # Find files of importance
    results_dir = glob(f"{filedir_}/*Results*")
    raw_dir = glob(f"{filedir_}/*Raw*")

    # Assert
    try:
        assert len(results_dir) == 1
        assert len(raw_dir) == 1

    except AssertionError:
        print('The Zip must contain both Results and Raw Data.')

    # Add description
    with open(results_dir[0]) as r:

        # Read first 22 lines
        description = '\n'.join([next(r).strip().lstrip('# ') for _ in range(22)])
        date = re.search('Last Modified Date/Time: \d{4}-\d{2}-\d{2}', description)[0].split(':')[1].strip()
        name = re.search('Plate File Name: .+', description)[0].split(':')[1].strip().strip('.eds')

    # Add data to current experiment
    if (current_experiment.name != 'DefaultName'):
        current_experiment.name = name

    if (current_experiment.date != '1996-05-25'):
        current_experiment.date = date

    # Add description
    current_experiment.observations = description

    # Add results
    results = pd.read_csv(
        results_dir[0], comment='#', usecols=[
            'Well Position', 'Reporter', 'Sample', 'Target', 'Cq']
    ).replace('', pd.NA).dropna()

    # Remove undetermined
    results['Cq'] = results['Cq'].replace('Undetermined', 0)

    # Round Cq values
    results['Cq'] = np.around(results['Cq'].astype(float), 2)

    # Unique reporters
    used_channels = {qs_[r]: r for r in results['Reporter'].unique()}

    # Open Raw Data
    raw = pd.read_csv(
        raw_dir[0], comment='#', usecols=[
            "Well Position", "Cycle Number", *used_channels.keys()]
    ).replace('', pd.NA).dropna()

    # Rename columns based on their reporters
    raw.rename(used_channels, axis=1, inplace=True)

    # Remove file tree
    rmtree(filedir_)

    # Merge data
    return merge_results_fluorescence(results, raw)


def parse_7500(flat7500, current_experiment):
    """Parse flat 7500 export file

    Args:
        flat7500 {werkzeug.io} -- io.Werkzeug file buffer with a save attr
    """

  # Check if the correct file was sent over
    try:
        assert hasattr(flat7500, 'save') == True

    except AssertionError:
        raise AssertionError('Input file must be of type Werkzeug and have a `save` function to write on disk.')

    # Save file to dist
    filedir_, filepath = save_to_temp(flat7500)

    # Read file results
    with open(filepath, 'r') as r:

        # Read description
        description = '\n'.join(next(r).strip().lstrip('* ') for _ in range(6))
        date = re.search('Experiment Run End Time = \d{4}-\d{2}-\d{2}', description)[0].split('=')[1].strip()
        name = re.search('Experiment File Name = .+',
                         description)[0].split('=')[1].strip().strip('.eds').split('\\')[-1]
        data, raw_file = {}, r.read().split('\n\n')

    # Add data to current experiment
    if (current_experiment.name != 'DefaultName'):
        current_experiment.name = name

    if (current_experiment.date != '1996-05-25'):
        current_experiment.date = date

    # Add description
    current_experiment.observations = description

    # Iterate over separated data(skip first)
    for d in raw_file[1:]:

        # Remove trialing white space
        d = d.strip()

        # Split by new line
        split_data = d.split('\n')

        # First line as header (Remove non work characters)
        header = search(r'\w+', split_data[0])

        # Check if header exists
        if header:

            # Extract matching subtring
            header = header.group(0)

        else:

            # Else raise error
            raise('Section delimiters before data')

        # Add header and data to container
        data[header] = split_data[1:]

    # Read results and raw tables
    try:
        assert all(item in list(data.keys()) for item in ['Raw', 'Results'])

    except AssertionError:
        print('Your raw data must contain both Raw Data and Results exports.')

    # Transform results to records into records
    results = [record.split('\t') for record in data['Results']]
    results = pd.DataFrame.from_records(data=results[1:], columns=results[0])
    results = results.replace('', pd.NA)[['Well', 'Reporter', 'Sample Name', 'Target Name', 'Cт']].dropna()

    # Change column names for compatibility
    results.columns = ['Well Position', 'Reporter', 'Sample', 'Target', 'Ct']

    # Unique reporters and filter columns
    used_channels = {abi7500n.get(r, 'NOT_SUPPORTED'): r for r in results['Reporter'].unique()}
    filter_columns = ['Well', 'Cycle'] + list(used_channels.keys())

    # Transform raw data to records
    raw = [record.split('\t') for record in data['Raw']]
    raw = pd.DataFrame.from_records(data=raw[1:], columns=raw[0])
    raw = raw.replace('', pd.NA)[filter_columns].dropna()

    # Rename columns based on their reporters
    raw.rename({'Well': 'Well Position', 'Cycle': 'Cycle Number', **used_channels}, axis=1, inplace=True)

    # Remove temp
    rmtree(filedir_)

    # Return data
    return merge_results_fluorescence(results, raw)

    # # Load Experiment to database
    # load_experiment(results, current_experiment)


def parse_q2000(flatq2000, current_experiment):
    """Parse flat q2000 export file

    Args:
        flatq2000 {werkzeug.io} -- io.Werkzeug file buffer with a save attr
    """

  # Check if the correct file was sent over
    try:
        assert hasattr(flatq2000, 'save') == True

    except AssertionError:
        raise AssertionError('Input file must be of type Werkzeug and have a `save` function to write on disk.')

    # Save file to dist
    filedir_, filepath = save_to_temp(flatq2000)

    # Read file results
    with open(filepath, 'r') as r:

        # Read description
        description = '\n'.join(next(r).strip().lstrip('* ') for _ in range(3))
        date = re.search('Export File Created at:\d{4}-\d{2}-\d{2}', description)[0].split(':')[1].strip()
        name = re.search('Experiment Name: .+', description)[0].split(':')[1].strip()
        data, raw_file = {}, r.read().split('\n\n')

    # Add data to current experiment
    if (current_experiment.name != 'DefaultName'):
        current_experiment.name = name

    if (current_experiment.date != '1996-05-25'):
        current_experiment.date = date

    # Add description
    current_experiment.observations = description

    # Iterate over separated data(skip first)
    for d in raw_file[1:]:

        # Remove trialing white space
        d = d.strip()

        # Split by new line
        split_data = d.split('\n')

        # First line as header (Remove non work characters)
        header = search(r'\w+', split_data[0])

        # Check if header exists
        if header:

            # Extract matching subtring
            header = header.group(0)

        else:

            # Else raise error
            raise('Section delimiters before data')

        # Add header and data to container
        data[header] = split_data[1:]

    # Read results and raw tables
    try:
        assert all(item in list(data.keys()) for item in ['Raw', 'Results'])

    except AssertionError:
        print('Your raw data must contain both Raw Data and Results exports.')

    # Transform results to records into records
    results = [record.split('\t') for record in data['Results']]
    results = pd.DataFrame.from_records(data=results[1:], columns=results[0])
    results = results.replace('', pd.NA)[['Well', 'Dye', 'Sample', 'Target', 'Ct']].dropna()

    # Remove / from dataset
    results['Ct'] = results['Ct'].replace('/', 0)

    # Change column names for compatibility
    results.columns = ['Well Position', 'Reporter', 'Sample', 'Target', 'Ct']

    # Unique reporters and filter columns
    used_channels = {q2000.get(r, 'NOT_SUPPORTED'): r for r in results['Reporter'].unique()}
    filter_columns = ['Well', 'Cycle'] + list(used_channels.keys())

    # Transform raw data to records
    raw = [record.split('\t') for record in data['Raw']]
    raw = pd.DataFrame.from_records(data=raw[1:], columns=raw[0] + ['', ''])
    raw = raw.replace('', pd.NA)[filter_columns].dropna()

    # Rename columns based on their reporters
    raw.rename({'Well': 'Well Position', 'Cycle': 'Cycle Number', **used_channels}, axis=1, inplace=True)

    # Remove temp
    rmtree(filedir_)

    # Return data
    return merge_results_fluorescence(results, raw)


def load_DA2(filebuffer, current_experiment):
    """Load DA2 data format to dataset
    """

    # Parse dataset
    results = parse_DA2(filebuffer, current_experiment)

    # Load Experiment to database
    load_experiment(results, current_experiment)


def load_7500(filebuffer, current_experiment):
    """Load ABI 7500 data to database
    """

    # Parse dataset
    results = parse_7500(filebuffer, current_experiment)

    # Load experiment to database
    load_experiment(results, current_experiment)


def load_q2000(filebuffer, current_experiment):
    """Load Q2000 data to database
    """

    # Parse results
    results = parse_q2000(filebuffer, current_experiment)

    # Load experiments to database
    load_experiment(results, current_experiment)


def query_samples(current_user, sample):
    """Query database for samples based on sample name
    """

    # Build query
    query = f"""
    SELECT experiments.id as experiment_id, sample, name, marker, amp_status, amp_cq FROM experiments
    JOIN samples ON samples.experiment_id = experiments.id
    JOIN results ON results.sample_id = samples.id
    JOIN markers ON results.marker_id = markers.id
    WHERE experiments.user_id = {current_user.id} and samples.sample LIKE '%%{sample}%%';
    """

    # Run in pandas
    return pd.read_sql(query, con=db.session.bind).to_dict(orient='records')


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
            new_marker.user_id = current_user.id
            db.session.add(new_marker)
            db.session.commit()

            # Add to m_hash
            m = Marker.query.filter_by(marker=marker).first()
            m_hash[m.marker] = m.id

    return m_hash


# Amp status
def amp_status(x, amp_keyword='Amp'):
    return True if x == amp_keyword else False

# Load results fast
@lru_cache(maxsize=100)
def get_experiment_results(experiment_id):
    """Query and parse a DataFrame with Experiment(experiment_id) results
    """

    # Build query
    query = f"""
    SELECT sample, marker, amp_status, amp_cq FROM samples
    JOIN experiments ON samples.experiment_id = experiments.id
    JOIN results ON results.sample_id = samples.id
    JOIN markers ON results.marker_id = markers.id
    WHERE experiments.user_id = {current_user.id} and experiments.id = {experiment_id}
    """

    # Run query
    results_df = pd.read_sql(query, db.session.bind)

    # Return results
    return results_df


def available_markers():
    """Return a list of all available markers
    """

    # Generate query
    query = f"""
    SELECT id, marker, target_id FROM markers
    WHERE markers.user_id = {current_user.id}
    """

    # Run query
    markers = pd.read_sql(query, db.session.bind)

    # Return markers
    return markers.to_json(orient='records')


def get_brief():
    """Count the number of experiments and samples processed
    """

    query = f"""
    SELECT s.sample, e.name, e.analyzed FROM samples AS s
    JOIN experiments AS e ON s.experiment_id = e.id
    WHERE e.user_id = {current_user.id}
    """

    # Run query
    dataset = pd.read_sql(query, db.session.bind)

    # Pending experiments vs analzyzed experiments
    not_reported = dataset['analyzed'] == False
    pending, reported = np.sum(not_reported), np.sum(~not_reported)

    # Make unique
    exps, samples = len(dataset['name'].unique()), len(dataset['sample'])

    # Return dataset
    return {"experiments": int(exps), "samples": int(samples), "pending": int(pending), "reported": int(reported)}


def amp_stat_data():
    """Build a target based timeseries for each added type
    """

    # Build query
    query = f"""
    SELECT experiments.name, date, samples.id, target, amp_cq FROM samples
    JOIN experiments on experiments.id = samples.experiment_id
    JOIN results on results.sample_id = samples.id
    JOIN markers on results.marker_id = markers.id
    JOIN targets on markers.target_id = targets.id
    WHERE experiments.user_id = {current_user.id} AND experiments.analyzed = true
    """

    # Run query in pandas
    dataset = pd.read_sql(query, db.session.bind)

    # Compute all amplified samples
    dataset['amp_status'] = dataset['amp_cq'] != 0

    # Group by date and target and calculate amplification (binary mean) percentages
    dataset = dataset.groupby(['date', 'target'])['amp_status'].mean().reset_index()

    # Parse date as datetime
    dataset['date'] = pd.to_datetime(dataset['date'])

    # Parse dates
    dataset['day'] = dataset['date'].dt.day
    dataset['month'] = dataset['date'].dt.month_name()

    # Make then pretty
    dataset['day-month'] = dataset['day'].astype(str) + '-' + dataset['month'].astype(str)

    # Instantiate data struct [{'target': 'example 1, 'data': [1, 2, 3]}]
    datasets = []
    dates = None

    # Generate parsed dataset
    for target in dataset['target'].unique():

        # Mask dataset to keep target specific
        df = dataset[dataset['target'] == target]

        # Get dataset
        percs = df['amp_status'] * 100

        # Add data to struct
        datasets.append({'target': target, 'data': percs.to_list()})

        # Times will become the x axis
        dates = df['day-month'].to_list()

    # Sort list of dictionaries
    datasets = sorted(datasets, key=lambda i: np.mean(i['data']))

    # Use last iteration day-month column
    return {'dates': dates, 'datasets': datasets}


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
    WHERE experiments.user_id = {current_user.id} AND experiments.analyzed = true
    """

    # Run query with pandas
    dataset = pd.read_sql(query, db.session.bind)

    # Get split list of lists
    tags = []

    # Iterate over dataset
    for t in dataset['tags']:

        # If t exists
        if(t):

            # Get its tags
            tags.append(t.split(','))

    # Flatten tags
    tags = [item for sublist in tags for item in sublist]

    # Count data
    tag_counter = Counter(tags)

    # Sorted count data
    tag_counter = dict(tag_counter.most_common(len(tag_counter.keys())))

    return {'labels': list(tag_counter.keys()), 'dataset': list(tag_counter.values())}


def location_modifications(locations):
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
    WHERE experiments.user_id= {current_user.id} AND experiments.analyzed = true
    """

    # Run sample query
    sample_df = pd.read_sql(sample_query, db.session.bind)

    # Get location data
    location_query = f"""
    SELECT key, location, latitude, longitude, color FROM locations
    WHERE locations.user_id= {current_user.id}
    """

    # Run location query
    location_df = pd.read_sql(location_query, db.session.bind)

    # Find key inside sample names
    counter = Counter(x[2:5] for x in sample_df['sample'])

    # Filter counter for unwanted locations
    locs = {k: v for k, v in counter.items() if k in list(location_df['key'])}

    # Add a count
    location_df['count'] = location_df['key'].apply(lambda x: locs.get(x, 0))

    # Divide by total sum
    location_df['perc'] = location_df['count'] / location_df['count'].sum()

    # Transform to json structure
    rv = [
        {
            'loc': [x['latitude'], x['longitude']],
            'name': x['location'],
            'perc': x['perc'],
            'count': x['count'],
            'bgColor': x['color']
        }
        for i, x in location_df.iterrows() if x['count'] > 0
    ]

    # Sort by largest count
    return sorted(rv, key=lambda x: x['count'], reverse=True)


def sample_table(experiment_id):
    """Get current experiment data"""

    # Build query
    query = f"""
    SELECT samples.id, sample, marker, amp_status AS amp, amp_cq AS cq, score, results.id AS result_id FROM experiments
    JOIN samples on samples.experiment_id = experiments.id
    JOIN results on results.sample_id= samples.id
    JOIN markers on results.marker_id= markers.id
    WHERE experiments.user_id = {current_user.id} and experiments.id = {experiment_id};
    """

    # Run query
    dataset = pd.read_sql(query, db.session.bind)

    # Add random score
    dataset['score'] = np.abs(np.random.rand(dataset.shape[0]) - 0.5)
    dataset['score'] = np.around(dataset['score'] * 2, decimals=2)

    # Return dataset as a list
    return dataset.to_dict('records')


def compute_kmeans_labels(dataset):
    """Compute KMeans labels based on PCA transformed dataset
    """

    # Model distortion
    models = [
        KMeans(n_clusters=i, n_init=20, max_iter=500, random_state=42).fit(dataset) for i in range(2, 10)
    ]

    # Get distortions
    sil_scores = [silhouette_score(dataset, m.labels_, metric='euclidean') for m in models]

    # Compute best K
    best_k = np.argmax(sil_scores)

    # Return best model labels
    return models[best_k].labels_


def experiment_pca_kmeans(experiment_id, k=None):
    """Build a PCA from experiment results
    """

    # Get results
    results_df = get_experiment_results(experiment_id)

    # Count unique markers
    n_components = len(results_df['marker'].unique())

    # Assert there are no duplicates
    assert len(results_df.duplicated(subset=['sample', 'marker'])) != 0

    # Pivot Table
    results_df = results_df.pivot(index='sample', columns='marker', values='amp_cq')

    # Drop NaN columns
    results_df = results_df.dropna(axis=0)

    # Scaled dataset
    scaled_data = StandardScaler().fit_transform(results_df)

    # PCA from scaled data
    pca = PCA(n_components=n_components, random_state=42).fit_transform(scaled_data)

    # Add random noise for plotting (jitter)
    pca += np.random.randn(pca.shape[0], pca.shape[1]) * 0.01

    # Add components to results DataFrame with jitter
    results_df['PCA 1'] = np.around(pca[:, 0], 2)
    results_df['PCA 2'] = np.around(pca[:, 1], 2)

    # Add cluster labels
    if k:
        results_df['Cluster'] = KMeans(n_clusters=k).fit(pca).labels_

    else:
        results_df['Cluster'] = compute_kmeans_labels(pca)

    # PCA dataset
    pca_df = results_df.reset_index()[['sample', 'PCA 1', 'PCA 2', 'Cluster']]

    # Return dataset
    return pca_df.to_dict('records')


# Sliding window noise detector
def sliding_denoiser(raw_data, window=5):
    """Compute Log(raw_data) - Min(Std(SlidingWindow(Log(raw_data))))
    """

    # Compute means
    stds_ = [np.std(raw_data[i: i: window]) for i in range(len(raw_data - window + 1))]

    # Compute argmin
    std_argmin = np.argmin(stds_)

    # Log transform data (add small amount to remove zeros)
    raw_data = np.log(raw_data + 1e-5)

    # Compute denoised data
    denoised_data = raw_data - np.mean(raw_data[std_argmin: std_argmin + window])

    # Clip data to -1 for plotting
    return np.clip(denoised_data, -1, 10)


@lru_cache(maxsize=10)
def compute_fluorescences(experiment_id):
    """Get current experiment fluorescence data"""

    # Build query
    query = f"""
    SELECT results.id as result_id, well, sample, marker, cycle, fluorescence FROM samples
    JOIN fluorescences on fluorescences.sample_id= samples.id
    JOIN markers on markers.id= fluorescences.marker_id
    JOIN experiments on experiments.id= samples.experiment_id
    JOIN results on(results.sample_id = samples.id and results.marker_id = markers.id)
    WHERE experiments.id = {experiment_id}
    """

    # Run query
    dataset = pd.read_sql(query, db.session.bind)

    # Create single column index
    dataset['indexer'] = dataset['result_id'].astype(str) + '&-&' + dataset['well'] + \
        '&-&' + dataset['sample'] + '&-&' + dataset['marker']

    # Pivot and sort dataset
    dataset = dataset.pivot(index='indexer', columns='cycle', values='fluorescence')

    # Log transform and remove noise
    # dataset.iloc[:, :] = dataset.apply(lambda row: sliding_denoiser(row), axis=1).values

    # Reset index
    dataset.reset_index(inplace=True)

    # Separate data
    split_indexer = dataset['indexer'].str.split('&-&', expand=True).values

    # Add split data to DataFrame
    for idx, col in enumerate(['result_id', 'well', 'sample', 'marker']):

        # Add column
        dataset.insert(idx, col, split_indexer[:, idx])

    # Remove redundant indexer
    dataset.drop('indexer', axis=1, inplace=True)

    # Return dataset
    return dataset


def experiment_fluorescences(experiment_id):
    """Send experiment to frontend
    """

    # Get data
    dataset = compute_fluorescences(experiment_id)

    # Build json like dataset
    return [{'result_id': d[1], 'well': d[2], 'sample': d[3], 'marker': d[4], 'data': list(d[5:])} for d in dataset.itertuples()]


def maximum_gradient(experiment_id):
    """Second order gradient maximum distribution
    """

    # Get fluorescences and initialize grad_
    fluo_data = experiment_fluorescences(experiment_id)
    max_grad = []

    # Iterate over fluorescences and compute grad and cycle
    for f in fluo_data:

        # Compute second order gradient
        grad_ = np.gradient(np.log(np.array(f['data']) + 5e-5))

        # Extract argmax from index 5 onward to avoid weirdness
        cycle = np.argmax(grad_[5:]) + 5

        # Add to dataset
        max_grad.append({
            'result_id': f['result_id'],
            'sample': f['sample'],
            'marker': f['marker'],
            'cycle': int(cycle),
            'maxgrad': float(grad_[cycle])
        })

    # Return max gradient
    return max_grad


def maximum_gradient_kde(experiment_id):
    """Compute a Max Gradient KDE
    """

    # Get fluorescences
    fluo_data = compute_fluorescences(experiment_id)

    # Compute max gradients
    fluo_data['max_grad'] = fluo_data.iloc[:, 5:].apply(lambda r: np.max(np.gradient(r)), axis=1)

    # Initialize empty kde array
    kdes = []

    # Iterate over marker
    for marker in fluo_data['marker'].unique():

        # Filter dataset by marker
        d_ = fluo_data[fluo_data['marker'] == marker]

        # Transform data
        d_ = np.array(d_['max_grad']).reshape(-1, 1)

        # Compute KDE of d_
        kde = KernelDensity(kernel='gaussian').fit(d_)

        # Compute log densities
        kde_estimates = np.exp(kde.score_samples(np.linspace(-5, 10, 100).reshape(-1, 1)))

        # Save exp(log_densities) to kdes
        kdes.append({'marker': marker, 'kde': list(kde_estimates)})

    # Return dataset
    return kdes
