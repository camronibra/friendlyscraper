from dataclasses import dataclass
import re

@dataclass
class Source:
    name: str
    base_url: str
    category_urls: tuple[str, ...]
    article_pattern: re.Pattern
    content_selector: str

