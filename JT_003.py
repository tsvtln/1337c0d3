import requests
from bs4 import BeautifulSoup
import json
import hashlib
import os

# URL for the ASEAN Wikipedia page.
URL = 'https://en.wikipedia.org/wiki/ASEAN'
OUTPUT_FILE = 'countries_data.json'


def fetch_content(url: str) -> BeautifulSoup:
    # fetch the content from the url and return a beautifulsoup object
    response = requests.get(url)
    response.raise_for_status()  # Raise an error if the request fails.
    return BeautifulSoup(response.content, 'html.parser')


def find_urban_areas_table(soup: BeautifulSoup) -> BeautifulSoup:
    # we find the h3 Urban areas (seen with f12 inspector), grep the table element and returns it
    header = soup.find(lambda tag: tag.name == "h3" and "Urban areas" in tag.get_text())
    if header:
        table = header.find_next("table")
        return table


def parse_table(table: BeautifulSoup) -> dict:
    """
    Parses the Urban areas table and returns a dictionary in the following structure:

    {
        "Country1": {
            "cities": [
                {
                    "core_city": <city_name>,
                    "population": <population>,
                    "area": <area>,
                    "density": <population density (population/area) rounded to 2 decimals>
                },
                ...
            ],
            "total_population": <sum of all cities' populations>,
            "total_area": <sum of all cities' areas>,
            "density": <overall density (total_population/total_area) rounded to 2 decimals>
        },
        ...
    }

    The function identifies the column indexes for:
      - Country
      - Core city
      - Population
      - Area

    It then extracts and cleans the data from each row, calculates the density for each metropolitan area,
    and groups them under their respective country.
    """
    countries_dictionary = {}

    # get all rows from the table
    rows = table.find_all("tr")
    # get the header cells from the first row
    header = [cell.get_text(strip=True) for cell in rows[0].find_all(["th", "td"])]


    idx_country = next(i for i, h in enumerate(header) if "Country" in h)
    idx_core_city = next(i for i, h in enumerate(header) if "Core city" in h or "City" in h)
    idx_population = next(i for i, h in enumerate(header) if "Population" in h)
    idx_area = next(i for i, h in enumerate(header) if "Area" in h)


    # we go through each data row and skip header row
    for row in rows[1:]:
        # include both table header and table data in each row
        cells = row.find_all(["th", "td"])
        if len(cells) < max(idx_country, idx_core_city, idx_population, idx_area) + 1:
            continue  # skip rows that don't have enough cells

        country = cells[idx_country].get_text(strip=True)
        core_city = cells[idx_core_city].get_text(strip=True)

        # clear population text by removing commas and any notes (split by "[")
        pop_text = cells[idx_population].get_text(strip=True).split("[")[0].replace(",", "")
        try:
            population = int(pop_text)
        except ValueError:
            continue

        # clear the area text by removing commas and any notes (split by "[")
        area_text = cells[idx_area].get_text(strip=True).split("[")[0].replace(",", "")
        try:
            area = float(area_text)
        except ValueError:
            continue

        # calculate population density for the metropolitan area
        density = population / area if area > 0 else None

        city_data = {
            "core_city": core_city,
            "population": population,
            "area": area,
            "density": round(density, 2) if density is not None else None
        }

        if country not in countries_dictionary:
            countries_dictionary[country] = {"cities": []}
        countries_dictionary[country]["cities"].append(city_data)

    # for every country calculate the overall density
    for country, data in countries_dictionary.items():
        total_population = sum(city["population"] for city in data["cities"])
        total_area = sum(city["area"] for city in data["cities"])
        overall_density = total_population / total_area if total_area > 0 else None
        data["total_population"] = total_population
        data["total_area"] = total_area
        data["density"] = round(overall_density, 2) if overall_density is not None else None

    return countries_dictionary


def generate_hash(data: dict) -> str:
    # this is for generating an md5sum so we can compare easier
    data_str = json.dumps(data, sort_keys=True)
    return hashlib.md5(data_str.encode()).hexdigest()


def load_previous_data(filename: str) -> dict:
    # open the 'db' file
    if not os.path.exists(filename):
        return {}
    try:
        with open(filename, 'r') as f:
            return json.load(f)
    except json.JSONDecodeError:
        return {}


def save_data(filename: str, data: dict) -> None:
    # to save the collected data in json format to the 'db'
    with open(filename, 'w') as f:
        json.dump(data, f, indent=4)


def main():
    soup = fetch_content(URL)
    table = find_urban_areas_table(soup)

    # parse the table to build the countries dictionary
    countries_dictionary = parse_table(table)

    # pretty-print the dictionary
    print(json.dumps(countries_dictionary, indent=4))

    # load previously saved data
    previous_data = load_previous_data(OUTPUT_FILE)

    # compare the new data with previous data using md5sum
    new_hash = generate_hash(countries_dictionary)
    old_hash = generate_hash(previous_data)

    # save the new data only if it is different from the old one
    if new_hash != old_hash:
        save_data(OUTPUT_FILE, countries_dictionary)
        print("Data updated and saved.")
    else:
        print("No changes detected. File not updated.")


if __name__ == '__main__':
    main()
