import yahoo_fin.stock_info as si
import re
import csv
import json
from io import StringIO
from bs4 import BeautifulSoup
import requests
import yfinance as yf

import yahoofinancials

ticker = 'AAPL'
#yahoo_financials = YahooFinancials(ticker)


#historical_stock_prices = yahoo_financials.get_historical_price_data('2008-09-15', '2018-09-15', 'weekly')




sheet = si.get_cash_flow("aapl")
print(sheet.loc["netIncome"][0])







url_stats = "https://finance.yahoo.com/quote/{}/key-statistics?p={}"
url_profile = "https://finance.yahoo.com/quote/{}/profile?p={}"
url_financials = "https://finance.yahoo.com/quote/{}/financials?p={}"

stock = "AAPL"
response = requests.get(url_financials.format(stock, stock))
soup = BeautifulSoup(response.text, 'html.parser')
pattern = re.compile(r'\s--\sData\s--\s')
script_data = soup.find('script', text=pattern).contents[0]


start = script_data.find('context')-2
json_data = json.loads(script_data[start:-12])

json_data['context'].keys()

json_data['context']['dispatcher']['stores']['QuoteSummaryStore'].keys()

# income statement
annual_is = json_data['context']['dispatcher']['stores']['QuoteSummaryStore']['incomeStatementHistory']['incomeStatementHistory']
quarterly_is = json_data['context']['dispatcher']['stores']['QuoteSummaryStore']['incomeStatementHistoryQuarterly']['incomeStatementHistory']

# cash flow statement
annual_cf = json_data['context']['dispatcher']['stores']['QuoteSummaryStore']['cashflowStatementHistory']['cashflowStatements']
quarterly_cf = json_data['context']['dispatcher']['stores']['QuoteSummaryStore']['cashflowStatementHistoryQuarterly']['cashflowStatements']

# balance sheet
annual_bs = json_data['context']['dispatcher']['stores']['QuoteSummaryStore']['balanceSheetHistory']['balanceSheetStatements']
quarterly_bs = json_data['context']['dispatcher']['stores']['QuoteSummaryStore']['balanceSheetHistoryQuarterly']['balanceSheetStatements']

#print(annual_cf)
annual_is_stmts = []
quarterly_is_stmts = []


for s in annual_is:
    statement = {}
    for key, val in s.items():
        try:
            statement[key] = val['raw']
        except TypeError:
            continue
        except KeyError:
            continue
    annual_is_stmts.append(statement)
#print(annual_is_stmts)

#for i in range(0,4):
#    print(annual_is_stmts[i]['netIncome'])
for s in quarterly_is:
    statement = {}
    for key, val in s.items():
        try:
            statement[key] = val['raw']
        except TypeError:
            continue
        except KeyError:
            continue
    quarterly_is_stmts.append(statement)


annual_cf_stmts = []
quarterly_cf_stmts = []

# annual
for s in annual_cf:
    statement = {}
    for key, val in s.items():
        try:
            statement[key] = val['raw']
        except TypeError:
            continue
        except KeyError:
            continue
    annual_cf_stmts.append(statement)


# quarterly
for s in quarterly_cf:
    statement = {}
    for key, val in s.items():
        try:
            statement[key] = val['raw']
        except TypeError:
            continue
        except KeyError:
            continue
    quarterly_cf_stmts.append(statement)

annual_bs_stmts = []

for s in annual_bs:
    statement = {}
    for key, val in s.items():
        try:
            statement[key] = val['raw']
        except TypeError:
            continue
        except KeyError:
            continue
    annual_bs_stmts.append(statement)



#for i in range(0,4):
#    print(annual_is_stmts[i])



