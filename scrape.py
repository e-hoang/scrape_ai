from bs4 import BeautifulSoup
from openai import OpenAI
from flask import Flask, render_template, request
import requests
import os

api_key = os.getenv('SCRAPE_API_KEY')
if not api_key:
    raise ValueError('SCRAPET_API_KEY is not set.')

client = OpenAI(api_key=api_key)

app = Flask(__name__)
@app.route("/", methods=['GET', 'POST'])

def index():
    result = None
    url = 'https://finance.yahoo.com/markets/'
    headers = {'User-Agent' : 'Mozilla/5.0'}
    page = requests.get(url, headers=headers) 
    soup = BeautifulSoup(page.text, 'html.parser')

    ticker_spans = soup.findAll('span', class_='symbol yf-1jsynna')
    
    for ticker in ticker_spans:
        symbol = ticker.get_text(strip=True)
        if symbol:
            print(symbol)

if __name__ == '__main__':
    app.run(debug=True)