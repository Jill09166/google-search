thonimport json
import logging
from pathlib import Path
from extractors.google_parser import GoogleParser
from outputs.exporters import JSONExporter
from extractors.utils_cleaner import normalize_keyword

logging.basicConfig(level=logging.INFO, format="%(levelname)s: %(message)s")

CONFIG_PATH = Path(__file__).resolve().parent / "config" / "settings.example.json"
DATA_PATH = Path(__file__).resolve().parents[1] / "data" / "keywords.sample.txt"

def load_config():
    with open(CONFIG_PATH, "r") as f:
        return json.load(f)

def load_keywords():
    if not DATA_PATH.exists():
        logging.error(f"Keyword file not found at {DATA_PATH}")
        return []
    with open(DATA_PATH, "r") as f:
        return [normalize_keyword(line.strip()) for line in f if line.strip()]

def main():
    config = load_config()
    keywords = load_keywords()

    if not keywords:
        logging.warning("No keywords loaded. Exiting.")
        return

    parser = GoogleParser(config=config)
    exporter = JSONExporter()

    results = []
    for kw in keywords:
        logging.info(f"Processing keyword: {kw}")
        data = parser.fetch_and_parse(kw)
        results.extend(data)

    output_path = exporter.export(results)
    logging.info(f"Results saved to: {output_path}")

if __name__ == "__main__":
    main()