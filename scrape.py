from bs4 import BeautifulSoup
import requests

def main():
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
    main()