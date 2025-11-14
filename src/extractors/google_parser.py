thonimport logging
import requests
from bs4 import BeautifulSoup

class GoogleParser:
    def __init__(self, config):
        self.user_agent = config.get("user_agent", "Mozilla/5.0")
        self.base_url = "https://www.google.com/search?q={query}"

    def fetch_and_parse(self, query):
        url = self.base_url.format(query=query.replace(" ", "+"))
        headers = {"User-Agent": self.user_agent}

        try:
            response = requests.get(url, headers=headers, timeout=10)
            response.raise_for_status()
        except Exception as e:
            logging.error(f"Failed fetching Google results for '{query}': {e}")
            return []

        soup = BeautifulSoup(response.text, "html.parser")
        result_blocks = soup.select("div.g")

        extracted = []
        rank = 1

        for block in result_blocks:
            title_el = block.select_one("h3")
            link_el = block.select_one("a")
            snippet_el = block.select_one("div.VwiC3b")

            if not title_el or not link_el:
                continue

            item = {
                "query": query,
                "title": title_el.get_text(strip=True),
                "url": link_el.get("href"),
                "snippet": snippet_el.get_text(strip=True) if snippet_el else "",
                "rank": rank,
                "displayedUrl": (block.select_one("span.VuuXrf") or {}).get("aria-label", ""),
                "sourceType": "organic"
            }
            extracted.append(item)
            rank += 1

        return extracted