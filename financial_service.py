from fin_parser import parse_financial_data
from dbclient import DbClient


class FinancialService:
    def __init__(self):
        self.dbclient = DbClient()
        pass

    def update_financial_data(self, str_data, validator):
        parsed_fin_data = parse_financial_data(str_data, validator)
        if parsed_fin_data:
            self.dbclient.update_consolidated_profit_before_tax(parsed_fin_data['consolidated_profit_before_tax'])
            self.dbclient.update_consolidated_net_sales(parsed_fin_data['consolidated_net_sales'])
            self.dbclient.update_consolidated_balance_sheet(parsed_fin_data['consolidated_balance_sheet'])
            self.dbclient.update_standalone_net_profit(parsed_fin_data['standalone_net_profit'])
            self.dbclient.update_standalone_net_sales(parsed_fin_data['standalone_net_sales'])
            self.dbclient.update_standalone_profit_before_tax(parsed_fin_data['standalone_profit_before_tax'])
            self.dbclient.update_standalone_other_income(parsed_fin_data['standalone_other_income'])
            self.dbclient.update_standalone_balance_sheet(parsed_fin_data['standalone_balance_sheet'])
            self.dbclient.update_consolidated_other_income(parsed_fin_data['consolidated_other_income'])
            self.dbclient.update_consolidated_net_profit(parsed_fin_data['consolidated_net_profit'])



