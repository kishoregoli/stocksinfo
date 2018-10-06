import yaml
'''
{"symbol": "SOLARINDS", "financials": "{\"consolidated_data\": {\"Net Sales\": [\"614.72\", \"575.34\", \"465.68\", \"408.40\"], 
\"Consolidated\": [\"Jun'18\", \"Mar'18\", \"Dec'17\", \"Sep'17\"], 
\"Other Income\": [\"7.66\", \"3.76\", \"2.62\", \"3.25\"], \"PBDIT\": [\"128.22\", \"118.14\", \"104.31\", \"87.22\"], 
\"Net Profit\": [\"72.92\", \"67.78\", \"57.68\", \"48.25\"]}, \"standalone_bs_data\": {\"Net Worth\": [\"759.21\"], 
\"Total Debt\": [\"96.48\"], \"Net Block\": [\"420.18\"], \"Total Share Capital\": [\"18.10\"], \"Total Assets\": [\"855.69\"], 
\"Investments\": [\"65.52\"]}, \"consolidated_bs_data\": {\"Net Worth\": [\"1,083.86\"], \"Total Debt\": [\"387.85\"], \"Net Block\": [\"923.28\"], \"Total Share Capital\": [\"18.10\"], \"Total Assets\": [\"1,519.09\"], \"Investments\": [\"17.05\"]}, \"standalone_data\": {\"Net Sales\": [\"388.44\", \"393.27\", \"313.02\", \"251.86\"], \"Other Income\": [\"7.54\", \"5.47\", \"4.19\", \"4.55\"], \"PBDIT\": [\"76.68\", \"69.30\", \"53.19\", \"43.29\"], \"Net Profit\": [\"48.74\", \"41.65\", \"30.50\", \"24.04\"], \"Standalone\": [\"Jun'18\", \"Mar'18\", \"Dec'17\", \"Sep'17\"]}}"}
'''


def get_quarterly_data(financial_data, quarters, symbol):
    q1, q2, q3, q4 = 0, 0, 0, 0
    if type(financial_data) == list:
        for quarter, data in zip(quarters, financial_data):
            try:
                float_data = float(data)
                if "Mar" in quarter:
                    q1 = float_data
                elif "Jun" in quarter:
                    q2 = float_data
                elif "Sep" in quarter:
                    q3 = float_data
                elif "Dec" in quarter:
                    q4 = float_data
            except:
                pass
    return {
        "symbol": symbol,
        "q1": q1,
        "q2": q2,
        "q3": q3,
        "q4": q4
    }


def parse_financial_data(str_data, validator="Jun18"):
    data = yaml.safe_load(str_data)
    symbol = data['symbol']
    print "Parsing for symbol: {}".format(symbol)
    financials = yaml.safe_load(data['financials'])
    if not any(quarter.replace("'", "").lower() == validator.lower() for quarter in financials['standalone_data']['Standalone']):
        return
    consolidated_quarters = financials['consolidated_data']['Consolidated']
    consolidated_net_sales = get_quarterly_data(financials['consolidated_data'].get('Net Sales', financials['consolidated_data'].get('Interest Earned')), consolidated_quarters, symbol)
    consolidated_other_income = get_quarterly_data(financials['consolidated_data']['Other Income'], consolidated_quarters, symbol)
    consolidated_profit_before_tax = get_quarterly_data(financials['consolidated_data'].get('PBDIT', financials['consolidated_data'].get('Total Expenses')), consolidated_quarters, symbol)
    consolidated_net_profit = get_quarterly_data(financials['consolidated_data']['Net Profit'], consolidated_quarters, symbol)
    consolidated_bs_data = financials['consolidated_bs_data']
    consolidated_bs_data = {key: float(data[0].replace(",", "")) for key, data in consolidated_bs_data.items()}
    consolidated_balance_sheet = {
        'symbol': symbol,
        'total_share_capital': consolidated_bs_data['Total Share Capital'],
        'net_worth': consolidated_bs_data['Net Worth'],
        'total_debt': consolidated_bs_data['Total Debt'],
        'net_block': consolidated_bs_data['Net Block'],
        'investments': consolidated_bs_data['Investments'],
        'total_assets': consolidated_bs_data['Total Assets']
    }
    standalone_quarters = financials['standalone_data']['Standalone']
    standalone_net_sales = get_quarterly_data(financials['standalone_data'].get('Net Sales', financials['standalone_data'].get('Interest Earned')), standalone_quarters,
                                                symbol)
    standalone_other_income = get_quarterly_data(financials['standalone_data']['Other Income'],
                                                   standalone_quarters, symbol)
    standalone_profit_before_tax = get_quarterly_data(financials['standalone_data'].get('PBDIT' , financials['standalone_data'].get('Total Expenses')), standalone_quarters,
                                                        symbol)
    standalone_net_profit = get_quarterly_data(financials['standalone_data']['Net Profit'], standalone_quarters,
                                                 symbol)
    standalone_bs_data = financials['standalone_bs_data']
    standalone_bs_data = {key: float(data[0].replace(",", "")) for key, data in standalone_bs_data.items()}
    standalone_balance_sheet = {
        'symbol': symbol,
        'total_share_capital': standalone_bs_data['Total Share Capital'],
        'net_worth': standalone_bs_data['Net Worth'],
        'total_debt': standalone_bs_data['Total Debt'],
        'net_block': standalone_bs_data['Net Block'],
        'investments': standalone_bs_data['Investments'],
        'total_assets': standalone_bs_data['Total Assets']
    }
    return {
        'consolidated_net_sales': consolidated_net_sales,
        'consolidated_other_income': consolidated_other_income,
        'consolidated_profit_before_tax': consolidated_profit_before_tax,
        'consolidated_net_profit': consolidated_net_profit,
        'consolidated_balance_sheet': consolidated_balance_sheet,
        'standalone_net_sales': standalone_net_sales,
        'standalone_other_income': standalone_other_income,
        'standalone_profit_before_tax': standalone_profit_before_tax,
        'standalone_net_profit': standalone_net_profit,
        'standalone_balance_sheet': standalone_balance_sheet
    }


