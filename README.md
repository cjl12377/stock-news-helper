# stock-news-helper
Sends top news on a company when their ticker's previous day closing price exceeds a certain percentage constraint


## API endpoints used:
Get stock data - https://www.alphavantage.co/query
Get news stories - https://newsapi.org/v2/everything
Send SMS - Twilio (watch not to burst your free credits)


To change number of articles retrieved:
- Change pageSize in NEWS_PARAMS

To change Percentage constraints of price fluctuations:
e.g. 5%
under get_stock_alert() -->  if (abs(day_changes)/opening_price)*100 > **5**:
        get_news(day_changes, up_down)
