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
if not os.path.exists(DOWNLOADS_PATH):
    os.makedirs(DOWNLOADS_PATH)

if not os.path.exists(OUTPUT_PATH):
    os.makedirs(OUTPUT_PATH)

logging.basicConfig(filename=os.path.join(OUTPUT_PATH, 'nse_daily_data_reader.log'), level=logging.INFO)

NSE_DAILY_DATA_CSV_ZIP_FILENAME = 'cm{day}{month}{year}bhav.csv.zip'
NSE_DAILY_DATA_CSV_FILENAME = 'cm{day}{month}{year}bhav.csv'
NSE_DAILY_DATA_URL = 'https://www.nseindia.com/content/historical/EQUITIES/{year}/{month}/cm{day}{month}{year}bhav.csv.zip'
NSE_DAILY_DATA_HEADERS = {
    'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.11 (KHTML, like Gecko) Chrome/23.0.1271.64 Safari/537.11',
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
    'Accept-Charset': 'ISO-8859-1,utf-8;q=0.7,*;q=0.3',
    'Accept-Encoding': 'none',
    'Accept-Language': 'en-US,en;q=0.8',
    'Connection': 'keep-alive'
}

MONTH_NAMES = {"01": "JAN", "02": "FEB", "03": "MAR", "04": "APR", "05": "MAY", "06": "JUN", "07": "JUL", "08": "AUG",
               "09": "SEP", "10": "OCT", "11": "NOV", "12": "DEC"}

NSE_DAILY_DATA_COLUMNS = ['symbol', 'series', 'open', 'high', 'low', 'close', 'last', 'prev_close', 'total_trade_qty',
                          'total_trade_val', 'added_on', 'total_trades', 'isin', 'empty']


def main(backup_day):
    global NSE_DAILY_DATA_URL, NSE_DAILY_DATA_CSV_ZIP_FILENAME, NSE_DAILY_DATA_CSV_FILENAME, DOWNLOADS_PATH
    year, month, _day = backup_day.split('-')[0], MONTH_NAMES[backup_day.split('-')[1]], backup_day.split('-')[2]
    NSE_DAILY_DATA_URL = NSE_DAILY_DATA_URL.format(day=_day, month=month, year=year)
    NSE_DAILY_DATA_CSV_ZIP_FILENAME = NSE_DAILY_DATA_CSV_ZIP_FILENAME.format(day=_day, month=month, year=year)
    NSE_DAILY_DATA_CSV_FILENAME = NSE_DAILY_DATA_CSV_FILENAME.format(day=_day, month=month, year=year)
    logging.info("Started backup for the day: {}".format(backup_day))
    file_path = os.path.join(DOWNLOADS_PATH, NSE_DAILY_DATA_CSV_ZIP_FILENAME)
    if not os.path.exists(file_path):
        if not os.path.exists(os.path.dirname(file_path)):
            os.makedirs(os.path.dirname(file_path))
        print NSE_DAILY_DATA_URL
        req = urllib2.Request(NSE_DAILY_DATA_URL, headers=NSE_DAILY_DATA_HEADERS)
        page = urllib2.urlopen(req)
        with open(file_path, 'wb') as writer:
            writer.write(page.read())
    zf = zipfile.ZipFile(file_path)
    df = pd.read_csv(zf.open(NSE_DAILY_DATA_CSV_FILENAME), skiprows=1,
                     names=NSE_DAILY_DATA_COLUMNS)
    del df['empty']
    dbClient = DbClient()
    for i, record in enumerate(yaml.safe_load(df.to_json(orient='records'))):
        record['added_on'] = datetime.datetime.strptime(backup_day, "%Y-%m-%d").strftime('%Y-%m-%d %H:%M:%S')
        record['p_change'] = round((float(record['close']) - float(record['prev_close'])), 2)
        record['change_percent'] = round(
            (float(record['close']) - float(record['prev_close'])) / float(record['prev_close']) * 100, 2)
        dbClient.update_nse_daily_data(record)


def parse_args():
    """
    """
    parser = argparse.ArgumentParser(
        description='nse stocks daily data')
    parser.add_argument('--day', type=str, help='Day from to backup - <YYYY-MM-DD>',
                        default=str(datetime.datetime.now().date() - datetime.timedelta(1)))
    return parser.parse_args()


if __name__ == '__main__':
    """
    """
    ARGS = parse_args()
    main(ARGS.day)
