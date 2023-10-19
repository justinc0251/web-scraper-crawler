from flask import Flask, jsonify, request
import requests
import trafilatura
from bs4 import BeautifulSoup
import time

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

    for page_number in range(1, max_pages + 1):
        try:
            # Modify the URL to include pagination parameter
            url = f'{base_url}{page_number}'

            headers = {
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36'
            }

            r = requests.get(url, headers=headers)
            r.raise_for_status()

            soup = BeautifulSoup(r.content, 'lxml')
            articles = soup.find_all('article', class_='row')

            for article in articles:

                title = clean_text(article.find(
                    'h3').text)

                # Get the URL of the article
                article_url = article.find('a')['href']

                # Scrape the content of the article using Trafilatura
                article_content = scrape_article_content(f'{article_url}'
                                                         )

                # Clean the content to remove newline characters and \\u
                cleaned_content = clean_text(article_content)

                scraped_data.append({
                    'title': title,
                    'content': cleaned_content
                })

                time.sleep(0.5)

        except Exception as e:
            return {'error': str(e)}

    return scraped_data


@app.route('/', methods=['GET'])
def get_scraped_data():
    try:
        base_url = 'https://www.uswonline.com/blog/'
        max_pages = 1  # Define the maximum number of pages to scrape

        scraped_data = scrape_blog_pages(base_url, max_pages)

        return jsonify(scraped_data)

    except Exception as e:
        return {'error': str(e)}


if __name__ == '__main__':
    app.run(debug=True, port=8001)
