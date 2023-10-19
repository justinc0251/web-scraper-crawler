from trafilatura import fetch_url, extract
import json

def scrape_website(url):
    # Fetch the HTML content from the URL
    html = fetch_url(url)

    # Extract text content using Trafilatura
    extracted_text = extract(html)

    return extracted_text

if __name__ == "__main__":
    website_url = "https://www.wasteconnections.com/arizona/disposal-recycle-guide/"

    extracted_text = scrape_website(website_url)

    # Convert the extracted text to a JSON structure
    data = {'text_content': extracted_text}

    # Save the data as JSON
    with open("extracted_content.json", "w") as json_file:
        json.dump(data, json_file, indent=4)
