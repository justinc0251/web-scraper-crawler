import pandas as pd
from tqdm import tqdm
from trafilatura.sitemaps import sitemap_search
from trafilatura import fetch_url, extract
import time
import json


def get_urls_from_sitemap(resource_url: str) -> list:
    """
    Get a list of urls from a sitemap with trafilatura
    """
    urls = sitemap_search(resource_url)
    return urls


def extract_article(url: str) -> dict:
    """
    Extract article from a url
    """
    downloaded = fetch_url(url)
    article = extract(downloaded, favor_precision=True)
    return {
        'url': url,
        'article': article
    }


def create_dataset(list_of_websites: list) -> list:
    """
    Create a list of dictionaries with data from blog posts
    """
    data = []
    for website in list_of_websites:
        urls = get_urls_from_sitemap(website)
        for url in urls:
            data.append(extract_article(url))
            time.sleep(0.5)
    return data


if __name__ == "__main__":
    # Define your data sources here (list_of_websites)
    list_of_websites = [
        "https://www.scu.edu/sustainability/operations/waste/"
        # Add more blog URLs as needed
    ]

    data_list = create_dataset(list_of_websites)

    # Save the data as JSON
    with open("dataset.json", "w") as json_file:
        json.dump(data_list, json_file, indent=4)
