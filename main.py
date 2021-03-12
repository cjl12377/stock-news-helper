import requests
from twilio.rest import Client
from twilio.http.http_client import TwilioHttpClient

STOCK = "ZM"
COMPANY_NAME = "zoom"

## STEP 1: Use https://www.alphavantage.co
# When STOCK price increase/decreases by 5% between yesterday and the day before yesterday then print("Get News").

def get_stock_alert():
    STOCK_API_KEY = "04CGX6JUWY1XUSMZ"
    STOCK_ENDPOINT = "https://www.alphavantage.co/query"
    STOCK_PARAMS = {
        "function": "TIME_SERIES_DAILY",
        "symbol": STOCK,
        "apikey": STOCK_API_KEY
    }
    response = requests.get(url=STOCK_ENDPOINT, params=STOCK_PARAMS)
    response.raise_for_status()

    data = response.json()
    latest_day = list(data["Time Series (Daily)"].keys())[0]
    opening_price = float(data["Time Series (Daily)"][latest_day]["1. open"])
    closing_price = float(data["Time Series (Daily)"][latest_day]["4. close"])

    day_changes = closing_price-opening_price
    if day_changes >0:
        up_down = "🔺"
    if day_changes <0:
        up_down = "🔻"

    if (abs(day_changes)/opening_price)*100 > 5:
        get_news(day_changes, up_down)
## STEP 2: Use https://newsapi.org
# Instead of printing ("Get News"), actually get the first 3 news pieces for the COMPANY_NAME.

def get_news(day_changes, up_down):
    NEWS_API = "c65d4aa17f6349c0a24f7ed570e21365"
    NEWS_ENDPOINT = "https://newsapi.org/v2/everything"
    NEWS_PARAMS = {
        "apiKey": NEWS_API,
        "qInTitle": COMPANY_NAME,
        "pageSize": 3
    }
    response = requests.get(url=NEWS_ENDPOINT, params=NEWS_PARAMS)
    response.raise_for_status()
    articles = response.json()['articles']
    formatted_articles = [f"\n{STOCK}: {up_down}{round(abs(day_changes),2)}%\nHeadline: {article['title']}\n\nText: {article['description']}\nURL: {article['url']}" for article in articles]

    send_sms(formatted_articles)
## STEP 3: Use https://www.twilio.com
# Send a seperate message with the percentage change and each article's title and description to your phone number. 

def send_sms(formatted_articles):
    """"sends 1 message for every article. Num of articles pulled can be changed at pageSize in NEWS_PARAMS"""
    messages = formatted_articles
    TWILIO_AUTH_TOKEN = "0f53615bd31018dfde6bb939b2c37468"
    TWILIO_ACCOUNT_SID = "AC56fcef9a91c1ee6b39e4d8ad15f1e120"
    client = Client(TWILIO_ACCOUNT_SID, TWILIO_AUTH_TOKEN)
    for i in messages:
        message = client.messages.create(
            body=i,
            from_="+18329812771",
            to="+6590211777"
        )
        print(message.sid)

get_stock_alert()

#Optional: Format the SMS message like this: 
"""
TSLA: 🔺2%
Headline: Were Hedge Funds Right About Piling Into Tesla Inc. (TSLA)?. 
Brief: We at Insider Monkey have gone over 821 13F filings that hedge funds and prominent investors are required to file by the SEC The 13F filings show the funds' and investors' portfolio positions as of March 31st, near the height of the coronavirus market crash.
or
"TSLA: 🔻5%
Headline: Were Hedge Funds Right About Piling Into Tesla Inc. (TSLA)?. 
Brief: We at Insider Monkey have gone over 821 13F filings that hedge funds and prominent investors are required to file by the SEC The 13F filings show the funds' and investors' portfolio positions as of March 31st, near the height of the coronavirus market crash.
"""

