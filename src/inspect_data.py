#!/usr/local/bin/python

import os
import click
import numpy as np
import pandas as pd


FILE_DIR = os.path.dirname(os.path.abspath(__file__))
DEFAULT_INPUT = os.path.join(FILE_DIR, '../data/raw/new.csv')
DEFAULT_DTYPE = {'Id': np.uint16,
                 'MSSubClass': np.int16,
                 'MSZoning': str,
                 'LotFrontage': np.float32,
                 'LotArea': np.int64,
                 'Street': str,
                 'Alley': str,
                 'LotShape': str,
                 'LandContour': str,
                 'Utilities': str,
                 'LotConfig': str,
                 'LandSlope': str,
                 'Neighborhood': str,
                 'Condition1': str,
                 'Condition2': str,
                 'BldgType': str,
                 'HouseStyle': str,
                 'OverallQual': np.uint8,
                 'OverallCond': np.uint8,
                 'YearBuilt': np.uint16,
                 'YearRemodAdd': np.uint16,
                 'RoofStyle': str,
                 'RoofMatl': str,
                 'Exterior1st': str,
                 'Exterior2nd': str,
                 'MasVnrType': str,
                 'MasVnrArea': np.float32,
                 'ExterQual': str,
                 'ExterCond': str,
                 'Foundation': str,
                 'BsmtQual': str,
                 'BsmtCond': str,
                 'BsmtExposure': str,
                 'BsmtFinType1': str,
                 'BsmtFinSF1': np.int32,
                 'BsmtFinType2': str,
                 'BsmtFinSF2': np.int32,
                 'BsmtUnfSF': np.int32,
                 'TotalBsmtSF': np.int32,
                 'Heating': str,
                 'HeatingQC': str,
                 #'CentralAir': bool,
                 'Electrical': str,
                 '1stFlrSF': np.int32,
                 '2ndFlrSF': np.int32,
                 'LowQualFinSF': np.int32,
                 'GrLivArea': np.int32,
                 'BsmtFullBath': np.uint8,
                 'BsmtHalfBath': np.uint8,
                 'FullBath': np.uint8,
                 'HalfBath': np.uint8,
                 'BedroomAbvGr': np.uint8,
                 'KitchenAbvGr': np.uint8,
                 'KitchenQual': str,
                 'TotRmsAbvGrd': np.uint8,
                 'Functional': str,
                 'Fireplaces': np.uint8,
                 'FireplaceQu': str,
                 'GarageType': str,
                 'GarageYrBlt': np.float32,
                 'GarageFinish': str,
                 'GarageCars': np.uint8,
                 'GarageArea': np.int32,
                 'GarageQual': str,
                 'GarageCond': str,
                 'PavedDrive': str,
                 'WoodDeckSF': np.int32,
                 'OpenPorchSF': np.int32,
                 'EnclosedPorch': np.int32,
                 '3SsnPorch': np.int32,
                 'ScreenPorch': np.int32,
                 'PoolArea': np.int32,
                 'PoolQC': str,
                 'Fence': str,
                 'MiscFeature': str,
                 'MiscVal': np.int32,
                 'MoSold': np.uint8,
                 'YrSold': np.int32,
                 'SaleType': str,
                 'SaleCondition': str,
                 'SalePrice': np.uint16
                 }


@click.command()
@click.option('-i',
              '--input',
              default=DEFAULT_INPUT,
              type=click.Path(exists=True),
              help='specify an input file',
              metavar='input')
def main(**kwargs):
    """Here is a comment.
    """

    inspect_data(kwargs['input'])


def inspect_data(input):
    """Here is a comment.
    """

    with open(input, 'r') as fin:
        try:
            pd.read_csv(input,
                        header=0,
                        sep=",",
                        encoding='utf-8',
                        dtype=DEFAULT_DTYPE)
        except Exception:
            print('dtype is invalid.')
    return 1


if __name__=='__main__':
    main()
