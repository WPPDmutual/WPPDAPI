from bs4 import BeautifulSoup
import requests
import json
import ast

ticker = 'AAPL'

html_doc = requests.get("http://sentdex.com/financial-analysis/?i="+ ticker + "&tf=all").content

soup = BeautifulSoup(html_doc, 'html.parser')

data = None

for script in soup.find_all('script'):
    try:
        if script['async'] == "":
            data = script.text
    except:
        continue

data = json.loads(data.split('=')[2].split('var')[0].replace(' ', '').replace('\n', '').replace("'", '"').replace(',visible:false},', '}'))


with open('sentiment/' + ticker + 'sentiment.json', 'w') as f:
    json.dump(data, f)

print(data)
