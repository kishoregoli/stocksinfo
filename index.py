from financial_service import FinancialService

fin_service = FinancialService()

filename = 'financials_jun18.json'
validator = (filename.split("_")[1]).split(".")[0]

with open(filename) as reader:
    for line in reader:
        try:
            fin_service.update_financial_data(line, validator)
        except Exception as e:
            print "Failed for symbol: {}".format(line)