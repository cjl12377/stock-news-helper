# stock-news-helper
When a chosen ticker's previous day closing price exceeds 5% (percentage constraint) of the opening price, the title of news are searched for the company name and 3 (pageSzize) articles are returned and parsed, then sent to a chat via Telegram. (Previous commits used SMS via Twilio)

## Where I hosted:
[pythonanywhere](https://www.pythonanywhere.com/) - it's limited in its features for the free tier but its simple and works


## API endpoints used:
1. Get stock data - https://www.alphavantage.co/query
2. Get news stories - https://newsapi.org/v2/everything
3. Send SMS - Twilio (careful not to burst your free credits)
4. Telegram API - https://core.telegram.org/bots/api

## Variables to edit:
To change number of articles retrieved:
- Change pageSize in NEWS_PARAMS (e.g. 3)

To change Percentage constraints of price fluctuations:
e.g. 5%
under get_stock_alert() -->  if (abs(day_changes)/opening_price)*100 > **5**:
        get_news(day_changes, up_down)

## Example:
Example-telegram-news-alert![Uploading image.png…]()

