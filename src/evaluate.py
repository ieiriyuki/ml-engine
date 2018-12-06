#!/usr/local/bin/python

import os
import json
import click
import numpy as np
from datetime import datetime
from sklearn.preprocessing import StandardScaler
from sklearn.linear_model import LinearRegression
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_squared_log_error


FILE_DIR = os.path.dirname(os.path.abspath(__file__))
NOW = datetime.now().strftime("%Y%m%d-%H%M%S")
DEFAULT_MODELSET = os.path.join(FILE_DIR, '../data/pickles/modelset.pkl')
DEFAULT_OUTPUT = os.path.join(FILE_DIR,
                              '../data/prepared/metrics' +  NOW +  '.json')


# not fully implemented
@click.command()
@click.option('-m',
              '--model',
              default=DEFAULT_MODELSET,
              type=click.Path(),
              help='specify a modelset to calculate metrics',
              metavar='m')
@click.option('-o',
              '--output',
              default=DEFAULT_OUTPUT,
              type=click.Path(),
              help='specify an output file',
              metavar='output')
def evoke_calculate_metrics(**kwargs):
    """here is a help description. This should not work yet.
    """
    print('This is under construction.')

    return 1


def calculate_metrics(x, y, pipeline):
    """implicitly assume a pipeline that includes scaling and model
    """

    r2 = pipeline.score(x, y)
    prediction = pipeline.predict(x).flatten().tolist()
    rmsle = np.sqrt(mean_squared_log_error(y, prediction))

    return r2, rmsle


# not fully implemented
if __name__=='__main__':
    evoke_calculate_metrics()
