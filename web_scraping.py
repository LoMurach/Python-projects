# Web scraping is downloadign large amounts of data in a short period of time
# https://www.youtube.com/watch?time_continue=105&v=Kz1b8YNeruE&feature=emb_logo

import requests
from bs4 import BeautifulSoup
import pandas as pd

l = []
base_url = "https://www.century21global.com/for-sale-residential/Japan?pageNo="
for page in range(1, 878, 1):
    print(base_url + str(page))
    r = requests.get(base_url + str(page))
    c = r.content
    soup = BeautifulSoup(c, "html.parser")
    all = soup.find_all("a", {"class" : "search-result-info"})
    for item in all:
        d = {}

        try:
            d['City'] = item.find("span", {"class" : "search-result-label"}).text.replace("\r", "")

        except:
            pass

        try:
            d['Area'] = item.find("div", {"class" : "size"}).text.replace("\r", "").replace("\n", "").replace("m2", "").replace("sq. ft.", "")
        except:
            pass

        try:
            d['Price USD'] = item.find("div", {"class" : "search-result-label-secondary price-user"}).text.replace("$", "").replace("USD", "")
        except:
            pass

        try:
            d['Price JPY'] = item.find("div", {"class" : "search-result-label-primary price-native"}).text.replace("¥", "").replace("JPY", "")
        except:
            pass

        l.append(d)

df = pd.DataFrame(l)
df
# Split column City into 3  columns
df[['In Japan', 'City','Country']] = df.City.str.split(",",expand=True,)

# Split column Area into 2 columns
df[['Area feet', 'Area kv meters']] = df.Area.str.split("-",expand=True,)

# Drop Na, column In Japan and column Area
df.dropna(inplace=True)
df.drop(columns=['In Japan'], inplace=True)
df.drop(columns=['Area'], inplace=True)

# Re-order columns
df = df[['Country', 'City', 'Area feet', 'Area kv meters', 'Price JPY', 'Price USD']]
df

grp = df['Country'].groupby(df['City']).agg({'Country' : 'count'}).sort_values(by='Country',ascending=False)
print(grp)
