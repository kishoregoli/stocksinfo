import datetime
import argparse

from elasticsearch import Elasticsearch
from elasticsearch.helpers import bulk

from mail_sender import send_mail
from mysql_api import MysqlApi


def main(day):
    mysql_api = MysqlApi()

    symbols_map = {}
    for record in mysql_api.get_records("SELECT symbol, min(close), max(close), avg(close), min(low) from nsedailydata group by symbol", None):
        symbols_map[record[0]] = {}
        symbol = symbols_map[record[0]]
        symbol['min_close'] = round(record[1], 2)
        symbol['max_close'] = round(record[2], 2)
        symbol['avg_close'] = round(record[3], 2)
        symbol['min_low'] = round(record[4], 2)
        symbol.update(
            {'c_net_worth': 0, 'c_total_debt': 0, 's_net_worth': 0, 's_total_debt': 0})
    result = mysql_api.get_records("SELECT cb.Symbol, cb.NetWorth, cb.TotalDebt, sb.NetWorth, sb.TotalDebt from consolidatedbalancesheets as cb inner join standalonebalancesheets as sb on cb.symbol=sb.symbol where cb.NetWorth != 0 and sb.NetWorth != 0 order by sb.Networth desc, cb.NetWorth desc;", None)
    for record in result:
        try:
            symbols_map[record[0]].update({'c_net_worth': record[1], 'c_total_debt': record[2], 's_net_worth': record[3], 's_total_debt': record[4]})
        except:
            pass
    for record in mysql_api.get_records("SELECT symbol, open, low, high, close, prevclose from nsedailydata where addedOn=(STR_TO_DATE('{day}', '%Y-%m-%d'))".format(day=day), None):
        if record[0] in symbols_map:
            symbol = symbols_map[record[0]]
            symbol['open'] = round(record[1], 2)
            symbol['low'] = round(record[2], 2)
            symbol['high'] = round(record[3], 2)
            symbol['close'] = round(record[4], 2)
            symbol['prev_close'] = round(record[5], 2)
            symbol['open_up'] = symbol['open'] > symbol['prev_close']
            symbol['close_up'] = symbol['close'] > symbol['open']
            symbol['change_per'] = round((symbol['close']-symbol['prev_close'])/symbol['prev_close'] * 100, 2)

    for record in mysql_api.get_records("select symbol, sum(round((close-prevclose)/prevclose * 100, 2)) from nsedailydata where addedOn BETWEEN (STR_TO_DATE('{day}', '%Y-%m-%d') - INTERVAL 3 DAY) AND STR_TO_DATE('{day}', '%Y-%m-%d') group by symbol".format(day=day), None):
        if record[0] in symbols_map:
            symbol = symbols_map[record[0]]
            symbol['sum_3_days_change_per'] = round(record[1], 2)

    for record in mysql_api.get_records("select symbol, sum(round((close-prevclose)/prevclose * 100, 2)) from nsedailydata where addedOn BETWEEN (STR_TO_DATE('{day}', '%Y-%m-%d') - INTERVAL 7 DAY) AND STR_TO_DATE('{day}', '%Y-%m-%d') group by symbol".format(day=day), None):
        if record[0] in symbols_map:
            symbol = symbols_map[record[0]]
            symbol['sum_7_days_change_per'] = round(record[1], 2)

    for record in mysql_api.get_records("select symbol, sum(round((close-prevclose)/prevclose * 100, 2)) from nsedailydata where addedOn BETWEEN (STR_TO_DATE('{day}', '%Y-%m-%d') - INTERVAL 15 DAY) AND STR_TO_DATE('{day}', '%Y-%m-%d') group by symbol".format(day=day), None):
        if record[0] in symbols_map:
            symbol = symbols_map[record[0]]
            symbol['sum_15_days_change_per'] = round(record[1], 2)

    for record in mysql_api.get_records("select symbol, sum(round((close-prevclose)/prevclose * 100, 2)) from nsedailydata where addedOn BETWEEN (STR_TO_DATE('{day}', '%Y-%m-%d') - INTERVAL 30 DAY) AND STR_TO_DATE('{day}', '%Y-%m-%d') group by symbol".format(day=day), None):
        if record[0] in symbols_map:
            symbol = symbols_map[record[0]]
            symbol['sum_30_days_change_per'] = round(record[1], 2)

    for record in mysql_api.get_records("SELECT symbol, resultdate from resultscalender", None):
        if record[0] in symbols_map:
            symbol = symbols_map[record[0]]
            symbol['result_date'] = record[1]

    messages = []
    i = 1
    for symbol, values in symbols_map.items():
        if values['c_total_debt'] != 0 or values['s_total_debt'] != 0:
            continue
        values['symbol'] = symbol
        values['timestamp'] = day
        messages.append({"_type": "data", "_id": "data-{}".format(i), "_source": values})
        i += 1
    es = Elasticsearch('localhost')
    success, _ = bulk(es, messages, index='stocks-zerodebts-{}'.format(day))

    my_symbols = sorted(['SASKEN', 'DBL', 'INFY', 'IGL', 'TITAN', 'BATAINDIA', 'GRAPHITE', 'NIACL', 'HDFCBANK', 'NBCC', 'GREAVESCOT', 'BPCL', 'VINYLINDIA',
                  'HFCL', 'CYIENT', 'GMBREW', 'EICHERMOT', 'RELIANCE'])

    body = """
        <table id='stocks'>
            <tr>
            <th>Symbol</th>
            <th>PrevClose</th>
            <th>Open</th>
            <th>Close</th>
            <th>Change %(today)</th>
            <th>Change %(3 days)</th>
            <th>Change %(7 days)</th>
            <th>Change %(15 days)</th>
            <th>Change %(30 days)</th>
            </tr>
    """
    for symbol in my_symbols:
        body += """
            <tr>
                <td>
                {symbol}
                </td>
                <td>{prev_close}</td>
                <td>{open}</td>
                <td>
                {close}
                </td>
                <td>
                {change_per}
                </td>
                <td>
                {sum_3_days_change_per}
                </td>
                <td>
                {sum_7_days_change_per}
                </td>
                <td>
                {sum_15_days_change_per}
                </td>
                <td>
                {sum_30_days_change_per}
                </td>
            </tr>
        """.format(symbol=symbol, prev_close=symbols_map[symbol]['prev_close'], open=symbols_map[symbol]['open'] ,close=symbols_map[symbol]['close'], change_per=symbols_map[symbol]['change_per'],
                   sum_3_days_change_per=symbols_map[symbol]['sum_3_days_change_per'],
                   sum_7_days_change_per=symbols_map[symbol]['sum_7_days_change_per'], sum_15_days_change_per=symbols_map[symbol]['sum_15_days_change_per']
        , sum_30_days_change_per = symbols_map[symbol]['sum_30_days_change_per'])

    body += """
        </table>
    """

    subject = "Stocks Info for the day: {}".format(day)
    send_mail(subject, body)


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
    





