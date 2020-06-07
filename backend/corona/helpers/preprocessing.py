from corona.models import qPCR, Project, Sample, Marker, Result
from corona.extensions import db
from functools import lru_cache
from collections import defaultdict, deque
from re import search
from datetime import date
from uuid import uuid1
from zipfile import ZipFile
from glob import glob
from sklearn.decomposition import PCA
from sklearn.preprocessing import StandardScaler
from sklearn.pipeline import Pipeline
import pandas as pd
import numpy as np
import os


def open_zipped_project(buffered_zip):
    """ Extract data from zipped qPCR project

    Arguments:
        buffered_zip {werkzeug.io} -- [A werkzeug file buffer]
    """

    # Make temporary file directory
    dir_uuid = f'/code/projects/{uuid1()}'
    os.makedirs(dir_uuid)

    # Save file
    filename = dir_uuid + '/zipped_project.zip'
    buffered_zip.save(filename)

    # Open file
    with ZipFile(filename, 'r') as zippedObj:

        # Extract data to temporary dir_uuid folder
        zippedObj.extractall(dir_uuid)

        # Make a data container with relevant data
        data_container = {}

        # Get Results, Amplification and Sample data
        amp_data = glob(f'{dir_uuid}/*Amplification*')[0]
        results = glob(f'{dir_uuid}/*Results*')[0]

        # Open dataframes
        amp_data = pd.read_csv(amp_data, comment='#').replace('', pd.NA).dropna()
        results = pd.read_csv(results, comment='#').replace('', pd.NA).dropna()

        # Change Undetermined to 0
        results = results.replace('Undetermined', 0)

        # Make them the correct datatype
        amp_data = amp_data.astype({
            'Well Position': str, 'Sample': str,
            'Cycle Number': int, 'Target': str, 'Rn': float
        })

        results = results.astype(
            {
                'Well Position': str, 'Sample': str, 'Target': str,
                'Amp Status': str, 'Cq': float, 'Cq Confidence': float
            })

    return {'Amplification': amp_data, 'Results': results}


def import_qpcr(filebuffer, section_sep='\w+') -> dict:
    """Open qPCR csv file and saves each subdocument in dictionary of pandas DataFrames
    """

    # Create unique id
    file_uuid = f'/code/projects/{uuid1()}'

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
    os.remove(file_uuid)

    return data_container


def parse_qpcr(data_container, sep='\t'):
    """Parse qPCR data coming from a determined raw file
    """

    # Get Sample Data and instantiate dataframe
    samples = [record.split(sep) for record in data_container['Sample']]
    samples = pd.DataFrame.from_records(data=samples[1:], columns=samples[0])

    # Get qPCR data and instantiate dataframe
    qpcrs = [record.split(sep) for record in data_container['Amplification']]
    qpcrs = pd.DataFrame.from_records(data=qpcrs[1:], columns=qpcrs[0])

    # Merge data
    qpcrs_with_samples = pd.merge(qpcrs, samples, how='inner', on=['Well', 'Target Name'])

    # Filter necessary data
    qs = qpcrs_with_samples[['Well', 'Cycle', 'Sample Name', 'Target Name', 'Rn']]  # 'ΔRn'

    # Remove empty spaces and NaNs
    qs = qs.replace('', pd.NA).dropna()

    return qs


@lru_cache(maxsize=10)
def query_marker(marker_id):
    """Query database for markers
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
def amp_status(x):
    return True if x == 'Amp' else False


def feed_zip(filebuffer, current_project, current_user):
    """Add project to database
    """

    # Import data
    data_container = open_zipped_project(filebuffer)

    # Extract data
    amp, results, details = data_container['Amplification'], data_container['Results'], 'details'

    # Get unique samples
    unique_samples = results['Sample'].unique()

    # Unique markers
    unique_markers = amp['Target'].unique()

    # Get marker hash
    m_hash = add_markers(unique_markers)

    # Iterate over samples
    for sample_name in unique_samples:

        # Instantiate sample
        sample = Sample(sample=sample_name, project=current_project)

        # Mask dataframe for qPCRs
        sample_qpcrs = amp[amp['Sample'] == sample_name]

        # Iterate over qpcrs cycles
        for qpcr in sample_qpcrs.itertuples():

            # Get marker_id
            marker_id = m_hash[qpcr[4]]

            # Instantiate qPCR
            qpcr = qPCR(
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
                amp_status=amp_status(result[4]), amp_score=round(result[5], 2),
                amp_cq=round(result[6], 3), cq_confidence=round(result[7], 3),
                marker_id=marker_id, sample=sample
            )

    # Add project to DB
    db.session.add(current_project)
    db.session.commit()


def feed_qpcrs(filebuffer, current_project, current_user):
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
        sample = Sample(sample=sample_name, project=current_project)

        # Mask dataframe for sample qPCRS
        sample_qpcrs = qs[qs['Sample Name'] == sample_name]

        # Iterate over qpcrs
        for qpcr in sample_qpcrs.itertuples():

            # Get marker_id
            marker_id = m_hash[qpcr[4]]

            # Instantiate qPCR
            qpcr = qPCR(
                well=qpcr[1], cycle=qpcr[2],
                rn=qpcr[5], sample=sample, marker_id=marker_id)

    # Add project to DB
    db.session.add(current_project)
    db.session.commit()


@lru_cache(maxsize=100)
def query_qpcrs(sample_id):
    """ Query and return a parse qPCR for frontend display
    """

    # Query sample
    sample = Sample.query.get_or_404(sample_id)

    # Get qPCRs
    qpcrs = [(q.marker_id, q.cycle, q.rn) for q in sample.qpcrs]

    # Max cycles
    max_cycle = max([q[1] for q in qpcrs])

    # Container
    qpcrs_data = defaultdict(list)

    # Iterate over qpcrs tuples
    for q in qpcrs:

        # Check if key not in data
        if q[0] not in qpcrs_data.keys():
            qpcrs_data[q[0]] = [*range(max_cycle)]

        # Add data to container
        qpcrs_data[q[0]][q[1] - 1] = q[2]

    # Array of data
    qpcrs_array = []

    # Change dict key name
    for k in qpcrs_data:

        # Query db for key
        qpcrs_array.append({
            'marker': query_marker(k),
            'amp': qpcrs_data[k],
            'well': sample.qpcrs[0].well
        })

    return sorted(qpcrs_array, key=lambda x: x['marker'])


def export_results(project_id, current_user):
    """Export project
    """

    config = {
        'export_delimiter': ',',
        'retention_tag_sample': 'Control',
        'retention_tag_result_1': 'RETENIDO',
        'retention_tag_result_2': 'INHIBIDO',
    }

    try:

        # Get samples form project
        samples = Project.query.filter_by(user_id=current_user.id, id=project_id).first()

        if samples is None:
            raise ValueError

        # Get results (samples, results)
        results = [(s.sample, s.result) for s in samples.samples]

    except:
        raise ValueError('You can only export your own projects')

    try:
        # Empty file
        file_string = []

        # Iterate over results
        for sample, result in results:

            # Filter if retention_tag_result
            if (config['retention_tag_result_1'] in result) or (config['retention_tag_result_2'] in result):

                # Skip
                continue

            # Filter if retention_tag_sample
            if (config['retention_tag_sample'] in sample):

                # Skip
                continue

            # Write data
            file_string.append(f"{sample}{config['export_delimiter']}{result}\n")

        # return filepath
        return ''.join(file_string)

    except:
        raise IOError('Could not export project')


def analyze_project(project_samples):
    """Analyze project
    """

    # Set column names
    column_names = ['sample', 'marker', 'amp_status', 'amp_cq', 'cq_confidence']

    # Get records from set
    records = deque()

    # Iterate over query
    for s in project_samples:

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
    if len(markers) > 2:

        # Build PCA pipeline
        pipe = Pipeline([('scaler', StandardScaler()),
                         ('reducer', PCA(n_components=2))])

        # Process cq matrix
        pca = pipe.fit_transform(results_df)

        # Add PCA components to dataframe
        results_df['PCA 1'] = pca.iloc[:, 0]
        results_df['PCA 2'] = pca.iloc[:, 1]

    # Data
    # data = [{'x': s[markers[1]], 'y': s[markers[0]]} for s in results_df.to_dict('records')]
    data = results_df.to_dict('list')

    # # Build extended Confidene dataframe
    # confidence = results.pivot_table(index='sample', columns='marker', values='cq_confidence').to_dict()

    # Count amplifications
    statistics = results.groupby('marker')['amp_status'].agg([np.mean, np.sum]).reset_index().to_dict('records')

    return samples, data, statistics


def available_markers(current_user):
    """Return a list of all available markers
    """

    query = f"""
    SELECT DISTINCT(m.id)
    FROM samples AS s 
    JOIN projects AS p on s.project_id = p.id
    JOIN results AS r on r.sample_id = s.id
    JOIN markers as m on r.marker_id = m.id
    WHERE p.user_id = {current_user.id}
    """

    # Run query
    markers = db.session.execute(query)

    # Clean markers
    markers = [{'value': m.id, 'text': query_marker(m.id)} for m in markers]

    # Return marker list
    return markers


def dashboard_data(marker_id, current_user):
    """Query dashboard data (date, perc_cases, total_samples, total_projects)
    """
    my_query = f"""
    SELECT experiment_date, CAST(COUNT(CASE WHEN amp_status THEN 1 END) as decimal) / COUNT(amp_status), COUNT(DISTINCT(sample)), COUNT(DISTINCT(name))
    FROM samples AS s
    JOIN projects as p on s.project_id = p.id
    JOIN results as r on r.sample_id = s.id
    JOIN markers as m on r.marker_id = m.id
    WHERE m.id = {marker_id} AND p.user_id = {current_user.id}
    GROUP BY experiment_date
    """

    # Run query
    data = db.session.execute(my_query)

    # Parse data
    data = [(str(d[0]), round(float(d[1]), 2), d[2], d[3]) for d in data]

    # Insert into dataframe
    data = pd.DataFrame(data=data, columns=['Date', 'Amp Fraction', 'Total Samples', 'Total Projects'])

    # Return data
    return data.to_dict('list')
