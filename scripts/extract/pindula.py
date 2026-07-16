"""
------------------------------------------------------------
Project : Zimbabwe Education Master Data Platform (ZEMDP)
Module  : Pindula Extractor
Purpose : Extract secondary school data from Pindula
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
# URL
# ==========================

PINDULA_URL = (
    "https://www.pindula.co.zw/"
    "List_of_Secondary_and_High_Schools_in_Zimbabwe_and_Contact_Numbers"
)

# ==========================
# Download Page
# ==========================

def download_page(url):

    print("Downloading Pindula page...")

    session = requests.Session()

    session.headers.update({

        "User-Agent": (
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"
            " AppleWebKit/537.36 (KHTML, like Gecko)"
            " Chrome/125.0 Safari/537.36"
        ),

        "Accept": (
            "text/html,application/xhtml+xml,"
            "application/xml;q=0.9,*/*;q=0.8"
        ),

        "Accept-Language": "en-US,en;q=0.9",

        "Connection": "keep-alive"

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
# Extract Schools
# ==========================

def extract_schools(soup):

    print("Extracting schools...")

    schools = []

    table = soup.find("table")

    rows = table.find_all("tr")[1:]      # Skip header

    for row in rows:

        columns = row.find_all("td")

        if len(columns) != 3:
            continue

        # ---------------------------------
        # Contact Information
        # ---------------------------------

        contact = columns[2].get_text(" ", strip=True)

        # Remove labels
        contact = re.sub(

            r"(?i)(telephone|tel|phone|mobile|cell|fax)\s*:\s*",

            "",

            contact

        )

        # Split by commas, slashes, semicolons and new lines
        parts = re.split(

            r"[,/;\n]+",

            contact

        )

        phone_numbers = []

        email = None

        for part in parts:

            part = part.strip()

            if not part:
                continue

            # Email
            if "@" in part:

                email = part

                continue

            # Remove unwanted characters
            part = (
                part.replace("(", "")
                    .replace(")", "")
                    .replace("-", "")
                    .replace(" ", "")
                    .rstrip(",.")
                    .lstrip(",.")
            )

            if part:

                phone_numbers.append(part)

        # Remove duplicates
        phone_numbers = list(dict.fromkeys(phone_numbers))

        # ---------------------------------
        # School Record
        # ---------------------------------

        school = {

            "school_name": columns[0].get_text(strip=True),

            "province": None,

            "city": columns[1].get_text(strip=True),

            "physical_address": None,

            "school_type": None,

            "education_level": None,

            "website": None,

            "email": email,

            "phone_numbers": phone_numbers,

            "profile": None,

            "ranking_o_level": None,

            "ranking_a_level": None,

            "source": "Pindula"

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
# Run
# ==========================

def run():

    html = download_page(PINDULA_URL)

    soup = parse_page(html)

    schools = extract_schools(soup)

    return schools


# ==========================
# Main
# ==========================

if __name__ == "__main__":

    schools = run()

    save_to_json(

        schools,

        "data/raw/pindula_schools.json"

    )

    print(f"\nExtracted {len(schools)} schools.\n")

    for school in schools[:10]:

        print(school)