from bs4 import BeautifulSoup
import pandas as pd
import requests
import json
import time

print("hello world")

#global_url = 'http://coinmarketcap.com/'
request = requests.get('https://coinmarketcap.com/')
soup = BeautifulSoup(request.content, 'html.parser')
#results = request.json()

print(soup.title)

print(soup.prettify())

data = soup.find('script', id="__NEXT_DATA__",type="application/json")

coins = {}

coin_data = json.loads(data.contents[0])
listings = coin_data['props']['initialState']['cryptocurrency']['listingLatest']['data']

for i in listings:
    coins[str(i['id'])] = i['slug']

for i in coins:
    page = requests.get(f'https://coinmarketcap.com/currencies/{coins[i]}/historical-data?start=20200101&end=20200630')
    soup = BeautifulSoup(page.content, 'html.parser')
    data = soup.find('script', id="__NEXT_DATA__", type = "application/json")
    historical_data = json.loads(data.contents[0])
    #quotes = historical_data['props']['initialState']['cryptocurrency']['ohlcvHistorical'][i]['quotes']
    #info =   historical_data['props']['initialState']['cryptocurrency']['ohlcvHistorical'][i]

market_cap = []
volume = []
timestamp = []
name = []
symbol = []
slug = []

for j in quotes:
    market_cap.append(j['quote']['USD']['market_cap'])
    volume.append(j['quote']['USD']['volume'])
    timestamp.append(j['quote']['USD']['timestamp'])
    name.append(info['name'])
    symbol.append(info['symbol'])
    slug.append(coins[i])

df = pd.Dataframe(columns = ['marketcap', 'volume', 'timestamp', 'name', 'symbol', 'slug'])
df['marketcap'] = market_cap
df['volume'] = volume
df['timestamp'] = timestamp
df['volume'] = volume
df['name'] = name
df['symbol'] = name
df['slug'] = slug

df.to_csv('coinapi.csv', index = False)

