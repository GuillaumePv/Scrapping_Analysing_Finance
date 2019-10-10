#importation des packages pour avoir graphes & tableaux
import pandas as pd
from matplotlib import pyplot as plt
import pandas_datareader.data as web
import datetime as dt
from matplotlib import style

style.use('ggplot')

#initialisation du début des dates & fin de cotations
start = dt.datetime(2000,1,1)
end = dt.datetime(2018,12,31)

#recherche des données sur yahoo finance -> construction dataFrame
df = web.DataReader('TSLA','yahoo',start,end)
print(df.head())


## Handling Data and Graphing ##

#mettre le dataFrame sous forme csv
df.to_csv('tsla.csv')

# possible de lire tous type de données (sql,excel,csv...) avec pandas (voir docu)
# read csv mais problem with index with csv 
df = pd.read_csv('tsla.csv')
print(df.head())

# bonne version
df = pd.read_csv('tsla.csv', parse_dates=True, index_col=0)
print(df.head())

## Vizualisation ##
#plot simple#

# ici problème car volume prend tout (valeur la + grande)
df.plot()
plt.show()

# choisir la colonne que l'on souhaite prendre
df['Adj Close'].plot()
plt.show()

#mettre plusieurs colonnes sur le graphes
df[['High','Close']].plot()
plt.show()

# creaton d'une nouvelle colonne (ici : 100 moving average)
df['100ma']=df['Adj Close'].rolling(window=100).mean()

#creation de fenetre pour mettre différents graphes dans une seule feuille (sharex => zoom sur grand graphe zomm aussi en bas)
grph1 = plt.subplot2grid((6,1),(0,0), rowspan=5, colspan=1)
grph2 = plt.subplot2grid((6,1),(5,0), rowspan=1, colspan=1, sharex=grph1)

grph1.plot(df.index,df['Adj Close'])
grph1.plot(df.index,df['100ma'])
grph2.bar(df.index,df['Volume'])

plt.show()
## création de bougie japonaises (à revoir) ##
# resample -> mettre les datas dans une autre unité (mois -> 10min) -> utile pour les stocks

#ohlc (open high low close
df_ohlc = df['Adj Close'].resample('10D').ohlc()

#Volume -> réféchir à comment agréger les donner => sum a bcp plus de sens que mean
df_volume = df['Volume'].resample('10D').sum()

# importer le module de boygies japonaises

from mpl_finance import candlestick_ohlc
import matplotlib.dates as mdates

# attention problème avec l'index des datas pour former bougies japonaises

df_ohlc.reset_index(inplace=True)

#convertir date en chiffre pour pouvoir faire graphe
df_ohlc['Date']=df_ohlc['Date'].map(mdates.date2num)

# graphe de bougies japonaises
grph1.xaxis_date()
candlestick_ohlc(grph1, df_ohlc.values, width=2, colorup='g')
grph2.fill_between(df_volume.index.map(mdates.date2num), df_volume.values, 0)
plt.show()

df_ohlc = df['Adj Close'].resample('10D').ohlc()
df_volume = df['Volume'].resample('10D').sum()

#vrai code pour avoir bougie japonaises
df_ohlc.reset_index(inplace=True)
df_ohlc['Date'] = df_ohlc['Date'].map(mdates.date2num)

ax1 = plt.subplot2grid((6,1), (0,0), rowspan=5, colspan=1)
ax2 = plt.subplot2grid((6,1), (5,0), rowspan=1, colspan=1, sharex=ax1)
ax1.xaxis_date()

candlestick_ohlc(ax1, df_ohlc.values, width=5, colorup='g')
ax2.fill_between(df_volume.index.map(mdates.date2num), df_volume.values, 0)
plt.show()

################################
## Automating getting S&P 500 ##
################################

# web-scapping -> beautiful soup (bs)

import bs4 as bs

# save all object in python
import pickle

#recupérer code source
import bs4 as bs

# save all object in python
import pickle

#recupérer code source
import requests

# spécifier date pour pandas
import datetime as dt

# create a new directory
import os 

import pandas as pd
import pandas_datareader.data as web

def save_sp500_tickers():
    resp = requests.get('https://en.wikipedia.org/wiki/List_of_S%26P_500_companies')
    # bien mettre .text et pas .txt
    soup = bs.BeautifulSoup(resp.text)
    # demander à soup ce qu'il faut trouver
    table = soup.find('table', {'class':'wikitable sortable'})
    tickers = []
    for row in table.findAll('tr')[1:]:
        ticker = row.findAll('td')[0].text
        tickers.append(ticker)
    
    with open('s&p500tickers.pickle','wb') as f:
        pickle.dump(tickers,f)
    
    print(tickers)
        
    return tickers

#save_sp500_tickers()

#obtenir data price de yahoo -> problème pour scapper data (yahoo)

def get_data_from_yahoo(reload_sp500=False):
    if reload_sp500:
        tickers = save_sp500_tickers()
    else:
        with open('s&p500tickers.pickle','rb') as f:
            tickers = pickle.load(f)
    
    if not os.path.exists('stock_dfs'):
        # creation d'un répertoire de travail
        os.makedirs('stock_dfs')
    
    start = dt.datetime(2000,1,1)
    end = dt.datetime(2016,12,31)
   # possible de faire 'tickers[:w]' pour choisir le nombre de valeur que l'on veut où quel valeur comme la const de graphe 
    for ticker in tickers:
        #savoir ticker qui on déjà été fait
        print(ticker)
        if not os.path.exists('stock_dfs/{}.csv'.format(ticker)):
            df = web.DataReader(ticker, 'yahoo', start, end)
            df.reset_index(inplace=True)
            df.set_index("Date", inplace=True)
            df = df.drop("Symbol", axis=1)
            df.to_csv('stock_dfs/{}.csv'.format(ticker))
        else:
            print('Already have {}'.format(ticker))
            
get_data_from_yahoo()

#####################
### Bonne Version ###
####################
!pip install yahoo_fin
from yahoo_fin import stock_info as si
import pandas as pd
from matplotlib import pyplot as plt
import pandas_datareader.data as web
import datetime as dt
from matplotlib import style

def save_sp500_tickers():
    resp = requests.get('http://en.wikipedia.org/wiki/List_of_S%26P_500_companies')
    soup = bs.BeautifulSoup(resp.text, 'lxml')
    table = soup.find('table', {'class': 'wikitable sortable'})
    tickers = []
    
    for row in table.findAll('tr')[1:]:
        ticker = row.findAll('td')[1].text
        tickers.append(ticker)
    with open("sp500tickers.pickle","wb") as f:
        pickle.dump(tickers,f)

    return tickers
  
save_sp500_tickers()

def get_data_from_yahoo(reload_sp500=False):
    if reload_sp500:
        tickers = save_sp500_tickers()
    else:
        with open("sp500tickers.pickle", "rb") as f:
            tickers = pickle.load(f)
            
    if not os.path.exists('stock_dfs'):
        os.makedirs('stock_dfs')
        
    start = dt.datetime(2015, 1, 1)
    end = dt.datetime.now()
    
    for ticker in tickers[:30]:
    # just in case your connection breaks, we'd like to save our progress!
        if not os.path.exists('stock_dfs/{}.csv'.format(ticker)):
            df = si.get_data(ticker, start, end)
            df.reset_index(inplace=True)
            df.to_csv('stock_dfs/{}.csv'.format(ticker))
        else:
            print('Already have {}'.format(ticker))
        
get_data_from_yahoo()

def compile_data():
    with open("sp500tickers.pickle", "rb") as f:
        tickers = pickle.load(f)

    main_df = pd.DataFrame()

    for count, ticker in enumerate(tickers[:30]):
        df = pd.read_csv('stock_dfs/{}.csv'.format(ticker))
        df.set_index('date', inplace=True)
        df.drop(['open','high','low','close','volume'],1,inplace=True)
        if main_df.empty:
            main_df = df
        else:
            main_df = main_df.merge(df, how='outer')

        if count % 10 == 0:
            print(count)
    print(main_df.head())
    main_df.to_csv('sp500_joined_closes.csv')


compile_data()