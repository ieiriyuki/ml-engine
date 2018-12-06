#!/usr/local/bin/python

import os
import sys
import pickle
import click
import pandas as pd
import numpy as np
from sklearn.preprocessing import StandardScaler
from sklearn.linear_model import LinearRegression
from sklearn.ensemble import RandomForestRegressor


FILE_DIR = os.path.dirname(os.path.abspath(__file__))
DEFAULT_INPUT = os.path.join(FILE_DIR, '../data/raw/test.csv')
DEFAULT_OUTPUT = os.path.join(FILE_DIR, '../data/prepared/my_submission.csv')
DEFAULT_PIPELINE = os.path.join(FILE_DIR, '../data/pickles/model.pkl')
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
@click.option('-p',
              '--pipeline',
              default=DEFAULT_PIPELINE,
              help='specify a pipeline for prediction')
def main(**kwargs):
    """load test data, predict house price for test data,
     and create a file for submission
    """

    wrap_predict(kwargs['input'],
                 kwargs['output'],
                 kwargs['pipeline'])


def wrap_predict(input, output, pipeline):

    features = DEFAULT_FEATURES[:-1]
    with open(input, 'r') as fin:
        data = pd.read_csv(fin,
                           header=0,
                           sep=",",
                           encoding='utf-8')

    with open(pipeline, 'rb') as fin:
        pipeline = pickle.load(fin)

    prediction = predict(data[features], pipeline)

    submit = pd.DataFrame({ 'Id': data['Id'],
                            'SalePrice': prediction })

    with open(output, 'w') as ofile:
        submit.to_csv(ofile, index=False)


def predict(data, pipeline):

    assert isinstance(data, pd.DataFrame), 'Error: data must be pandas.DataFrame'

    data = data.values.astype('f8')
    prediction = pipeline.predict(data).flatten().tolist()

    return prediction


if __name__=='__main__':
    main()
