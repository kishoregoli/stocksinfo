import argparse
import csv
import datetime
import json
import os
import urllib2

from logging_api import LOGGER
from psql_connector import PsqlConnector


ROOT_PATH = os.path.dirname(os.path.abspath(__name__))
DOWNLOADS_PATH = os.path.join(ROOT_PATH, 'Downloads')
NSE_DAILY_INDICES_CSV_FILENAME = 'ind_close_all_{day}{month}{year}.csv'
NSE_DAILY_INDICES_JSON_FILENAME = 'ind_close_all_{day}{month}{year}.json'
NSE_DAILY_INDICES_URL = 'https://www.nseindia.com/content/indices/ind_close_all_{day}{month}{year}.csv'
NSE_DAILY_INDICES_HEADERS = {
    'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.11 (KHTML, like Gecko) Chrome/23.0.1271.64 Safari/537.11',
    'Accept-Language': 'en-US,en;q=0.8',
    'Connection': 'keep-alive',
    'Content-Type': 'application/csv',
    'Accept': '*/*',
    'Host': 'nseindia.com'
}

NSE_DAILY_INDICES_FIELD_NAMES = ("index_name", "index_date", "open_index_value", "high_index_value", "low_index_value", "close_index_value", "points_change", "percent_change",
                              "volume", "turn_over", "pe", "pb", "div_yield")


def update_file_formats(day, month, year):
    global NSE_DAILY_INDICES_URL, NSE_DAILY_INDICES_CSV_FILENAME, NSE_DAILY_INDICES_JSON_FILENAME
    NSE_DAILY_INDICES_URL = NSE_DAILY_INDICES_URL.format(day=day, month=month, year=year)
    NSE_DAILY_INDICES_CSV_FILENAME = NSE_DAILY_INDICES_CSV_FILENAME.format(day=day, month=month, year=year)
    NSE_DAILY_INDICES_JSON_FILENAME = NSE_DAILY_INDICES_JSON_FILENAME.format(day=day, month=month, year=year)


def download_nse_daily_indices(day):
    if day:
        backup_day = datetime.datetime.strptime(day, '%Y-%m-%d').date()
    else:
        backup_day = datetime.datetime.strptime(str(datetime.datetime.now().date()), '%Y-%m-%d').date()
    print backup_day
    year, month, _day = backup_day.year, str(backup_day.month).zfill(2), str(backup_day.day).zfill(2)
    update_file_formats(_day, month, year)
    req = urllib2.Request(NSE_DAILY_INDICES_URL, headers=NSE_DAILY_INDICES_HEADERS)
    try:
        page = urllib2.urlopen(req)
        file_path = os.path.join(DOWNLOADS_PATH, NSE_DAILY_INDICES_CSV_FILENAME)
        print file_path
        if not os.path.exists(os.path.dirname(file_path)):
            os.makedirs(os.path.dirname(file_path))
        with open(file_path, 'wb') as writer:
            writer.write(page.read())
        return file_path
    except urllib2.HTTPError as http_error:
        LOGGER.error("Failed to download URL: {}. Exception: {}".format(NSE_DAILY_INDICES_URL.format(day=_day, month=month, year=year), str(http_error)))
        raise http_error
    except Exception as exp:
        LOGGER.error("Error occurred while processing nse_daily_indices. Exception: {}".format(str(exp)))
        raise exp


def nse_daily_indices_csv_to_json(csvfile, fieldnames):
    with open(csvfile, 'rb') as reader:
        file_path = os.path.join(DOWNLOADS_PATH, NSE_DAILY_INDICES_JSON_FILENAME)
        with open(file_path, 'wb') as writer:
            reader.readline()
            csvreader = csv.DictReader(reader, fieldnames=fieldnames)
            for row in csvreader:
                writer.write(json.dumps({unicode(k, errors='ignore'): unicode(v, errors='ignore').strip() for k, v in row.items()}))
                writer.write('\n')
    return file_path


def update_nsestocks_db(json_file):
    queries = []
    query = 'INSERT INTO nse_daily_indices(index_name, index_date, open_index_value, high_index_value, low_index_value, close_index_value, points_change, pe) values  \
            (%s, %s, %s, %s, %s, %s, %s, %s) ON CONFLICT DO NOTHING;'
    with open(json_file) as reader:
        for line in reader.readlines():
            data = json.loads(line)
            for key, value in data.items():
                if value == '-' or value == '':
                    data[key] = None
            queries.append([query, (data['index_name'], datetime.datetime.strptime(data['index_date'], '%d-%m-%Y').strftime('%d-%b-%Y'), data['open_index_value'], data['high_index_value'],
                                    data['low_index_value'], data['close_index_value'], data['points_change'], data['pe'])])
        psql_conn = PsqlConnector(datbase='testdb')
        psql_conn.execute_many(queries)


def main(day, update_db=False):
    json_path = nse_daily_indices_csv_to_json(download_nse_daily_indices(day), NSE_DAILY_INDICES_FIELD_NAMES)
    if update_db:
        update_nsestocks_db(json_path)


def parse_args():
    """
    """
    parser = argparse.ArgumentParser(
        description='nse stocks information')
    parser.add_argument('--day', type=str, help='Day from to backup - <YYYY-MM-DD>', default=None)
    # parser.add_argument('--days', default=0, type=int, help='Number of days to backup, default 0 means the day itself')
    parser.add_argument('--update_db', action='store_true', dest='update_db', help='update Database', default=True)
    return parser.parse_args()

if __name__ == '__main__':
    """
    """
    ARGS = parse_args()
    main(ARGS.day, ARGS.update_db)
