#!/usr/local/bin/python

import os
import click
import pandas as pd
from datetime import datetime
from sklearn.model_selection import train_test_split


FILE_DIR = os.path.dirname(os.path.abspath(__file__))
NOW = datetime.now().strftime("%Y%m%d-%H%M%S")
DEFAULT_INPUT = os.path.join(FILE_DIR, '../data/prepared/alignmented_data.csv')
DEFAULT_TRAIN = os.path.join(FILE_DIR,
                             '../data/prepared/data_train_' + NOW + '.csv')
DEFAULT_VALID = os.path.join(FILE_DIR,
                             '../data/prepared/data_valid_' + NOW + '.csv')
RANDOM_SEED = 1234
VALID_RATIO = 0.25


@click.command()
@click.option('-i',
              '--input',
              default=DEFAULT_INPUT,
              type=click.Path(exists=True),
              help='specify an input file',
              metavar='input')
@click.option('-t',
              '--train',
              default=DEFAULT_TRAIN,
              type=click.Path(),
              help='specify an output train data',
              metavar='train')
@click.option('-v',
              '--valid',
              default=DEFAULT_VALID,
              type=click.Path(),
              help='specify an output valid data',
              metavar='valid')
@click.option('-r',
              '--ratio',
              default=VALID_RATIO,
              help='specify the ratio of validation',
              metavar='ratio')
@click.option('-s',
              '--seed',
              default=RANDOM_SEED,
              help='specify the initial random seed',
              metavar='seed')
def main(**kwargs):
    """split train and validation data using train_test_split()
    """

    wrap_train_test_split(kwargs['input'],
                          kwargs['train'],
                          kwargs['valid'],
                          kwargs['ratio'],
                          kwargs['seed'])


def wrap_train_test_split(input, train, valid, ratio, seed):
    """Here is a comment.
    """

    with open(input, 'r') as fin:
        data = pd.read_csv(fin,
                           header=0,
                           sep=",",
                           encoding='utf-8')

    train_data, valid_data = train_test_split(data,
                                              test_size=ratio,
                                              random_state=seed)

    with open(train, 'w') as fout:
        train_data.to_csv(fout, index=False)

    with open(valid, 'w') as fout:
        valid_data.to_csv(fout, index=False)


if __name__=='__main__':
    main()
