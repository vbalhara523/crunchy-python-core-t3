import requests
from bs4 import BeautifulSoup
import json
import time
import logging
from urllib.parse import urljoin

logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s", handlers=[logging.FileHandler("run.log"), logging.StreamHandler()])

def fetch_page(url, retries=3):
    headers = {"User-Agent": "Mozilla/5.0 (Student Project Bot; crunchy-python-core)"}
    delay = 2
    for attempt in range(retries):
        try:
            response = requests.get(url, headers=headers, timeout=10)
            if response.status_code == 429:
                logging.warning("Rate limited (429). Backing off for %s seconds.", delay)
                time.sleep(delay)
                delay *= 2
                continue
            response.raise_for_status()
            return response.text
        except requests.exceptions.RequestException as e:
            logging.warning("Attempt %s failed: %s", attempt + 1, e)
            time.sleep(delay)
            delay *= 2
    logging.error("Failed to fetch %s", url)
    return None

def parse_books(html):
    soup = BeautifulSoup(html, "html.parser")
    books = []
    for article in soup.find_all("article", class_="product_pod"):
        try:
            title_element = article.h3.a
            title = title_element["title"] if title_element else "Unknown Title"
            price_element = article.find("p", class_="price_color")
            price = price_element.text.strip() if price_element else "Unknown Price"
            stock_element = article.find("p", class_="instock availability")
            stock = stock_element.text.strip() if stock_element else "Unknown Stock"
            books.append({"title": title, "price": price, "stock": stock})
        except Exception as e:
            logging.error("Error parsing book: %s", e)
    next_button = soup.find("li", class_="next")
    next_url = next_button.a["href"] if next_button and next_button.a else None
    return books, next_url

def main():
    base_url = "http://books.toscrape.com/catalogue/category/books_1/"
    current_url = "index.html"
    all_books = []
    target_count = 100
    logging.info("Starting scraper targeting %s records", target_count)
    while current_url and len(all_books) < target_count:
        full_url = urljoin(base_url, current_url)
        html = fetch_page(full_url)
        if not html: break
        books, next_url = parse_books(html)
        all_books.extend(books)
        current_url = next_url
        time.sleep(1.5)
    all_books = all_books[:target_count]
    with open("books_data.json", "w", encoding="utf-8") as f:
        json.dump(all_books, f, indent=4)
    logging.info("Exported %s records to books_data.json", len(all_books))

if __name__ == "__main__":
    main()
