from mysql_queries import *
from mysql_api import MysqlApi


class DbClient:

    def __init__(self):
        self.mysqldb = MysqlApi()

    def update_consolidated_profit_before_tax(self, json_params):
        self.mysqldb.execute(UPDATE_CONSOLIDATED_PROFIT_BEFORE_TAX, json_params)

    def update_consolidated_net_sales(self, json_params):
        self.mysqldb.execute(UPDATE_CONSOLIDATED_NET_SALES, json_params)

    def update_consolidated_balance_sheet(self, json_params):
        self.mysqldb.execute(UPDATE_CONSOLIDATED_BALANCE_SHEET, json_params)

    def update_standalone_net_profit(self, json_params):
        self.mysqldb.execute(UPDATE_STANDALONE_NET_PROFIT, json_params)

    def update_standalone_net_sales(self, json_params):
        self.mysqldb.execute(UPDATE_STANDALONE_NET_SALES, json_params)

    def update_standalone_profit_before_tax(self, json_params):
        self.mysqldb.execute(UPDATE_STANDALONE_PROFIT_BEFORE_TAX, json_params)

    def update_standalone_other_income(self, json_params):
        self.mysqldb.execute(UPDATE_STANDALONE_OTHER_INCOME, json_params)

    def update_standalone_balance_sheet(self, json_params):
        self.mysqldb.execute(UPDATE_STANDALONE_BALANCE_SHEET, json_params)

    def update_consolidated_other_income(self, json_params):
        self.mysqldb.execute(UPDATE_CONSOLIDATED_OTHER_INCOME, json_params)

    def update_consolidated_net_profit(self, json_params):
        self.mysqldb.execute(UPDATE_CONSOLIDATED_NET_PROFIT, json_params)

    def update_nse_daily_data(self, json_params):
        self.mysqldb.execute(UPDATE_NSE_DAILY_DATA, json_params)

    def update_results_calender(self, json_params):
        self.mysqldb.execute(UPDATE_RESULTS_CALENDER, json_params)