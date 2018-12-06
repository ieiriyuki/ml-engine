#!/usr/local/bin/python

import os
import sys
import pickle
import json
import click
import pandas as pd
import numpy as np
from datetime import datetime
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import StandardScaler
from sklearn.linear_model import LinearRegression
from sklearn.ensemble import RandomForestRegressor
from mlflow import set_tracking_uri, log_metric, log_artifact
from mlflow.sklearn import log_model

sys.path.append(os.path.dirname(__file__))
from evaluate import calculate_metrics


FILE_DIR = os.path.dirname(os.path.abspath(__file__))
NOW = datetime.now().strftime("%Y%m%d-%H%M%S")
DEFAULT_TRAIN = os.path.join(FILE_DIR, '../data/prepared/data_train.csv')
DEFAULT_VALID = os.path.join(FILE_DIR, '../data/prepared/data_valid.csv')
DEFAULT_OUTPUT = os.path.join(FILE_DIR,
                              '../data/pickles/model_' + NOW + '.pkl')
DEFAULT_METRICS = os.path.join(FILE_DIR,
                               '../data/profile/metrics_' + NOW + '.json')
DEFAULT_URI = os.path.join(FILE_DIR, '../mlruns')
MODEL_DICT = { 'lm': LinearRegression(),
               'rf': RandomForestRegressor() }


@click.command()
@click.option('-t',
              '--train',
              default=DEFAULT_TRAIN,
              type=click.Path(exists=True),
              help='specify a train data',
              metavar='train')
@click.option('-v',
              '--valid',
              default=DEFAULT_VALID,
              type=click.Path(exists=True),
              help='specify a valid data',
              metavar='valid')
@click.option('-o',
              '--output',
              default=DEFAULT_OUTPUT,
              type=click.Path(),
              help='specify a model pickle as output',
              metavar='output')
@click.option('--metrics',
              default=DEFAULT_METRICS,
              type=click.Path(),
              help='specify an metrics json',
              metavar='metrics')
@click.option('--model',
              default='lm',
              type=click.Choice(['lm', 'rf']),
              help='specify a model to use')
def main(**kwargs):
    """assume inclusion of necessary features and exclusion of the others
    """

    wrap_train_and_validate(kwargs['train'],
                            kwargs['valid'],
                            kwargs['output'],
                            kwargs['metrics'],
                            kwargs['model'])


def wrap_train_and_validate(train, valid, output, metrics, model):
    """label must be on -1 column in train and valid data
    """

    with open(train, 'r') as fin:
        train_data = pd.read_csv(fin,
                                 header=0,
                                 sep=",",
                                 encoding='utf-8')

    with open(valid, 'r') as fin:
        valid_data = pd.read_csv(fin,
                                 header=0,
                                 sep=",",
                                 encoding='utf-8')

    pipeline, r2_train, rmsle_train, r2_valid, rmsle_valid = \
        train_and_validate(train_data, valid_data, model)

    metrics_dict = { 'r2_train': r2_train,
                     'rmsle_train': rmsle_train,
                     'r2_valid': r2_valid,
                     'rmsle_valid': rmsle_valid }

    with open(metrics, 'w') as fout:
        json.dump(metrics_dict, fout)

    with open(output, 'wb') as fout:
        pickle.dump(pipeline, fout)

    set_tracking_uri(DEFAULT_URI)
    log_artifact(output)


def train_and_validate(train, valid, model='lm'):
    """train a model and evaluate it with train and valid data
    """

    for i in (train, valid):
        assert isinstance(i, pd.DataFrame), \
            'Error: data must be pandas.DataFrame.'

    train = train.values.astype('f8')
    valid = valid.values.astype('f8')

    x_train, y_train = train[:, :-1], train[:, -1]
    x_valid, y_valid = valid[:, :-1], valid[:, -1]

    pipeline = train_pipeline(x_train, y_train, model)

    r2_train, rmsle_train = calculate_metrics(x_train, y_train, pipeline)
    r2_valid, rmsle_valid = calculate_metrics(x_valid, y_valid, pipeline)

    set_tracking_uri(DEFAULT_URI)
    log_metric('r2_train', r2_train)
    log_metric('r2_valid', r2_valid)
    log_metric('rmsle_train', rmsle_train)
    log_metric('rmsle_valid', rmsle_valid)
    log_model(pipeline, 'pipeline_' + model)

    return pipeline, r2_train, rmsle_train, r2_valid, rmsle_valid


def train_pipeline(x, y, model='lm'):
    """using data, train either model of linear regression or
    random forest, calculate metrics, save a pipeline.
    """

    assert isinstance(x, np.ndarray), 'Error: x must be a numpy.ndarray'
    assert isinstance(y, np.ndarray), 'Error: y must be a numpy.ndarray'

    estimators = [('scaler', StandardScaler()),
                  ('model', MODEL_DICT[model])]
    pipeline = Pipeline(estimators)
    pipeline.fit(x, y)

    return pipeline


if __name__=='__main__':
    main()
