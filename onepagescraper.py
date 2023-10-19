from flask import Flask, jsonify
import time
import requests
import trafilatura
from bs4 import BeautifulSoup

app = Flask(__name__)


def scrape_article_content(article_url):
    try:
        r = requests.get(article_url)
        r.raise_for_status()

        # Extract the main content of the article using Trafilatura
        downloaded = trafilatura.fetch_url(article_url)
        content = trafilatura.extract(downloaded)

        return content

    except Exception as e:
        return {'error': str(e)}


def clean_text(text):
    if isinstance(text, str):  # Check if the input is a string
        # Replace characters with empty strings
        new_text = text.replace('\u2019', '')
        return new_text.replace('\n', '')
    else:
        return text  # Return the input unchanged if it's not a string


def scrape_blog_pages(base_url, max_pages):
    scraped_data = []

    try:
        # Modify the URL to include pagination parameter
        url = f'{base_url}'

        headers = {
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 14_0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/117.0.0.0 Safari/537.36'
        }

        r = requests.get(url, headers=headers)
        r.raise_for_status()

        soup = BeautifulSoup(r.content, 'lxml')
        articles = soup.find_all('div', class_='accordion-item')

        for article in articles:
            title = clean_text(article.find(
                'div', class_='blog_post_title').text)

            # Get the URL of the article
            article_url = article.find(
                'a', class_='blog_index_featureimg')['href']

            # Scrape the content of the article using Trafilatura
            article_content = scrape_article_content(article_url)

            # Clean the content to remove newline characters and \\u
            cleaned_content = clean_text(article_content)

            scraped_data.append({
                'title': title,
                'content': cleaned_content
            })

    except Exception as e:
        return {'error': str(e)}

    return scraped_data


@app.route('/', methods=['GET'])
def get_scraped_data():
    try:
        base_url = 'https://reducewaste.sccgov.org/accepted-materials-list'
        max_pages = 1  # Define the maximum number of pages to scrape

        scraped_data = scrape_blog_pages(base_url, max_pages)

        return jsonify(scraped_data)

    except Exception as e:
        return {'error': str(e)}


if __name__ == '__main__':
    app.run(debug=True, port=8001)
