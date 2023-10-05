from flask import Flask, jsonify, request
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

@app.route('/', methods=['GET'])
def get_scraped_data():
    try:
        url = 'https://www.sustainablesv.org/sl-blog/?swcfpc=1'
        headers = {
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 14_0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/117.0.0.0 Safari/537.36'
        }

        r = requests.get(url, headers=headers)
        r.raise_for_status()

        soup = BeautifulSoup(r.content, 'lxml')
        articles = soup.find_all('article', class_='elementor-post')

        scraped_data = []
        for article in articles:
            title = article.find('h3', class_='elementor-post__title').text
            author = article.find('span', class_='elementor-post-author').text

            # Get the URL of the article
            article_url = article.find('a', class_='btn-read-more')['href']

            # Scrape the content of the article using Trafilatura
            article_content = scrape_article_content(article_url)

            scraped_data.append({
                'title': title,
                'author': author,
                'content': article_content
            })

        return jsonify(scraped_data)

    except Exception as e:
        return {'error': str(e)}

if __name__ == '__main__':
    app.run(debug=True, port=8001)