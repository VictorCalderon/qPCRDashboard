import pandas as pd
import numpy as np
from scipy.stats import norm
from itertools import product
from zipfile import ZipFile
from os import remove, path, makedirs


def gen_wells(rep=2):
    return np.array([[f'{w[0]}{w[1]}'] * rep for w in product(['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H'], [*range(1, 13)])]).flatten()


def gen_samples(rep=2):
    return np.array([[f'Sample {n}'] * rep for n in range(1, 97)]).flatten()


def random_amp(p=0.35):
    d = ['Amp', 'No Amp']
    return np.random.choice(d, p=[p, 1 - p])


def amp_score(x):
    if x == 'Amp':
        v = np.random.normal(loc=1.2, scale=0.05)
        return max(1, v)
    else:
        return 0


def cq(x):
    if x == 'Amp':
        v = np.random.normal(loc=30, scale=5)
        return min(37, v)
    else:
        return 'Undetermined'


def cq_conf(x):
    if x == 'Amp':
        return np.random.normal(loc=.95, scale=0.005)
    else:
        return 0


def flat(array):
    return np.array(array).flatten()


def sigmoid(height, cq):
    """Regular sigmoid func
    """
    # Set params
    a, k, x_0, c = [np.random.normal(loc=x, scale=x/5) for x in [height,  0.43462793, cq - 3,  0.14694006]]

    # Calculate z
    z = np.e ** (-k * (np.arange(40) - x_0))

    # Return sigmoid array
    return a / (1 + z) + c

def baseline():
    return [np.random.normal(loc=0.25, scale=0.001) for _ in range(40)]


def rn(amp):
    amped = results['Amp Score'] > 0
    rns = []

    for i in range(int(len(amped) / 2)):
        rns.extend(sigmoid(1.43, results['Cq'][2 * i]))

        if amped[2 * i + 1]:
            rns.extend(sigmoid(2.1, results['Cq'][2 * i + 1]))
        
        else:
            rns.extend(baseline())
    
    return rns

# Symetrical infected proportion config
std = 10
peak_infected = 35

# Generate infected proportions
xs = np.linspace(norm.ppf(0.01), norm.ppf(0.99), 30) * std
xs[15:] = xs[15:] * -1
xs = xs + peak_infected

# Generate files
for i, x in enumerate(xs):

    # Generate results and amplification datasets
    results = pd.DataFrame()
    amp = pd.DataFrame()

    # Populate dataframes
    results['Well Position'] = gen_wells()
    results['Sample'] = gen_samples()
    results['Target'] = flat([[f'Internal Control', f'SARS-CoV-2 Gene'] for n in range(1, 97)])
    results['Amp Status'] = flat([[f'Amp', f'{random_amp(p=x/100)}'] for n in range(1, 97)])
    results['Amp Score'] = results['Amp Status'].apply(lambda x: amp_score(x))
    results['Cq'] = results['Amp Status'].apply(lambda x: cq(x))
    results['Cq Confidence'] = results['Amp Status'].apply(lambda x: cq_conf(x))

    # Populate dataframess
    amp['Well Position'] = gen_wells(rep=80)
    amp['Sample'] = gen_samples(rep=80)
    amp['Cycle Number'] = flat([*range(1, 41)] * 96*2)
    amp['Target'] = flat([[f'Internal Control'] * 40 + [f'SARS-CoV-2 Gene'] * 40 for _ in range(1, 97)])
    amp['Rn'] = rn(amp)
    amp['dRn'] = [0] * len(amp)

    # Make dir
    try:
        makedirs('demo')
    except:
        continue

    # Filenames
    r = f'demo/Demo Run {i + 1}_Results Numbers.csv'
    a = f'demo/Demo Run{i + 1}_Amplification Data Numbers.csv'

    # Save files
    results.to_csv(r, index=False)
    amp.to_csv(a, index=False)

    # Generate ZipFile
    zipObj = ZipFile(f'data/Demo Run {i + 1}.zip', 'w')
    zipObj.write(r, path.basename(r))
    zipObj.write(a, path.basename(a))

    # Remove csv
    remove(r)
    remove(a)
