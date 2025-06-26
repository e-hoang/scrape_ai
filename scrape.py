from bs4 import BeautifulSoup
from openai import OpenAI
from flask import Flask, render_template, request
import requests
import os

#Load the OpenAI API key from enviornment variables
api_key = os.getenv('SCRAPE_API_KEY')
if not api_key:
    raise ValueError('SCRAPE_API_KEY is not set.')

#Initialize the OpenAI client and begin a conversation in the chat log
client = OpenAI(api_key=api_key)
chat_log = [
    {'role': 'assistant', 'content': 'You are going to analyze stocks'}
]

#Initialize the Flask application
app = Flask(__name__)
@app.route("/", methods=['GET', 'POST'])

def index():
    result = None #OpenAI response to the data that is scraped
    tickers = [] #List to hold ticker symbols

    #This takes the user url input, begins an AI conversation, and scrapes the data
    if request.method == 'POST':
        url = request.form['website']
        chat_log.append({'role': 'user', 'content': url})
        completion = client.chat.completions.create(
            model='gpt-4o-mini',
            messages=chat_log
        )
        response = completion.choices[0].message.content.strip()
        chat_log.append({'role': 'assistant', 'content': response})
        result = response
        tickers = scrape(url)

    return render_template('index.html', result=result, chat_log=chat_log, tickers=tickers)

def scrape(url):
    headers = {'User-Agent' : 'Mozilla/5.0'}
    page = requests.get(url, headers=headers) 
    soup = BeautifulSoup(page.text, 'html.parser') 

    #Find the ticker symbols in the class symbol yf-1jsynna
    ticker_spans = soup.findAll('span', class_='symbol yf-1jsynna')
    tickers = []
    
    #Scrape the ticker symbols
    for ticker in ticker_spans:
        symbol = ticker.get_text(strip=True)
        if symbol:
            tickers.append(symbol)

    #This returns the list of found ticker symbols
    return tickers

if __name__ == '__main__':
    app.run(debug=True)