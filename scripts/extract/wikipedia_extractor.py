"""
------------------------------------------------------------
Project : Zimbabwe Education Master Data Platform (ZEMDP)
Module  : Wikipedia Extractor
Purpose : Extract secondary school data from Wikipedia
Author  : Elias Tafadzwa Mudzudzu
------------------------------------------------------------
"""
import requests
from bs4 import BeautifulSoup
import json

WIKIPEDIA_URL = "https://en.wikipedia.org/wiki/List_of_schools_in_Zimbabwe"

def download_page(url: str) -> str:
    """
    Download HTML from Wikipedia.
    """

    headers = {
        "User-Agent": (
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
            "AppleWebKit/537.36 (KHTML, like Gecko) "
            "Chrome/138.0.0.0 Safari/537.36"
        )
    }

    response = requests.get(
        url,
        headers=headers,
        timeout=30
    )

    response.raise_for_status()

    return response.text

def parse_page(html: str) -> BeautifulSoup:
    """
    Parse HTML into a BeautifulSoup object.
    """

    return BeautifulSoup(html, "lxml")

def extract_schools(soup: BeautifulSoup) -> list[dict]:
    """
    Extract schools from Wikipedia grouped by province.
    """

    schools = []

    # Find all province sections
    sections = soup.find_all("section")

    for section in sections:

        # Find the province heading
        h2 = section.find("h2")

        if not h2:
            continue

        province = h2.get_text(strip=True)

        # Skip non-province sections
        if province in ["Contents", "See also", "References"]:
            continue

        # Find the school list
        ul = section.find("ul")

        if not ul:
            continue

        # Extract each school
        for li in ul.find_all("li", recursive=False):

            school = {
                "school_name": li.get_text(" ", strip=True),
                "province": province,
                "city": None,
                "physical_address": None,
                "school_type": None,
                "education_level": None,
                "website": None,
                "email": None,
                "phone_numbers": [],
                "profile": None,
                "ranking_o_level":None,
                "ranking_a_level":None,
                "source": "Wikipedia"
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

    print("Downloading Wikipedia page...")

    html = download_page(WIKIPEDIA_URL)

    print("Parsing HTML...")

    soup = parse_page(html)

    print("Extracting schools...")

    schools = extract_schools(soup)

    print(f"Extracted {len(schools)} schools.")

    return schools

if __name__ == "__main__":

    schools = run()

    save_to_json(
        schools,
        "data/raw/wikipedia_schools.json"
    )

    print(f"\nExtracted {len(schools)} schools.\n")

    for school in schools[:5]:
        print(school)

