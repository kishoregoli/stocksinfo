import argparse
import csv
import json
import os
import sys
import urllib2

from logging_api import LOGGER
from psql_connector import PsqlConnector


ROOT_PATH = os.path.dirname(os.path.abspath(__name__))
DOWNLOADS_PATH = os.path.join(ROOT_PATH, 'Downloads')
SECURITIES_CSV_FILENAME = 'EQUITY_L.csv'
SECURITIES_JSON_FILENAME = 'EQUITY_L.json'
SECURITIES_URL = 'https://www.nseindia.com/content/equities/EQUITY_L.csv'
SECURITIES_HEADERS = {
            'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.11 (KHTML, like Gecko) Chrome/23.0.1271.64 Safari/537.11',
            'Accept-Language': 'en-US,en;q=0.8',
            'Connection': 'keep-alive',
            'Content-Type': 'application/csv',
            'Accept': '*/*',
            'Host': 'nseindia.com'
}

SECURITIES_FIELD_NAMES = ('symbol', 'company_name', 'series', 'listing_date', 'paid_up_value', 'market_lot', 'isin_number', 'face_value')


def download_securities():
    req = urllib2.Request(SECURITIES_URL, headers=SECURITIES_HEADERS)
    try:
        page = urllib2.urlopen(req)
        file_path = os.path.join(DOWNLOADS_PATH, SECURITIES_CSV_FILENAME)
        if not os.path.exists(os.path.dirname(file_path)):
            os.makedirs(os.path.dirname(file_path))
        with open(file_path, 'w') as writer:
            writer.write(page.read())
        return file_path
    except urllib2.HTTPError as http_error:
        LOGGER.error("Failed to download URL: {}. Exception: {}".format(SECURITIES_URL, str(http_error)))
    except Exception as exp:
        LOGGER.error("Error occurred while processing securities. Exception: {}".format(str(exp)))


def securities_csv_to_json(csvfile, fieldnames):
    with open(csvfile, 'rb') as reader:
        file_path = os.path.join(DOWNLOADS_PATH, SECURITIES_JSON_FILENAME)
        with open(file_path, 'wb') as writer:
            reader.readline()
            csvreader = csv.DictReader(reader, fieldnames=fieldnames)
            for row in csvreader:
                writer.write(json.dumps({unicode(k, errors='ignore'): unicode(v, errors='ignore') for k, v in row.items()}))
                writer.write('\n')
    return file_path


def update_nse_securities_db(json_file):
    queries = []
    query = 'INSERT INTO nse_securities(symbol, company_name, series, listing_date, isin_number, face_value) values  \
            (%s, %s, %s, %s, %s, %s) ON CONFLICT DO NOTHING;'
    with open(json_file) as reader:
        for line in reader.readlines():
            data = json.loads(line)
            queries.append([query, (data['symbol'], data['company_name'], data['series'], data['listing_date'],
                                    data['isin_number'], data['face_value'])])
        psql_conn = PsqlConnector(datbase='testdb')
        psql_conn.execute_many(queries)


def main(update_db=False):
    json_path = securities_csv_to_json(download_securities(), SECURITIES_FIELD_NAMES)
    if update_db:
        update_nse_securities_db(json_path)


def parse_args():
    """
    """
    parser = argparse.ArgumentParser(
        description='nse stocks information')
    parser.add_argument('--update_db', action='store_true', dest='update_db', help='update Database', default=True)
    return parser.parse_args()

if __name__ == '__main__':
    """
    """

    ARGS = parse_args()
    main(ARGS.update_db)




