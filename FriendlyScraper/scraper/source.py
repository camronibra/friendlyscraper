import re
from models import Source

SOURCES = [
    Source(
        name="books-sandbox",
        base_url="https://books.toscrape.com/",
        category_urls=(
            "https://books.toscrape.com/catalogue/category/books/mystery_3/index.html",
            ),
        article_pattern=(re.compile(r"^(\.\./){3,}[^/]+_\d+/index\.html$")),
        content_selector="#product_description + p",
        ),
        ]
