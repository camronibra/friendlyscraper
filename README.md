# 📚 FriendlyScraper 

*A small scraper on a mission: stopping machines from misclassifying "low-resource" languages spoken by millions.* 

## Why I built this project

Low-resource languages get routinely misclassified or lumped into a "dominant" relative in NLP tooling. Fixing that is the greater objective. 

This scraper is the small first step: a rate-limited tool for pulling manageable text samples to test classification approaches on.

## Quick start

```bash
pip install -r requirements.txt
python scraper.py
```
Runs against the bundled sandbox site (e.g. books.toscrape.com, a site that is intended for scraping practice) and writes a JSONL file (takes one JSON object per line: url, text). The output filename is set in source.py.

## How it works
For each source, you supply the category pages, an article URL pattern (regex) and a CSS selector for the article text.

## Configuring a source
Copy and paste the example from `source.py` into `sources_local.py` (gitignored, takes priority) and edit `name`, `base_url`, `category_urls`, `article_pattern` and `content_selector`.

## What it does
- Checks robots.txt before every request and skips disallowed URLs.
- Identifies itself with a descriptive User-Agent.
- Waits at least 2 seconds between requests (could take longer if the site sets a crawl delay).
- Stores the source URL with every article.
- Ships no scraped data.

## Scope
Live web scraping is the current, small-scale mode. It is a testbed for sampling text, not intended to be scaled as-is. 

## Disclaimer
Not affiliated with any website scraped with it. Use only where a site's terms of service and the law permit. You are held responsible for your own compliance, including copyright. Provided as is, without warranty.

## Limitations and v2
- You must supply the URL pattern and selector per site (planned: sitemap/RSS discovery and automatic article extraction).
- No support for JS-rendered sites.
- No retry/backoff on 429/503 responses.
- Dari-vs-Persian classification is the current focus of active development.
- **v2 direction** live web crawling becomes an optional mode rather than the primary one. The main path shifts to identifying Dari-language text inside web archives (e.g. Common Crawl). This will use the same extraction and classification logic at a scale that live web scraping was never meant to reach. 

## Design decisions
- Config-driven `Source` objects keep site-specific details out of the scraper logic.
- A sandbox site is used for testing so development doesn't hit real outlets.
- Code only: scraped data is not distributed.
