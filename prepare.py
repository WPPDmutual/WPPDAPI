from os import listdir
from os.path import isfile, join
import json
import requests as r
import datetime
import time

dels = ['BalanceSheetDate', 'ContextForDurations', 'ContextForInstants', 'CurrentFiscalYearEndDate', 'DocumentFiscalPeriodFocus', 'DocumentFiscalYearFocusContext',
'DocumentFiscalPeriodFocusContext', 'DocumentPeriodEndDate', 'DocumentType', 'EntityFilerCategory', 'EntityRegistrantName', 'IncomeStatementPeriodYTD',
'TradingSymbol', 'DocumentFiscalYearFocus', 'EntityCentralIndexKey']

train = {}
test = {}

train['growth'] = []
test['growth'] = []
train['data'] = []
test['data'] = []
train['ticker'] = []
test['ticker'] = []

def prepare(ticker):
    global train, test
    files = []

    f = listdir('ParsedData/' + ticker)
    if len(f) >= 12:
        for i in range(len(f)):
            data = []
            temp = json.loads(open('ParsedData/' +ticker + '/' + f[-(i+4)], 'r').read())
            for i in dels:
                del temp[i]
            for i in temp:
                data.append(temp[i])
            files.append(data)
            if len(files) == 8:
                break;
        train['data'].append(files[0] + files[1] + files[2] + files[3])
        test['data'].append(files[4] + files[5] + files[6] + files[7])

        trainchange, testchange = getchange(ticker)

        train['growth'].append(trainchange)
        test['growth'].append(testchange)

        train['ticker'].append(ticker)
        test['ticker'].append(ticker)

def getchange(ticker):
    f = listdir('ParsedData/' + ticker)
    if len(f) >= 12:
        dates = []
        nndates = {}
        for i in range(len(f)):
            date = f[-(i+4)].split('-')[1].split('.')[0]
            if datetime.datetime(*time.strptime("20160924", "%Y%m%d")[:6]).weekday() < 5:
                dates.append(date)
            else:
                dates.append(str(int(date) - 2))

            if len(dates) == 8:
                nndates['train'] = dates[4:]
                nndates['test'] = dates[0:4]
                break

        # data = json.loads(r.get('https://1900acbb6cd718c7f397d32cf6aa6b65:8396a4bb6dee40df2b83c93333a9d8ff@api.intrinio.com/historical_data?identifier='+
        # ticker + '&start_date=' + nndates['train'][-1] + '&end_date=' + str(int(nndates['test'][-1]) + 10000) + '&item=close_price&page_size=10000').text)['data']

        data = json.loads(r.get('https://1900acbb6cd718c7f397d32cf6aa6b65:8396a4bb6dee40df2b83c93333a9d8ff@api.intrinio.com/historical_data?identifier='+
        ticker + '&start_date=' + '2015-12-31' + '&end_date=' + '2017-12-31' + '&item=close_price&page_size=10000').text)['data']

        print(nndates)

        testchange = data[0]['value']/data[252]['value']
        trainchange = data[252]['value']/data[-1]['value']

        print(data[0]['value'])
        print(data[0]['date'])
        print(data[252]['value'])
        print(data[252]['date'])
        print(data[-1]['value'])
        print(data[-1]['date'])
        print(trainchange)
        print(testchange)
        print(ticker)

        return trainchange,testchange


for i in listdir('ParsedData'):
    try:
        prepare(i)
    except:
        continue
    print(i)

with open('train.json', 'w') as outfile:
    json.dump(train, outfile)
with open('test.json', 'w') as outfile:
    json.dump(test, outfile)
