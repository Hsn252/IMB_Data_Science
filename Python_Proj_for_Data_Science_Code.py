#!/usr/bin/env python
# coding: utf-8

# In[ ]:


get_ipython().system('pip install yfinance')
# !pip install pandas==1.3.3
# !pip install requests==2.26.0
get_ipython().system('pip install bs4')
# !pip install plotly==5.3.1

import yfinance as yf
import pandas as pd
import requests
from bs4 import BeautifulSoup
import plotly.graph_objects as go
from plotly.subplots import make_subplots
#!pip install pandas==1.3.3
#!pip install requests==2.26.0
get_ipython().system('pip install bs4')
get_ipython().system('pip install html5lib')
get_ipython().system('pip install lxml==4.6.4')
#!pip install plotly==5.3.1
import pandas as pd
import requests
from bs4 import BeautifulSoup

#Q1 Using yfinance to Extract Stock Data

tesla = yf.Ticker("TSLA")
tesla_data = tesla.history(period="max")
tesla_data.reset_index(inplace=True)
tesla_data.head()

#Q2 Using Webscraping to Extract Tesla Revenue Data
# Using the requests library to download the webpage https://www.macrotrends.net/stocks/charts/TSLA/tesla/revenue.
url = 'https://www.macrotrends.net/stocks/charts/TSLA/tesla/revenue'

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0;Win64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/89.0.4389.82 Safari/537.36',
    'Accept-Language': 'en-US,en;q=0.9',
    'Accept-Encoding': 'gzip, deflate, br',
    'Connection': 'keep-alive'
}

html_data = requests.get(url, headers=headers).text

# Parsing the html data using beautiful_soup.

soup = BeautifulSoup(html_data, 'html5lib')

tesla_revenue = []
for table in soup.find_all('table'):
    if ('Tesla Quarterly Revenue' in table.find('th').text):
        rows = table.find_all('tr')
        for row in rows:
            col = row.find_all('td')
            
            if col != []:
                date = col[0].text
                revenue = col[1].text.replace(',', '').replace('$', '')
                data = {"Date": date, "Revenue": revenue}
                tesla_revenue.append(data)

tesla_revenue = pd.DataFrame(tesla_revenue)
tesla_revenue = tesla_revenue[tesla_revenue['Revenue'].astype(bool)]
print(tesla_revenue.tail())

#Q3 Using yfinance to Extract Stock Data
#Using the  Ticker function we extract data on to create a object. The stock is GameStop and its ticker symbol is GME

Gamestop=yf.Ticker("GME")
gme_data=Gamestop.history(period='max')
gme_data.reset_index(inplace=True)
gme_data.head()

#Q4 using Webscraping to Extract GME Revenue Data
#Using the requests library to download the webpage https://cf-courses-data.s3.us.cloud-object-storage.appdomain.cloud/IBMDeveloperSkillsNetwork-PY0220EN-SkillsNetwork/labs/project/stock.html.

url = "https://cf-courses-data.s3.us.cloud-object-storage.appdomain.cloud/IBMDeveloperSkillsNetwork-PY0220EN-SkillsNetwork/labs/project/stock.html"

data = requests.get(url).text

soup = BeautifulSoup(data, "html5lib")

gme_revenue = pd.DataFrame(columns=['Date', 'Revenue'])
for table in soup.find_all('table'):
    if ('GameStop Quarterly Revenue' in table.find('th').text):
        rows = table.find_all('tr')
        for row in rows:
            col = row.find_all('td')
            if col != []:
                date = col[0].text
                revenue = col[1].text.replace(',',"").replace('$',"")
                gme_revenue = gme_revenue.append({"Date":date, "Revenue":revenue}, ignore_index=True)
                
                gme_revenue.tail()
                
    # Defining a Graphing Function for Q5 and Q6
    
    def make_graph(stock_data, revenue_data, stock):
    fig = make_subplots(rows=2, cols=1, shared_xaxes=True, subplot_titles=("Historical Share Price", "Historical Revenue"), vertical_spacing = .3)
    stock_data_specific = stock_data[stock_data.Date <= '2021--06-14']
    revenue_data_specific = revenue_data[revenue_data.Date <= '2021-04-30']
    fig.add_trace(go.Scatter(x=pd.to_datetime(stock_data_specific.Date, infer_datetime_format=True), y=stock_data_specific.Close.astype("float"), name="Share Price"), row=1, col=1)
    fig.add_trace(go.Scatter(x=pd.to_datetime(revenue_data_specific.Date, infer_datetime_format=True), y=revenue_data_specific.Revenue.astype("float"), name="Revenue"), row=2, col=1)
    fig.update_xaxes(title_text="Date", row=1, col=1)
    fig.update_xaxes(title_text="Date", row=2, col=1)
    fig.update_yaxes(title_text="Price ($US)", row=1, col=1)
    fig.update_yaxes(title_text="Revenue ($US Millions)", row=2, col=1)
    fig.update_layout(showlegend=False,
    height=900,
    title=stock,
    xaxis_rangeslider_visible=True)
    fig.show()
    
    # Q5 Plotting Tesla Stock Graph
    
    make_graph(tesla_data, tesla_revenue, 'Tesla')
    
    #Q6 Plotting GameStop Stock Graph
    
    make_graph(gme_data, gme_revenue, 'GameStop')
    
    
    # End 

