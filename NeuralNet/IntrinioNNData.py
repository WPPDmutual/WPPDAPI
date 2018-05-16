import json
import requests
import csv
import pandas as pd


tags = json.loads(open("tags.json", "r").read())

tickers = json.loads(open("tickers.json", "r").read())

headers = None

with open('test.csv', 'r' ) as theFile:
    reader = csv.reader(theFile)
    headers = next(reader)


for ticker in tickers:
    
    train = [None]*(len(headers) -1)
    test = [None]*(len(headers) -1)
    current = [None]*(len(headers) -2)

    train.insert(0, ticker)
    test.insert(0, ticker)
    current.insert(0, ticker)

    print(ticker)

    for tag in tags:

        companydata = json.loads(requests.get("https://aaf0c9c2800c05440f2fd22d44bafe05:e1c6a9f01d60ceb7016f60cdd48c668a@api.intrinio.com/historical_data?identifier="
        + ticker + "&item=" + tag + "&frequency=quarterly").content)

        try:
            if companydata['errors'] != None:
                continue
        except:
            if tag == "close_price"  and companydata["result_count"] < 12:
                break


            for n in range(len(companydata['data'])):
                quarter = ((n) % 4) + 1

                if n < 4:
                    current[headers.index(tag + " Q" + str(quarter))] = companydata['data'][n]["value"]
                if 3 < n < 8:
                    test[headers.index(tag + " Q" + str(quarter))] = companydata['data'][n]["value"]
                if 7 < n < 12:
                    train[headers.index(tag + " Q" + str(quarter))] = companydata['data'][n]["value"]
                if n > 11:
                    break
    else:

        testgrowth = int(current[headers.index("close_price Q4")])/int(current[headers.index("close_price Q1")])
        traingrowth = int(test[headers.index("close_price Q4")])/int(test[headers.index("close_price Q1")])

        test[headers.index("growth")] = testgrowth
        train[headers.index("growth")] = traingrowth

        print("done")

        with open('test.csv', 'a') as f:
            writer = csv.writer(f)
            writer.writerow(test)

        with open('train.csv', 'a') as f:
            writer = csv.writer(f)
            writer.writerow(train)

        with open('current.csv', 'a') as f:
            writer = csv.writer(f)
            writer.writerow(current)

    continue
