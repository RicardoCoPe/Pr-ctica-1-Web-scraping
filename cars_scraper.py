# Import libraries
from bs4 import BeautifulSoup
import requests
import re
import pandas as pd


def scraping():
    names = []
    locations = []
    years = []
    combustibles = []
    kilometers = []
    transmissions = []
    powers = []
    prices = []
    financed_prices = []
    dealers = []
    dealer_ratings = []

    # Data from 20 pages
    for i in range(1, 21):
        # Store website in a variable
        url = 'https://www.autocasion.com/coches-ocasion?page=' + str(i)

        # Request to website
        headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) ' +
                                 'AppleWebKit/537.36 (KHTML, like Gecko) ' +
                                 'Chrome/94.0.4606.81 Safari/537.36'}
        page = requests.get(url, headers=headers)

        # HTTP code returned by the server
        # page.status_code

        # Raw content of the server response
        # page.content

        # Soup object
        soup = BeautifulSoup(page.content, 'html.parser')

        # Show the nested structure
        # print(soup.prettify())

        # Store results in a variable (16 cars entries per page)
        results = soup.find_all('article', {'class': 'anuncio'})

        # Target necessary data
        for result in results:
            # Names
            try:
                names.append(result.find('h2').get_text().strip())
            except IndexError:
                names.append('n/a')

            # Locations
            try:
                locations.append(result.find('ul').find_all('li')[0].get_text().
                                 replace('Provincia: ', ''))
            except IndexError:
                locations.append('n/a')

            # Years
            try:
                years.append(result.find('ul').find_all('li')[1].get_text().
                             replace('Matriculación: ', ''))
            except IndexError:
                years.append('n/a')

            # Combustibles
            try:
                combustibles.append(result.find('ul').find_all('li')[2].get_text().
                                    replace('Combustible: ', ''))
            except IndexError:
                combustibles.append('n/a')

            # Kilometers
            try:
                kilometers.append(result.find('ul').find_all('li')[3].get_text())
            except IndexError:
                kilometers.append('n/a')

            # Transmissions
            try:
                transmissions.append(result.find('ul').find_all('li')[4].
                                     get_text().replace('Cambio: ', ''))
            except IndexError:
                transmissions.append('n/a')

            # Powers
            try:
                powers.append(result.find('ul').find_all('li')[5].get_text())
            except IndexError:
                powers.append('n/a')

            # Prices
            try:
                prices.append(result.find('p', {'class': 'precio'}).get_text().
                              strip())
            except IndexError:
                prices.append('n/a')

            # Financed_prices
            try:
                financed_prices.append(result.find(
                    'span', {'class': 'financiacion'}).get_text())
            except AttributeError:
                financed_prices.append('Sin financiación')

            # Dealers
            try:
                dealers.append(result.find('p', {'class': 'titulo'}).get_text())
            except AttributeError:
                dealers.append('n/a')

            # Dealer_ratings
            try:
                dealer_ratings.append(result.find('div', {'class': 'valoracion'}).
                                      get_text())
            except AttributeError:
                dealer_ratings.append('n/a')

        # From kilometers data, select the number of kilometers
        for i, kilometer in enumerate(kilometers):
            try:
                kilometers[i] = re.findall('[0-9.]+', kilometer)[0]
            except IndexError:
                kilometers[i] = 'n/a'

        # From power data, select the number of CV
        for i, power in enumerate(powers):
            try:
                powers[i] = re.findall('[0-9]+', power)[0]
            except IndexError:
                powers[i] = 'n/a'

        # From price data, select the number of €
        for i, price in enumerate(prices):
            try:
                prices[i] = re.findall('[0-9.]+', price)[0]
            except IndexError:
                prices[i] = 'n/a'

        # From dealer rating data, select the number of rating
        for i, dealer_rating in enumerate(dealer_ratings):
            try:
                dealer_ratings[i] = re.findall('([0-9],\d{1})', dealer_rating)[0]
            except IndexError:
                dealer_ratings[i] = 'n/a'

    # Dictionary with scraped data
    cars_dict = {'Name': names, 'Location': locations, 'Year': years,
                 'Combustible': combustibles, 'Kilometers': kilometers,
                 'Transmission': transmissions, 'Power [CV]': powers,
                 'Price [€]': prices, 'Financed Price': financed_prices,
                 'Dealer': dealers, 'Dealer Rating (over 5)': dealer_ratings}

    # Dataframe with scraped data
    cars_df = pd.DataFrame.from_dict(cars_dict)

    return cars_df
