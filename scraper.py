import requests
from bs4 import BeautifulSoup
import time
from urllib.parse import urlparse, urljoin
import json
import urllib.robotparser
from datetime import datetime, timezone
import logging

logging.basicConfig(
    level = logging.INFO,
    format = "%(asctime)s %(levelname)s %(message)s",
)

logger = logging.getLogger(__name__)

try:
    from sources_local import SOURCES
except ImportError:
    from source import SOURCES

USER_AGENT = "friendlyscraper/1.0 (+https://github.com/camronibra/friendlyscraper)"
HEADERS = {"User-Agent": USER_AGENT}
DEFAULT_DELAY = 2
robot_parsers = {}

def main():
    for source in SOURCES:
        with open(f"{source.name}.jsonl", "w", encoding="utf-8") as file:
            scraped_text = scrape(source)
            for url, text in scraped_text:
                fetched_at = datetime.now(timezone.utc).isoformat()
                record = {"url": url, "text": text, "source": source.name, "fetched_at": fetched_at}
                file.write(json.dumps(record, ensure_ascii=False) + "\n")

def scrape(source):
    article_urls = collect_article_urls(source)

    for article_url in article_urls:
        article_html = fetch_page(article_url)

        if article_html:
            text = extract_article_text(article_html, source)

            if text:
                yield(article_url, text)

def get_robot_parser(url):
    parsed = urlparse(url)
    root = f"{parsed.scheme}://{parsed.netloc}"

    if root not in robot_parsers:
        parser = urllib.robotparser.RobotFileParser()
        try:
            response = requests.get(root + "/robots.txt", headers=HEADERS, timeout=15)
            if response.status_code == 200:
                parser.parse(response.text.splitlines())
                parser.modified()
            elif response.status_code in (401, 403) or response.status_code >= 500:
                parser.disallow_all = True
            else:
                parser.allow_all = True
        except requests.RequestException:
            parser.disallow_all = True
        robot_parsers[root] = parser

    return(robot_parsers[root])

def fetch_page(url):
    parser = get_robot_parser(url)
    delay = parser.crawl_delay(USER_AGENT) 
    
    if not parser.can_fetch(USER_AGENT, url):
        print(f"Skipped (disallowed by robots.txt): {url}")
        return None
    else:
        try: 
            time.sleep(max(delay or 0, DEFAULT_DELAY))
            response = requests.get(url, headers=HEADERS, timeout=15)
            response.raise_for_status()
            return response.text
        except requests.RequestException as e:
            print(f"Could not fetch {url}: {e}")
            return None

def extract_article_text(html, source):
    soup = BeautifulSoup(html, "html.parser")
    content = soup.select_one(source.content_selector)

    if content is None:
        return(None)

    return content.get_text(" ", strip=True)

def collect_article_urls(source):
    urls = []

    for category_url in source.category_urls:
        category_html = fetch_page(category_url)

        if category_html is not None:
            found_urls = parse_categories(category_html, category_url, source)
            urls.extend(found_urls)

    return list(dict.fromkeys(urls))

def parse_categories(html, page_url, source):
    soup = BeautifulSoup(html, "html.parser")
    links = soup.find_all("a", href=True)

    found = set()

    for link in links:
        href = link["href"]
        pattern_found = source.article_pattern.search(href)
        if pattern_found:
            found.add(urljoin(page_url, href))

    return(found)

if __name__ == "__main__":
    main()

