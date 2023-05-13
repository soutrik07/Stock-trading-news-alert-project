import requests
from twilio.rest import Client
STOCK_NAME = "TSLA"
COMPANY_NAME = "Tesla Inc"

STOCK_ENDPOINT = "https://www.alphavantage.co/query"
NEWS_ENDPOINT = "https://newsapi.org/v2/everything"
API = "e0d47b5163d74698b9b3e4b5a9769acb"
TWILIO_SID = "AC45f4f16f251a4014d8b9ba5a5a567f13"
TWILIO_TOKEN = "1f36000a773e7fdb7294f8feedd0eead"
    ## STEP 1: Use https://www.alphavantage.co/documentation/#daily
# When stock price increase/decreases by 5% between yesterday and the day before yesterday then print("Get News").
parameters = {
    "function": "TIME_SERIES_DAILY_ADJUSTED",
    "symbol": "TSLA",
    "apikey": "21BFOQ64MS2BCHXE"
}

parameters_news = {
    "apiKey": API,
    "q": COMPANY_NAME,
    "sortBy": "popularity",
    "from": "2022-11-08",
    "to": "2022-11-08"

}

#TODO 1. - Get yesterday's closing stock price. Hint: You can perform list comprehensions on Python dictionaries. e.g. [new_value for (key, value) in dictionary.items()]

response = requests.get(url=STOCK_ENDPOINT, params=parameters)
response.raise_for_status()
data_yesterday = response.json()["Time Series (Daily)"]
data_list = [value for (key, value) in data_yesterday.items()]
data_y = data_list[0]["4. close"]
print(data_y)

#TODO 2. - Get the day before yesterday's closing stock price

data_day_before_yesterday = data_list[1]["4. close"]
print(data_day_before_yesterday)

#TODO 3. - Find the positive difference between 1 and 2. e.g. 40 - 20 = -20, but the positive difference is 20. Hint: https://www.w3schools.com/python/ref_func_abs.asp

diff = float(data_day_before_yesterday) - float(data_y)
positive_diff = abs(diff)
print(positive_diff)

#TODO 4. - Work out the percentage difference in price between closing price yesterday and closing price the day before yesterday.

change_percent = (positive_diff*100)/float(data_y)
print(change_percent)

#TODO 5. - If TODO4 percentage is greater than 5 then print("Get News").


# news = response_news.json()["articles"][0]["title", "description"]
# print(news)



    ## STEP 2: https://newsapi.org/ 
    # Instead of printing ("Get News"), actually get the first 3 news pieces for the COMPANY_NAME. 

#TODO 6. - Instead of printing ("Get News"), use the News API to get articles related to the COMPANY_NAME.

if change_percent > 1:
    response_news = requests.get(url=NEWS_ENDPOINT, params=parameters_news)
    response_news.raise_for_status()
    articles = response_news.json()["articles"]
    three_articles = articles[:3]
    print(three_articles)

    #TODO 7. - Use Python slice operator to create a list that contains the first 3 articles. Hint: https://stackoverflow.com/questions/509211/understanding-slice-notation


        ## STEP 3: Use twilio.com/docs/sms/quickstart/python
        #to send a separate message with each article's title and description to your phone number.

    #TODO 8. - Create a new list of the first 3 article's headline and description using list comprehension.

    formatted_articles = [f"Headline: {article['title']}. \nBrief: {article['description']}" for article in three_articles]

    #TODO 9. - Send each article as a separate message via Twilio.
    client = Client(TWILIO_SID, TWILIO_TOKEN)
    for article in formatted_articles:
        message = client.messages.create(
            body=article,
            from_="+18563864592",
            to="+918910908717"
        )


#Optional TODO: Format the message like this: 
"""
TSLA: 🔺2%
Headline: Were Hedge Funds Right About Piling Into Tesla Inc. (TSLA)?. 
Brief: We at Insider Monkey have gone over 821 13F filings that hedge funds and prominent investors are required to file by the SEC The 13F filings show the funds' and investors' portfolio positions as of March 31st, near the height of the coronavirus market crash.
or
"TSLA: 🔻5%
Headline: Were Hedge Funds Right About Piling Into Tesla Inc. (TSLA)?. 
Brief: We at Insider Monkey have gone over 821 13F filings that hedge funds and prominent investors are required to file by the SEC The 13F filings show the funds' and investors' portfolio positions as of March 31st, near the height of the coronavirus market crash.
"""

