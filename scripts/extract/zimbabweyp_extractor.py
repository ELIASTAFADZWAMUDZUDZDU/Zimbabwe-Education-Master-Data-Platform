"""
------------------------------------------------------------
Project : Zimbabwe Education Master Data Platform (ZEMDP)
Module  : ZimbabweYP Extractor
Purpose : Extract secondary school data from ZimbabweYP
Author  : Elias Tafadzwa Mudzudzu
------------------------------------------------------------
"""

# ==========================
# Imports
# ==========================

import requests
from bs4 import BeautifulSoup
import json

# ==========================
# Constants
# ==========================

BASE_URL = "https://www.zimbabweyp.com/category/Secondary_Schools"

# ==========================
# Download Page
# ==========================

def download_page(url):

    print("Downloading ZimbabweYP page...")

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

    companies = soup.find_all("div", class_="company")

    for company in companies:

        # ----------------------
        # School Name
        # ----------------------

        name_tag = company.find("h3")

        school_name = (
            name_tag.get_text(strip=True)
            if name_tag
            else None
        )

        # ----------------------
        # Address
        # ----------------------

        address_tag = company.find("div", class_="address")

        address = (
            address_tag.get_text(" ", strip=True)
            if address_tag
            else None
        )

        # ----------------------
        # Phone Number
        # ----------------------

        phone_numbers = []

        phone_icon = company.find("i", class_="fa-phone")

        if phone_icon:

            phone_div = phone_icon.find_parent("div")

            if phone_div:

                phone = phone_div.get_text(" ", strip=True)

                phone_numbers.append(phone)

        # ----------------------
        # Profile Link
        # ----------------------

        profile = None

        profile_button = company.find(
            "a",
            href=True
        )

        if profile_button:

            profile = (
                "https://www.zimbabweyp.com"
                + profile_button["href"]
            )

        # ----------------------
        # Create Dictionary
        # ----------------------

        school = {

            "school_name": school_name,

            "province": None,

            "city": None,

            "physical_address": address,

            "school_type": None,

            "education_level": None,

            "website": None,

            "email": None,

            "phone_numbers": phone_numbers,

            "profile": profile,
            
            "ranking_o_level":None,

            "ranking_a_level":None,

            "source": "ZimbabweYP"

        }

        schools.append(school)

    return schools

# ==========================
# Extract School Profile
# ==========================

def extract_profile(url):

    print(f"Visiting Profile: {url}")

    html = download_page(url)

    soup = parse_page(html)

    # ----------------------
    # Website
    # ----------------------

    website = None

    website_tag = soup.find("div", class_="text weblinks")

    if website_tag:

        link = website_tag.find("a")

        if link:

            website = link.get("href")

    # ----------------------
    # Description
    # ----------------------

    profile = None

    description_tag = soup.find("div", class_="text desc")

    if description_tag:

        profile = description_tag.get_text(
            " ",
            strip=True
        )

    # ----------------------
    # Address
    # ----------------------

    address = None

    address_tag = soup.find(id="company_address")

    if address_tag:

        address = address_tag.get_text(
            " ",
            strip=True
        )

    # ----------------------
    # Phone Numbers
    # ----------------------

    phone_numbers = []

    phone_sections = soup.find_all("div", class_="text phone")

    for phone in phone_sections:

        number = phone.get_text(
            " ",
            strip=True
        )

        if number:

            phone_numbers.append(number)

    # ----------------------
    # Return Updated Fields
    # ----------------------

    return {

        "website": website,

        "physical_address": address,

        "phone_numbers": phone_numbers,

        "profile": profile

    }
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

# ==========================
# Run Pipeline
# ==========================

def run():

    all_schools = []

    for page in range(1, 11):

        # ----------------------
        # Build URL
        # ----------------------

        if page == 1:

            url = BASE_URL

        else:

            url = f"{BASE_URL}/{page}"

        print(f"\nProcessing Page {page}...")

        # ----------------------
        # Download Page
        # ----------------------

        html = download_page(url)

        # ----------------------
        # Parse HTML
        # ----------------------

        soup = parse_page(html)

        # ----------------------
        # Extract Schools
        # ----------------------

        schools = extract_schools(soup)

        print(f"Extracted {len(schools)} schools from Page {page}")

        # ----------------------
        # Enrich Each School
        # ----------------------

        for school in schools:

            profile_url = school.get("profile")

            if profile_url:

                details = extract_profile(profile_url)

                school.update(details)

        # ----------------------
        # Add To Master List
        # ----------------------

        all_schools.extend(schools)

    print(f"\nTotal Schools Extracted: {len(all_schools)}")

    return all_schools

# ==========================
# Main
# ==========================

if __name__ == "__main__":

    schools = run()

    save_to_json(
        schools,
        "data/raw/zimbabweyp_schools.json"
    )

    print(f"\nExtracted {len(schools)} schools.\n")

    for school in schools[:10]:
        print(school)