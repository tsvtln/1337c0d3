"""
requirements:
beautifulsoup4==4.12.3
certifi==2024.8.30
charset-normalizer==3.3.2
idna==3.8
requests==2.32.3
soupsieve==2.6
urllib3==2.2.3
"""

import requests
from bs4 import BeautifulSoup
import json
import hashlib


def fetch_data():
    url = 'https://en.wikipedia.org/wiki/List_of_European_Union_member_states_by_population'
    response = requests.get(url)
    soup = BeautifulSoup(response.content, 'html.parser')

    table = soup.find('table', {'class': 'wikitable'})
    rows = table.find_all('tr')[1:]

    countries_dictionary = {}
    for row in rows:
        cells = row.find_all('td')
        if len(cells) < 2:
            continue
        country = cells[0].get_text(strip=True)
        population = cells[1].get_text(strip=True).replace(',', '')
        try:
            population = int(population)
        except ValueError:
            continue

        countries_dictionary[country] = {'country_population': population}

    return countries_dictionary


def calculate_percentages(countries_dictionary):
    total_population = sum(entry['country_population'] for entry in countries_dictionary.values())
    for country, data in countries_dictionary.items():
        data['country_population_percentage'] = format((data['country_population'] / total_population) * 100, '.1f')


def load_previous_data(filename):
    try:
        with open(filename, 'r') as file:
            return json.load(file)
    except (FileNotFoundError, json.JSONDecodeError):
        return {}


def save_data(filename, data):
    with open(filename, 'w') as file: json.dump(data, file, indent=4)


def generate_hash(data):
    data_str = json.dumps(data, sort_keys=True)
    return hashlib.md5(data_str.encode()).hexdigest()


def main():
    filename = 'countries_population.json'  # db file

    """
     We get the new data and compare the md5 of the old data with the new one. If it's different than there's changes
     and we save them to the db file. 
    """
    new_data = fetch_data()
    calculate_percentages(new_data)
    previous_data = load_previous_data(filename)

    if generate_hash(new_data) != generate_hash(previous_data):
        save_data(filename, new_data)
        print("Data updated and saved.")
    else:
        print("No changes detected. Data not updated.")

    print(json.dumps(new_data, indent=4))


if __name__ == '__main__':
    main()
