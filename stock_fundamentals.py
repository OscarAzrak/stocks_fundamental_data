import yahoo_fin.stock_info as si
import re
import csv
import json
from io import StringIO
from bs4 import BeautifulSoup
import requests
import pandas as pd
import yfinance as yf
import datetime as dt
import matplotlib.pyplot as plt
from financial_statements import *
pd.set_option('display.max_column',None)
pd.set_option('display.max_rows',None)

import yahoofinancials

def get_stock(ticker):
    stock = yf.Ticker(ticker)

    return stock

def get_dividend_history(stock):
    dividends = stock.dividends
    dividends = dividends.to_frame()
    dividends = dividends.groupby([(dividends.index.year)]).sum()
    dividends.iloc[-1]['Dividends'] = stock.info['dividendRate']

    return dividends


def make_list(dividends):
    dividendlist = list(dividends['Dividends'])
    divindex = dividends.index.to_list()
    return dividendlist, divindex

def get_consecutive_years(divindex):
    years = 0
    for a in range(0, len(divindex)):
        try:
            if divindex[a] + 1 == divindex[a + 1]:
                years += 1
            else:
                years = 0
        except:
            pass
    return years

def get_consecutive_dividends(dividendlist, years):
    dividendlist = dividendlist[-years-1:]
    divyears = 0
    for i in range(0, len(dividendlist) - 1):
        try:
            if dividendlist[i] >= dividendlist[i - 1]:
                divyears += 1
        except:
            pass
    return divyears

def get_div_cagr(dividendlist, divyears):
    currentdiv = dividendlist[-1]
    if divyears >= 10:
        div10yearsago = dividendlist[-11]
        cagrlong = ((currentdiv/div10yearsago)**(1/10)) - 1
    else:
        divstart = dividendlist[-divyears-2]
        cagrlong = ((currentdiv/divstart)**(1/divyears)) - 1
    div5years = dividendlist[-6]
    cagr5 = ((currentdiv/div5years)**(1/5)) - 1

    return cagr5, cagrlong

def get_yoc(stock, dividendlist, cagr, period=5):
    price = stock.info['previousClose']
    currdiv = dividendlist[-1]
    yoc = (currdiv*(1 + cagr)**period)/price
    return yoc


def get_financial_statements(url):

    df = scrape_table(url)
    return df

def get_net_income(df):
    is_df = df.iloc[1:]

    net_income = is_df['Net Income Common Stockholders']
    return net_income

def get_revenue(df):
    is_df = df.iloc[1:]

    revenue = is_df['Total Revenue']
    return revenue

def get_total_debt(df):
    total_debt = df['Total Debt']
    return total_debt

def get_net_debt(df):
    net_debt = df['Net Debt']
    return net_debt

def get_shares(df):
    shares = df['Share Issued']
    return shares

def get_cash(df):
    cf_df = df.iloc[1:]
    cash_flow = cf_df['Free Cash Flow']
    return cash_flow

def main():
    symbol = 'AAPL'
    bs_url = 'https://finance.yahoo.com/quote/' + symbol + '/balance-sheet?p=' + symbol
    is_url = 'https://finance.yahoo.com/quote/' + symbol + '/financials?p=' + symbol
    cf_url = 'https://finance.yahoo.com/quote/' + symbol + '/cash-flow?p=' + symbol

    stock = get_stock(symbol)
    print(stock.ticker)
    print('-'*15)
    dividends = get_dividend_history(stock)
    dividendlist, dividendindex = make_list(dividends)
    years = get_consecutive_years(dividendindex)
    dividendyears = get_consecutive_dividends(dividendlist, years)
    cagr5, cagrlong = get_div_cagr(dividendlist, dividendyears)
    yoc5_5 = get_yoc(stock, dividendlist, cagr5, period=5)
    yoc10_5 = get_yoc(stock, dividendlist, cagrlong, period=5)
    yoc5_10 = get_yoc(stock, dividendlist, cagr5, period=10)
    yoc10_10 = get_yoc(stock, dividendlist, cagrlong, period=10)
    yoc5_15 = get_yoc(stock, dividendlist, cagr5, period=15)
    yoc10_15 = get_yoc(stock, dividendlist, cagrlong, period=15)
    yoc5_20 = get_yoc(stock, dividendlist, cagr5, period=20)
    yoc10_20 = get_yoc(stock, dividendlist, cagrlong, period=20)


    print(stock.ticker, 'has raised dividends for:', dividendyears, 'years with a cagr of', cagrlong*100,'% since the past 10 years')
    print('-'*75)
    print('Your Yield On Cost in 5 years calculating with 5 years cagr:',yoc5_5*100, '%')
    print('Your Yield On Cost in 5 years calculating with 10 years cagr:',yoc10_5*100, '%')
    print('Your Yield On Cost in 10 years calculating with 5 years cagr:',yoc5_10*100, '%')
    print('Your Yield On Cost in 10 years calculating with 10 years cagr:',yoc10_10*100, '%')
    print('Your Yield On Cost in 15 years calculating with 5 years cagr:',yoc5_15*100, '%')
    print('Your Yield On Cost in 15 years calculating with 10 years cagr:',yoc10_15*100, '%')
    print('Your Yield On Cost in 20 years calculating with 5 years cagr:',yoc5_20*100, '%')
    print('Your Yield On Cost in 20 years calculating with 10 years cagr:',yoc10_20*100, '%')


    is_df = get_financial_statements(is_url)
    bs_df = get_financial_statements(bs_url)
    cf_df = get_financial_statements(cf_url)

    net_income = get_net_income(is_df)
    print(stock.ticker, 'net income for the past 4 years is:', net_income)
    revenue = get_revenue(is_df)
    print('with a revenue of ', revenue)
    total_debt = get_total_debt(bs_df)
    net_debt = get_net_debt(bs_df)
    print('the total debt is:', total_debt)
    print('and a net debt of', net_debt)

    shares = get_shares(bs_df)
    print('the amount of shares over the past 4 years are:', shares)
    cash = get_cash(cf_df)
    print(stock.ticker, 'cash is:',cash)







if __name__ == '__main__':
    main()










"""is_df = si.get_income_statement('aapl')
bs_df = si.get_balance_sheet('AAPL')
cf_df = si.get_cash_flow(symbol)

#data from income statement
netIncome = is_df.loc['netIncome'].to_list()
revenue = is_df.loc['totalRevenue'].to_list()


print(bs_df)
#data from balance sheet
cash = bs_df.loc['cash'].to_list()"""


"""plt.style.use('classic')
fig, axs = plt.subplots(sharex=True, figsize=(13, 9))

axs.bar(dividends['Dividends'], alpha=0.8)

plt.show()"""

