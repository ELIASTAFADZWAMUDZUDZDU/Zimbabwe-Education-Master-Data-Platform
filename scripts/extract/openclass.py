"""
------------------------------------------------------------
Project : Zimbabwe Education Master Data Platform (ZEMDP)
Module  : OpenClass Extractor
Purpose : Extract secondary school data from OpenClass Zimbabwe
Author  : Elias Tafadzwa Mudzudzu
------------------------------------------------------------
"""

import requests
from bs4 import BeautifulSoup
import json

url= "https://openclass.co.zw/contact-details-of-secondary-high-schools-in-zim/"


def download_page(url):

    print("Downloading OPENCLASS page...")

    session = requests.Session()

    session.headers.update({
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36",
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
        "Accept-Language": "en-US,en;q=0.9",
        "Connection": "keep-alive"
    })

    response = session.get(url, timeout=30)

    response.raise_for_status()

    return response.text

def parse_page(html):

    print("Parsing HTML...")

    return BeautifulSoup(html, "html.parser")

def extract_schools(soup):

    print("Extracting schools...")

    schools = []

    tables = soup.find_all("table")

    for table in tables:

        rows = table.find_all("tr")[1:]      # Skip header

        for row in rows:

            columns = row.find_all("td")

            if len(columns) != 3:
                continue

            school = {

                "school_name": columns[0].get_text(strip=True),

                "province": None,

                "city": columns[1].get_text(strip=True),

                "physical_address": None,

                "school_type": None,

                "education_level": None,

                "website": None,

                "email": None,

                "phone_numbers": [
                    columns[2].get_text(strip=True)
                ],

                "profile": None,

                "ranking_o_level":None,
            
                "ranking_a_level":None,

                "source": "OpenClass"

            }

            schools.append(school)

    return schools

def save_to_json(data, filename):
    """
    Save extracted data to a JSON file.
    """

    with open(filename, "w", encoding="utf-8") as file:
        json.dump(data, file, indent=4, ensure_ascii=False)

    print(f"Saved {len(data)} records to {filename}")    

def run():

    html = download_page(url)

    soup = parse_page(html)

    schools = extract_schools(soup)

    return schools

if __name__ == "__main__":

    schools = run()

    save_to_json(
    schools,
    "data/raw/openclass_schools.json"
    )

    print(f"\nExtracted {len(schools)} schools.\n")

    for school in schools[:10]:
        print(school)