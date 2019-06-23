from bs4 import BeautifulSoup
from random import choice
import requests
from csv import DictReader

base_url = "http://quotes.toscrape.com"


def read_quotes(filename):
    with open(filename, 'r') as file:
        csv_reader = DictReader(file)
        return list(csv_reader)


def start_game(quotes):
    quote = choice(quotes)
    remaining_guesses = 4
    print("Here's a quote: ")
    print(quote["text"])

    guess = ''
    while guess.lower() != quote["author"].lower() and remaining_guesses > 0:
        guess = input(
            f"Who said this quote? Guesses remaining: {remaining_guesses} \n ")
        print(f"DELETE ME -- pssst..answer is: {quote['author']}")
        if guess.lower() == quote["author"].lower():
            print("YOU GUESSED IT!!")
            break
        remaining_guesses -= 1
        print_hint(quote, remaining_guesses)

    again = ''
    while again.lower() not in ('y', 'yes', 'n', 'no'):
        again = input("Would you like to play agin (y/n)?")
    if again.lower() in ('yes', 'y'):
        return start_game(quotes)
    else:
        print("ok, Thanks for playing!")


def print_hint(quote, remaining_guesses):
    if remaining_guesses == 3:
        res = requests.get(f"{base_url}{quote['bio-link']}")
        soup = BeautifulSoup(res.text, "html.parser")
        birth_date = soup.find(class_="author-born-date").get_text()
        birth_place = soup.find(class_="author-born-location").get_text()
        print(
            f"Here's a hint: The author was born on {birth_date} {birth_place}")
    elif remaining_guesses == 2:
        print(
            f"Here's a hint: The author's first name starts with: {quote['author'][0]}")
    elif remaining_guesses == 1:
        last_initial = quote['author'].split(" ")[1][0]
        print(
            f"Here's a hint: The author's last name starts with: {last_initial}")
    else:
        print(f"Sorry no guesses remaining. The answer was {quote['author']}")


quotes = read_quotes("quotes.csv")
start_game(quotes)
