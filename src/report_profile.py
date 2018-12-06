#!/usr/loval/bin/python

import os
import sys
import hashlib
import click
import webbrowser
import pandas as pd
import pandas_profiling


FILE_DIR = os.path.dirname(os.path.abspath(__file__))
DEFAULT_INPUT = os.path.join(FILE_DIR, '../data/raw/old.csv')
DEFAULT_OUTPUT_PATH = os.path.join(FILE_DIR, '../data/profile/')


@click.command()
@click.option('-i',
              '--input',
              default=DEFAULT_INPUT,
              help='CSV file to profile',
              metavar='input')
@click.option('-o',
              '--output',
              default=None,
              help='Output report file',
              metavar='output')
@click.option('-s',
              '--silent',
              is_flag=True,
              default=True,
              help="Only generate but do not open report",
              metavar='s')
def main(**kwargs):
    """Profile the variables in a CSV file and generate a HTML report.
    """

    wrap_report_profile(kwargs['input'], kwargs['output'], kwargs['silent'])


def wrap_report_profile(input, output=None, silent=True):

    with open(input, 'r') as fin:
        data = pd.read_csv(fin,
                           header=0,
                           sep=",",
                           encoding='utf-8')

    if output==None:
        output = create_file_name(input)

    report_profile(data=data, output=output, s=silent)


def report_profile(data, output, s=True):
    assert isinstance(data, pd.DataFrame), \
        'Error: data must be a pandas.DataFrame.'

    pandas_profiling.ProfileReport(data).to_file(output)
    #if not s:
    #    webbrowser.open_new_tab(prof.file.name)


def create_file_name(base_name):
    md5 = hashlib.md5(base_name.encode('utf-8')).hexdigest()
    file_name = DEFAULT_OUTPUT_PATH + \
        'profile_' + \
        md5 + \
        '.html'
    return file_name


if __name__ == "__main__":
    main()
