import requests
import re
import time
import json

from bs4 import BeautifulSoup
from urllib.parse import urljoin
from pydantic import BaseModel, HttpUrl


BASE_URL = "https://books.toscrape.com/"
REQUEST_DELAY = 1.0


class Book(BaseModel):
    title: str
    price: float
    availability: str
    stock_count: int
    description: str | None
    category: str | None
    upc: str | None
    product_type: str | None
    price_excl_tax: float | None
    price_incl_tax: float | None
    tax: float | None
    number_of_reviews: int
    rating: int | None
    url: HttpUrl


def fetch_page(url: str) -> str:
    response = requests.get(
        url,
        timeout=10,
        headers={
            "User-Agent": "FlyRank-Polite-Scraper/1.0"
        }
    )

    response.raise_for_status()
    response.encoding = "utf-8"

    return response.text


def extract_book_links(html: str, page_url: str) -> list[str]:
    soup = BeautifulSoup(html, "html.parser")

    links = []

    for link in soup.select("article.product_pod h3 a"):
        href = link.get("href")

        if href:
            absolute_url = urljoin(page_url, href)
            links.append(absolute_url)

    return links


def extract_book(html: str, url: str) -> dict:
    soup = BeautifulSoup(html, "html.parser")

    title_element = soup.select_one("div.product_main h1")
    title = (
        title_element.get_text(strip=True)
        if title_element
        else None
    )

    price_element = soup.select_one(
        "div.product_main p.price_color"
    )
    price = (
        price_element.get_text(strip=True)
        if price_element
        else None
    )

    availability_element = soup.select_one(
        "div.product_main p.instock.availability"
    )
    availability = (
        availability_element.get_text(" ", strip=True)
        if availability_element
        else None
    )

    description_element = soup.select_one(
        "#product_description + p"
    )
    description = (
        description_element.get_text(" ", strip=True)
        if description_element
        else None
    )

    breadcrumb = soup.select("ul.breadcrumb li a")

    category = None

    if len(breadcrumb) >= 3:
        category = breadcrumb[2].get_text(strip=True)

    product_info = {}

    for row in soup.select("table.table.table-striped tr"):
        key_element = row.select_one("th")
        value_element = row.select_one("td")

        if key_element and value_element:
            key = key_element.get_text(strip=True)
            value = value_element.get_text(strip=True)
            product_info[key] = value

    rating_element = soup.select_one("p.star-rating")

    rating = None

    if rating_element:
        rating_classes = rating_element.get("class", [])

        rating_names = {
            "One": 1,
            "Two": 2,
            "Three": 3,
            "Four": 4,
            "Five": 5,
        }

        for rating_name, rating_value in rating_names.items():
            if rating_name in rating_classes:
                rating = rating_value
                break

    return {
        "title": title,
        "price": price,
        "availability": availability,
        "description": description,
        "category": category,
        "upc": product_info.get("UPC"),
        "product_type": product_info.get("Product Type"),
        "price_excl_tax": product_info.get("Price (excl. tax)"),
        "price_incl_tax": product_info.get("Price (incl. tax)"),
        "tax": product_info.get("Tax"),
        "number_of_reviews": product_info.get("Number of reviews"),
        "rating": rating,
        "url": url,
    }


def normalize_price(price: str | None) -> float | None:
    if not price:
        return None

    cleaned = price.replace("£", "").strip()

    try:
        return float(cleaned)
    except ValueError:
        return None


def normalize_stock(availability: str | None) -> int:
    if not availability:
        return 0

    match = re.search(
        r"\((\d+)\s+available\)",
        availability
    )

    if match:
        return int(match.group(1))

    return 0


def normalize_reviews(reviews: str | None) -> int:
    if not reviews:
        return 0

    try:
        return int(reviews)
    except ValueError:
        return 0


def normalize_book(book: dict) -> dict:
    return {
        "title": book["title"],
        "price": normalize_price(book["price"]),
        "availability": book["availability"],
        "stock_count": normalize_stock(
            book["availability"]
        ),
        "description": book["description"],
        "category": book["category"],
        "upc": book["upc"],
        "product_type": book["product_type"],
        "price_excl_tax": normalize_price(
            book["price_excl_tax"]
        ),
        "price_incl_tax": normalize_price(
            book["price_incl_tax"]
        ),
        "tax": normalize_price(
            book["tax"]
        ),
        "number_of_reviews": normalize_reviews(
            book["number_of_reviews"]
        ),
        "rating": book["rating"],
        "url": book["url"],
    }


def scrape_book(url: str) -> Book:
    html = fetch_page(url)

    raw_book = extract_book(
        html,
        url
    )

    normalized_book = normalize_book(
        raw_book
    )

    return Book(**normalized_book)


def get_catalogue_links() -> list[str]:

    catalogue_pages = [
        BASE_URL,
        urljoin(
            BASE_URL,
            "catalogue/page-2.html"
        ),
        urljoin(
            BASE_URL,
            "catalogue/page-3.html"
        ),
    ]

    all_links = []

    for page_url in catalogue_pages:

        print(
            f"Fetching catalogue: {page_url}"
        )

        try:
            html = fetch_page(page_url)

            links = extract_book_links(
                html,
                page_url
            )

            print(
                f"Found {len(links)} books"
            )

            all_links.extend(links)

        except Exception as error:

            print(
                f"Catalogue failed: {error}"
            )

        time.sleep(REQUEST_DELAY)

    return all_links


if __name__ == "__main__":

    start_time = time.time()

    print("=" * 60)
    print("FLYRANK POLITE SCRAPER")
    print("=" * 60)

    # --------------------------------
    # 1. Discover book URLs
    # --------------------------------

    book_links = get_catalogue_links()

    total_urls = len(book_links)

    print()
    print(f"Total book URLs discovered: {total_urls}")
    print()

    # --------------------------------
    # 2. Scrape books
    # --------------------------------

    books = []
    failures = []

    for index, book_url in enumerate(
        book_links,
        start=1
    ):

        print(
            f"[{index}/{total_urls}] "
            f"Scraping..."
        )

        try:

            book = scrape_book(
                book_url
            )

            books.append(
                book.model_dump(
                    mode="json"
                )
            )

            print(
                f"✓ {book.title}"
            )

        except Exception as error:

            print(
                f"✗ Failed: {book_url}"
            )

            print(
                f"  Error: {error}"
            )

            failures.append(
                {
                    "url": book_url,
                    "error": str(error)
                }
            )

        time.sleep(
            REQUEST_DELAY
        )

    # --------------------------------
    # 3. Save books
    # --------------------------------

    with open(
        "output/books.json",
        "w",
        encoding="utf-8"
    ) as file:

        json.dump(
            books,
            file,
            indent=2,
            ensure_ascii=False
        )

    # --------------------------------
    # 4. Save failures
    # --------------------------------

    with open(
        "output/failures.json",
        "w",
        encoding="utf-8"
    ) as file:

        json.dump(
            failures,
            file,
            indent=2,
            ensure_ascii=False
        )

    # --------------------------------
    # 5. Generate report
    # --------------------------------

    end_time = time.time()

    elapsed_time = end_time - start_time

    successful = len(books)
    failed = len(failures)

    if total_urls > 0:
        success_rate = (
            successful / total_urls
        ) * 100
    else:
        success_rate = 0

    report = {
        "total_urls_discovered": total_urls,
        "successful": successful,
        "failed": failed,
        "success_rate_percent": round(
            success_rate,
            2
        ),
        "elapsed_seconds": round(
            elapsed_time,
            2
        ),
        "request_delay_seconds": REQUEST_DELAY,
    }

    with open(
        "output/report.json",
        "w",
        encoding="utf-8"
    ) as file:

        json.dump(
            report,
            file,
            indent=2
        )

    # --------------------------------
    # 6. Final report
    # --------------------------------

    print()
    print("=" * 60)
    print("SCRAPING COMPLETE")
    print("=" * 60)

    print(
        f"URLs discovered : {total_urls}"
    )

    print(
        f"Successful       : {successful}"
    )

    print(
        f"Failed           : {failed}"
    )

    print(
        f"Success rate     : {success_rate:.2f}%"
    )

    print(
        f"Time taken       : {elapsed_time:.2f} seconds"
    )

    print()
    print("Output files:")
    print("  output/books.json")
    print("  output/failures.json")
    print("  output/report.json")

    print("=" * 60)