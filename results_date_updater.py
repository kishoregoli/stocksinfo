import argparse
import datetime
import logging
import os
import urllib2
import zipfile
import yaml

import pandas as pd
from dbclient import DbClient

DOWNLOADS_PATH = os.path.join(os.path.dirname(os.path.realpath(__file__)), "downloads")
OUTPUT_PATH = os.path.join(os.path.dirname(os.path.realpath(__file__)), "output")

RESULTS_CALENDER_PATH = os.path.join(DOWNLOADS_PATH, 'Results06102018.csv')

logging.basicConfig(filename=os.path.join(OUTPUT_PATH, 'results_date_updater.log'), level=logging.INFO)

RESULTS_CALENDER_COLUMNS = ['security_code', 'symbol', 'security_name', 'result_date']


def main():
    df = pd.read_csv(RESULTS_CALENDER_PATH, skiprows=1,
                     names=RESULTS_CALENDER_COLUMNS)
    dbClient = DbClient()
    for i, record in enumerate(yaml.safe_load(df.to_json(orient='records'))):
        record['result_date'] = datetime.datetime.strptime(record['result_date'], "%d %b %Y").strftime('%Y-%m-%d')
        dbClient.update_results_calender(record)


def parse_args():
    """
    """
    parser = argparse.ArgumentParser(
        description='results date updater')
    return parser.parse_args()


if __name__ == '__main__':
    """
    """
    ARGS = parse_args()
    main()

