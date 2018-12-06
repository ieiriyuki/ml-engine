#!/usr/local/bin/pyton

import os
import click
import pandas as pd
from datetime import datetime


FILE_DIR = os.path.dirname(os.path.abspath(__file__))
NOW = datetime.now().strftime("%Y%m%d-%H%M%S")
DEFAULT_INPUT = os.path.join(FILE_DIR, '../data/raw/old.csv')
DEFAULT_OUTPUT = os.path.join(FILE_DIR,
                              '../data/prepared/alignmented_data_' + NOW + '.csv')
DEFAULT_FEATURES = ['LotArea', 'BedroomAbvGr', 'YrSold', 'MoSold', 'SalePrice']


@click.command()
@click.option('-i',
              '--input',
              default=DEFAULT_INPUT,
              type=click.Path(exists=True),
              help='specify an input file',
              metavar='input')
@click.option('-o',
              '--output',
              default=DEFAULT_OUTPUT,
              type=click.Path(),
              help='specify an output file',
              metavar='output')
def main(**kwargs):
    """load data, extract features, and alignment columns
    """

    wrap_alignment(kwargs['input'], kwargs['output'])


def wrap_alignment(input, output):
    """load data, extract features, and alignment columns
    """

    features = DEFAULT_FEATURES
    with open(input, 'r') as fin:
        data = pd.read_csv(fin,
                           header=0,
                           sep=",",
                           encoding='utf-8',
                           usecols=features)

    data = alignment(data, features)

    with open(output, 'w') as fout:
        data.to_csv(fout, index=False)


def alignment(data, features):
    """only check if data is a pandas.DataFrame, and
    alignment columns (labels is -1)
    """

    assert isinstance(data, pd.DataFrame), "Error: data must be pandas.DataFrame."

    return data[features]


if __name__=="__main__":
    main()
