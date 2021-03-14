import requests
from twilio.rest import Client
from twilio.http.http_client import TwilioHttpClient
import os

STOCK = "ZM"
COMPANY_NAME = "zoom"
TWILIO_AUTH_TOKEN = os.environ.get("TWILIO_AUTH_TOKEN")
TWILIO_ACCOUNT_SID = os.environ.get("TWILIO_ACCOUNT_SID")
STOCK_API_KEY = os.environ.get("STOCK_API_KEY")
NEWS_API = os.environ.get("NEWS_API")
TELE_API_KEY = os.environ.get("TELE_API_KEY")
CHAT_ID = os.environ.get("CHAT_ID")



def get_stock_alert():
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

    if (abs(day_changes)/opening_price)*100 > 1.0:
        get_news(day_changes, up_down)


def get_news(day_changes, up_down):
    NEWS_ENDPOINT = "https://newsapi.org/v2/everything"
    NEWS_PARAMS = {
        "apiKey": NEWS_API,
        "qInTitle": COMPANY_NAME,
        "pageSize": 3
    }
    response = requests.get(url=NEWS_ENDPOINT, params=NEWS_PARAMS)
    response.raise_for_status()
    articles = response.json()['articles']
    formatted_articles = [f"\n{STOCK}: {up_down}{round(abs(day_changes),2)}% \n\nHeadline: {article['title']}\n\nText: {article['description']}\nURL: {article['url']}" for article in articles]

    send_telegram(formatted_articles=formatted_articles)

# def send_sms(formatted_articles):
#     """"sends 1 message for every article. Num of articles pulled can be changed at pageSize in NEWS_PARAMS"""
#     messages = formatted_articles
#     proxy_client = TwilioHttpClient()
#     proxy_client.session.proxies = {'https': os.environ['https_proxy']}
#
#     client = Client(TWILIO_ACCOUNT_SID, TWILIO_AUTH_TOKEN, http_client=proxy_client)
#
#     for i in messages:
#         message = client.messages.create(
#             body=i,
#             from_="+18329812771",
#             to="+6590211777"
#         )
#         print(message.sid)


def send_telegram(formatted_articles):
    """"sends 1 message for every article. Num of articles pulled can be changed at pageSize in NEWS_PARAMS"""
    messages = formatted_articles

    telegram_endpoint = f"https://api.telegram.org/bot{TELE_API_KEY}/sendMessage"
    for i in messages:
        params = {
            "chat_id": CHAT_ID,
            "text": i
        }
        response = requests.post(params=params, url=telegram_endpoint)
        response.raise_for_status()


get_stock_alert()
