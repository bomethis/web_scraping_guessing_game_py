from bs4 import BeautifulSoup
import requests

all_quotes = []
res = requests.get(f"http://quotes.toscrape.com")
soup = BeautifulSoup(res.text, "html.parser")
quotes = soup.find_all(call_="quote")
for quote in quotes:
    all_quotes.append({
        "text": quote.find(class_="text").get_text(),
        "auther": quote.find(class_="auther").get_text(),
        "bio-link": quote.find(class_="a")["href"]
        })

print(all_quotes)
