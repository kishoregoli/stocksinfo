UPDATE_CONSOLIDATED_NET_SALES = "INSERT INTO ConsolidatedNetSales (Symbol, Q1, Q2, Q3, Q4) VALUES " \
                                "(%(symbol)s, %(q1)s, %(q2)s, %(q3)s, %(q4)s) " \
                                "ON DUPLICATE KEY UPDATE Q1=%(q1)s, Q2=%(q2)s, Q3=%(q3)s, Q4=%(q4)s"

UPDATE_CONSOLIDATED_OTHER_INCOME = "INSERT INTO ConsolidatedOtherIncomes (Symbol, Q1, Q2, Q3, Q4) VALUES " \
                                    "(%(symbol)s, %(q1)s, %(q2)s, %(q3)s, %(q4)s) " \
                                    "ON DUPLICATE KEY UPDATE Q1=%(q1)s, Q2=%(q2)s, Q3=%(q3)s, Q4=%(q4)s"

UPDATE_CONSOLIDATED_PROFIT_BEFORE_TAX = "INSERT INTO ConsolidatedProfitsBeforeTaxes (Symbol, Q1, Q2, Q3, Q4) VALUES " \
                                           "(%(symbol)s, %(q1)s, %(q2)s, %(q3)s, %(q4)s) " \
                                           "ON DUPLICATE KEY UPDATE Q1=%(q1)s, Q2=%(q2)s, Q3=%(q3)s, Q4=%(q4)s"

UPDATE_CONSOLIDATED_NET_PROFIT = "INSERT INTO ConsolidatedNetProfits (Symbol, Q1, Q2, Q3, Q4) VALUES " \
                                  "(%(symbol)s, %(q1)s, %(q2)s, %(q3)s, %(q4)s) " \
                                  "ON DUPLICATE KEY UPDATE Q1=%(q1)s, Q2=%(q2)s, Q3=%(q3)s, Q4=%(q4)s"

UPDATE_CONSOLIDATED_BALANCE_SHEET = "INSERT INTO ConsolidatedBalanceSheets (Symbol, TotalShareCapital, NetWorth, " \
                                     "TotalDebt, NetBlock, Investments, TotalAssets) VALUES " \
                                     "(%(symbol)s, %(total_share_capital)s, %(net_worth)s, %(total_debt)s, " \
                                     "%(net_block)s, %(investments)s, %(total_assets)s) " \
                                     "ON DUPLICATE KEY UPDATE TotalShareCapital=%(total_share_capital)s, " \
                                     "NetWorth=%(net_worth)s, TotalDebt=%(total_debt)s, NetBlock=%(net_block)s," \
                                     "Investments=%(investments)s, TotalAssets=%(total_assets)s"

UPDATE_STANDALONE_NET_SALES = "INSERT INTO StandaloneNetSales (Symbol, Q1, Q2, Q3, Q4) VALUES " \
                                "(%(symbol)s, %(q1)s, %(q2)s, %(q3)s, %(q4)s) " \
                                "ON DUPLICATE KEY UPDATE Q1=%(q1)s, Q2=%(q2)s, Q3=%(q3)s, Q4=%(q4)s"

UPDATE_STANDALONE_OTHER_INCOME = "INSERT INTO StandaloneOtherIncomes (Symbol, Q1, Q2, Q3, Q4) VALUES " \
                                    "(%(symbol)s, %(q1)s, %(q2)s, %(q3)s, %(q4)s) " \
                                    "ON DUPLICATE KEY UPDATE Q1=%(q1)s, Q2=%(q2)s, Q3=%(q3)s, Q4=%(q4)s"

UPDATE_STANDALONE_PROFIT_BEFORE_TAX = "INSERT INTO StandaloneProfitsBeforeTaxes (Symbol, Q1, Q2, Q3, Q4) VALUES " \
                                           "(%(symbol)s, %(q1)s, %(q2)s, %(q3)s, %(q4)s) " \
                                           "ON DUPLICATE KEY UPDATE Q1=%(q1)s, Q2=%(q2)s, Q3=%(q3)s, Q4=%(q4)s"

UPDATE_STANDALONE_NET_PROFIT = "INSERT INTO StandaloneNetProfits (Symbol, Q1, Q2, Q3, Q4) VALUES " \
                                  "(%(symbol)s, %(q1)s, %(q2)s, %(q3)s, %(q4)s) " \
                                  "ON DUPLICATE KEY UPDATE Q1=%(q1)s, Q2=%(q2)s, Q3=%(q3)s, Q4=%(q4)s"

UPDATE_STANDALONE_BALANCE_SHEET = "INSERT INTO StandaloneBalanceSheets (Symbol, TotalShareCapital, NetWorth, " \
                                     "TotalDebt, NetBlock, Investments, TotalAssets) VALUES " \
                                     "(%(symbol)s, %(total_share_capital)s, %(net_worth)s, %(total_debt)s, " \
                                     "%(net_block)s, %(investments)s, %(total_assets)s) " \
                                     "ON DUPLICATE KEY UPDATE TotalShareCapital=%(total_share_capital)s, " \
                                     "NetWorth=%(net_worth)s, TotalDebt=%(total_debt)s, NetBlock=%(net_block)s," \
                                     "Investments=%(investments)s, TotalAssets=%(total_assets)s"

UPDATE_NSE_DAILY_DATA = "INSERT IGNORE INTO NseDailyData (Symbol, Series, Open, High, Low, Close, Last, PrevClose, " \
    "TotalTradeQty, TotalTradeVal, AddedOn, TotalTrades, ISIN, pChange, ChangePercent) " \
    "VALUES (%(symbol)s, %(series)s, %(open)s, %(high)s, %(low)s, %(close)s, %(last)s, " \
    "%(prev_close)s, %(total_trade_qty)s, %(total_trade_val)s, %(added_on)s, %(total_trades)s, " \
    "%(isin)s, %(p_change)s, %(change_percent)s)"

UPDATE_RESULTS_CALENDER = "INSERT IGNORE INTO ResultsCalender (SecurityCode, Symbol, SecurityName, ResultDate) " \
                          "VALUES (%(security_code)s, %(symbol)s, %(security_name)s, %(result_date)s) ON DUPLICATE KEY " \
                          "UPDATE ResultDate=%(result_date)s"