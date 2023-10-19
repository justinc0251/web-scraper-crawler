import json
from trafilatura import fetch_url, extract
from bs4 import BeautifulSoup

# Fetch the HTML content of the webpage
url = "https://reducewaste.sccgov.org/accepted-materials-list"
html = fetch_url(url)

# Parse the HTML content using BeautifulSoup
soup = BeautifulSoup(html, "html.parser")

# Extract dropdown titles and information
dropdown_data = []

# Replace these selectors with the actual selectors for your dropdowns
dropdown_title_selector = ".coh-style-tab"
dropdown_info_selector = ".coh-accordion-tabs-content"

# Find and extract the dropdown data
titles = soup.select(dropdown_title_selector)
info = soup.select(dropdown_info_selector)

# Ensure that the number of titles and info matches
for title, info in zip(titles, info):
    dropdown_data.append({
        "title": title.get_text(),
        "information": info.get_text()
    })

# Save the extracted data as JSON
with open("dropdown_data.json", "w") as json_file:
    json.dump(dropdown_data, json_file, indent=4)
