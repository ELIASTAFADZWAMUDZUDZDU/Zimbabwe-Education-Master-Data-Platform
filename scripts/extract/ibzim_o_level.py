"""
------------------------------------------------------------
Project : Zimbabwe Education Master Data Platform (ZEMDP)
Module  : IBZIM Extractor
Purpose : Extract O-Level school rankings from IBZIM
Author  : Elias Tafadzwa Mudzudzu
------------------------------------------------------------
"""

# ==========================
# Imports
# ==========================

import requests
from bs4 import BeautifulSoup
import json
import re

# ==========================
# Constants
# ==========================

URL = "https://www.ibzim.com/education/rankings/top-100-best-o-level-schools-in-zimbabwe"

# ==========================
# Download Page
# ==========================

def download_page(url):

    print("Downloading IBZIM page...")

    session = requests.Session()

    session.headers.update({

        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36",

        "Accept-Language": "en-US,en;q=0.9"

    })

    response = session.get(url, timeout=30)

    response.raise_for_status()

    return response.text


# ==========================
# Parse HTML
# ==========================

def parse_page(html):

    print("Parsing HTML...")

    return BeautifulSoup(html, "html.parser")


# ==========================
# Extract Rankings
# ==========================

def extract_rankings(soup):

    print("Extracting schools...")

    schools = []

    rows = soup.find_all("tr")

    for row in rows:

        columns = row.find_all("td")

        if len(columns) < 5:
            continue

        # ----------------------
        # Ranking
        # ----------------------

        ranking = None

        ranking_text = columns[0].contents[0].strip()

        match = re.search(r"\d+", ranking_text)

        if match:
            ranking = int(match.group())

        # ----------------------
        # School Name
        # ----------------------

        link = columns[0].find("a")

        school_name = (
            link.get_text(strip=True)
            if link
            else None
        )

        # ----------------------
        # City
        # ----------------------

        city = columns[3].get_text(strip=True)

        # ----------------------
        # School Type
        # ----------------------

        school_type = columns[4].get_text(strip=True)

        # ----------------------
        # Create Dictionary
        # ----------------------

        school = {

            "school_name": school_name,

            "province": None,

            "city": city,

            "physical_address": None,

            "school_type": school_type,

            "education_level": "O-Level",

            "website": None,

            "email": None,

            "phone_numbers": [],

            "profile": None,

            "ranking_o_level": ranking,

            "ranking_a_level":None,

            "source": "IBZIM"

        }

        schools.append(school)

    return schools


# ==========================
# Save JSON
# ==========================

def save_to_json(data, filename):

    with open(filename, "w", encoding="utf-8") as file:

        json.dump(
            data,
            file,
            indent=4,
            ensure_ascii=False
        )

    print(f"Saved {len(data)} records to {filename}")


# ==========================
# Run Pipeline
# ==========================

def run():

    html = download_page(URL)

    soup = parse_page(html)

    schools = extract_rankings(soup)

    print(f"\nExtracted {len(schools)} schools.")

    return schools


# ==========================
# Main
# ==========================

if __name__ == "__main__":

    schools = run()

    save_to_json(
        schools,
        "data/raw/ibzim_o_level_rankings.json"
    )

    print()

    for school in schools[:10]:

        print(school)