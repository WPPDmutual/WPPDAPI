from os import listdir
from os.path import isfile, join
import json
import requests as r
import datetime
import time

dels = ['BalanceSheetDate', 'ContextForDurations', 'ContextForInstants', 'CurrentFiscalYearEndDate', 'DocumentFiscalPeriodFocus', 'DocumentFiscalYearFocusContext',
'DocumentFiscalPeriodFocusContext', 'DocumentPeriodEndDate', 'DocumentType', 'EntityFilerCategory', 'EntityRegistrantName', 'IncomeStatementPeriodYTD',
'TradingSymbol', 'DocumentFiscalYearFocus', 'EntityCentralIndexKey']

current = {}

current['data'] = []
current['ticker'] = []

def prepare(ticker):
    global train, test

    f = listdir('ParsedData/' + ticker)
    if len(f) >= 4:
        data = []
        for j in range(len(f)):
            temp = json.loads(open('ParsedData/' +ticker + '/' + f[-j], 'r').read())
            for i in dels:
                del temp[i]
            for i in temp:
                data.append(temp[i])
            if j == 3:
                break;
        current['data'].append(data)
        current['ticker'].append(ticker)

for i in listdir('ParsedData'):
    try:
        prepare(i)
    except:
        continue
    print(i)

with open('current.json', 'w') as outfile:
    json.dump(current, outfile)
