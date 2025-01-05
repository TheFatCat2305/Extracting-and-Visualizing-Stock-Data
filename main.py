import yfinance as yf
import pandas as pd
import requests
from bs4 import BeautifulSoup
import plotly.graph_objects as go
from plotly.subplots import make_subplots

# Define a function to create stock and revenue graphs
def make_graph(stock_data, revenue_data, stock):
    """
    Generates a combined plot with historical stock prices and revenue data.
    Args:
    - stock_data (DataFrame): Stock price data with columns 'Date' and 'Close'.
    - revenue_data (DataFrame): Revenue data with columns 'Date' and 'Revenue'.
    - stock (str): Stock name to display as the graph title.
    """
    # Filter data to specific date ranges
    stock_data_specific = stock_data[stock_data.Date <= '2021-06-14']
    revenue_data_specific = revenue_data[revenue_data.Date <= '2021-04-30']

    # Create a subplot for share price and revenue
    fig = make_subplots(
        rows=2, cols=1, 
        shared_xaxes=True, 
        subplot_titles=("Historical Share Price", "Historical Revenue"),
        vertical_spacing=0.3
    )
    
    # Add stock price data to the first row
    fig.add_trace(
        go.Scatter(
            x=pd.to_datetime(stock_data_specific.Date), 
            y=stock_data_specific.Close.astype("float"), 
            name="Share Price"
        ), 
        row=1, col=1
    )
    
    # Add revenue data to the second row
    fig.add_trace(
        go.Scatter(
            x=pd.to_datetime(revenue_data_specific.Date), 
            y=revenue_data_specific.Revenue.astype("float"), 
            name="Revenue"
        ), 
        row=2, col=1
    )
    
    # Set axis titles
    fig.update_xaxes(title_text="Date", row=1, col=1)
    fig.update_xaxes(title_text="Date", row=2, col=1)
    fig.update_yaxes(title_text="Price ($US)", row=1, col=1)
    fig.update_yaxes(title_text="Revenue ($US Millions)", row=2, col=1)

    # Set layout properties
    fig.update_layout(
        showlegend=False,
        height=900,
        title=stock,
        xaxis_rangeslider_visible=True
    )
    
    # Show the graph
    fig.show()

# Use yfinance to extract Tesla stock data
tesla = yf.Ticker('TSLA')
tesla_data = tesla.history(period='max')
tesla_data.reset_index(inplace=True)

# Use web scraping to extract Tesla revenue data
url_tesla = 'https://cf-courses-data.s3.us.cloud-object-storage.appdomain.cloud/IBMDeveloperSkillsNetwork-PY0220EN-SkillsNetwork/labs/project/revenue.htm'
html_data_tesla = requests.get(url_tesla).text
soup_tesla = BeautifulSoup(html_data_tesla, 'html.parser')

# Parse Tesla revenue data
tesla_revenue = pd.DataFrame(columns=['Date', 'Revenue'])
rows_tesla = soup_tesla.find_all("tbody")[1].find_all('tr')
for row in rows_tesla:
    col = row.find_all("td")
    Date = col[0].text
    Revenue = col[1].text
    tesla_revenue = pd.concat(
        [tesla_revenue, pd.DataFrame({"Date": [Date], "Revenue": [Revenue]})], 
        ignore_index=True
    )

# Clean Tesla revenue data
tesla_revenue.dropna(inplace=True)
tesla_revenue = tesla_revenue[tesla_revenue['Revenue'] != ""]
tesla_revenue["Revenue"] = tesla_revenue["Revenue"].replace({"\$": "", ",": ""}, regex=True).astype(float)

# Use yfinance to extract GameStop stock data
gme = yf.Ticker('GME')
gme_data = gme.history(period='max')
gme_data.reset_index(inplace=True)

# Use web scraping to extract GameStop revenue data
url_gme = 'https://cf-courses-data.s3.us.cloud-object-storage.appdomain.cloud/IBMDeveloperSkillsNetwork-PY0220EN-SkillsNetwork/labs/project/stock.html'
html_data_gme = requests.get(url_gme).text
soup_gme = BeautifulSoup(html_data_gme, 'html.parser')

# Parse GameStop revenue data
gme_revenue = pd.DataFrame(columns=['Date', 'Revenue'])
rows_gme = soup_gme.find_all("tbody")[1].find_all('tr')
for row in rows_gme:
    col = row.find_all("td")
    Date = col[0].text
    Revenue = col[1].text
    gme_revenue = pd.concat(
        [gme_revenue, pd.DataFrame({"Date": [Date], "Revenue": [Revenue]})], 
        ignore_index=True
    )

# Clean GameStop revenue data
gme_revenue.dropna(inplace=True)
gme_revenue = gme_revenue[gme_revenue['Revenue'] != ""]
gme_revenue["Revenue"] = gme_revenue["Revenue"].replace({"\$": "", ",": ""}, regex=True).astype(float)

# Plot Tesla stock and revenue data
make_graph(tesla_data, tesla_revenue, 'Tesla')

# Plot GameStop stock and revenue data
make_graph(gme_data, gme_revenue, 'GameStop')
