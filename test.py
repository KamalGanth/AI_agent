import os
from dotenv import load_dotenv
load_dotenv()
def recent_news():
    '''Useful for recent news articles'''
    import requests
    try:
        api_key = os.getenv("NEWS_API_KEY")
        url  = ('https://newsapi.org/v2/everything?'
       'q=Apple&'
       'from=2025-06-10&'
       'sortBy=popularity&'
       'apiKey={}'.format(api_key))
        response = requests.get(url)
        headlines = response
        print("Tool Trigger")
        return f"Top Headlines are {headlines}"
    except Exception as e:
        return f"recent news error: {e}"


print(recent_news())

