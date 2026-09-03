Polite Book Scraper

A Python web scraper built for the FlyRank AI Backend Engineering Internship – Week 5 Assignment A9.

The scraper downloads three catalogue pages from **Books to Scrape**, discovers all 60 book pages, extracts structured book information, normalizes and validates the data with Pydantic, handles failures without stopping the entire process, and produces an honest scraping report.

Features

* Scrapes 3 catalogue pages
* Discovers all 60 book URLs
* Visits each book page
* Extracts structured book information
* Normalizes prices, stock counts, and review counts
* Validates scraped data using Pydantic
* Uses UTF-8 encoding for correct text handling
* Handles individual page failures gracefully
* Uses a 1-second delay between requests
* Uses a custom User-Agent
* Saves clean JSON output
* Generates a final scraping report

Tech Stack

* Python 3.10+
* Requests
* BeautifulSoup4
* Pydantic

## Project Structure

```text
scraper/
├── src/
│   └── main.py
├── output/
│   ├── books.json
│   ├── failures.json
│   └── report.json
├── cache/
├── .gitignore
├── README.md
└── requirements.txt
```

Installation

Create and activate a virtual environment:

```powershell
python -m venv venv
.\venv\Scripts\Activate.ps1
```

Install the dependencies:

```powershell
pip install -r requirements.txt
```

 Run the Scraper

From the `scraper` directory:

```powershell
python src\main.py
```

The scraper will:

1. Fetch the three catalogue pages.
2. Discover the book URLs.
3. Visit each book page.
4. Extract and normalize the data.
5. Validate each book with Pydantic.
6. Record any failed URLs.
7. Save the results.
8. Generate a final report.

Output

`output/books.json`

Contains the successfully scraped and validated books.

Each book includes fields such as:

* Title
* Price
* Availability
* Stock count
* Description
* Category
* UPC
* Product type
* Price excluding tax
* Price including tax
* Tax
* Number of reviews
* Rating
* URL

`output/failures.json`

Contains URLs that could not be successfully scraped or validated.

For the completed run, no failures were recorded.

`output/report.json`

Contains the final scraping statistics.

Example:

```json
{
  "total_urls_discovered": 60,
  "successful": 60,
  "failed": 0,
  "success_rate_percent": 100.0,
  "elapsed_seconds": 152.39,
  "request_delay_seconds": 1.0
}
```

Polite Scraping

The scraper is designed to make requests responsibly:

* Requests use a timeout.
* A descriptive User-Agent is provided.
* A 1-second delay is used between requests.
* Individual failures do not crash the entire scraper.
* The scraper reports failures honestly instead of silently ignoring them.

Final Result

The completed run successfully processed all 60 discovered book pages:

* **URLs discovered:** 60
* **Successful:** 60
* **Failed:** 0
* **Success rate:** 100%
* **Request delay:** 1 second
* **Total runtime:** 152.39 seconds
