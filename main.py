import asyncio
from dotenv import load_dotenv
from crawl4ai import AsyncWebCrawler
from config import BASE_URL, CATEGORIES, CSS_SELECTOR, REQUIRED_KEYS, REQUEST_DELAY
from utils.data_utils import save_products_to_csv
from utils.scraper_utils import fetch_product_page, get_browser_config

load_dotenv()

async def crawl_category(crawler: AsyncWebCrawler, category: str, session_id: str):
    """Crawls all pages of a given category and extracts products."""
    page_number = 1
    all_products = []
    seen_skus = set()

    while True:
        products, no_results = await fetch_product_page(
            crawler=crawler,
            page_number=page_number,
            base_url=BASE_URL,
            category=category,
            css_selector=CSS_SELECTOR,
            session_id=session_id,
            required_keys=REQUIRED_KEYS,
            seen_skus=seen_skus,
        )

        if no_results or not products:
            break

        all_products.extend(products)
        page_number += 1
        await asyncio.sleep(REQUEST_DELAY)

    return all_products

async def main():
    """Main function to scrape categories and save data."""
    browser_config = get_browser_config()
    session_id = "sarper_crawl_v1"

    async with AsyncWebCrawler(config=browser_config) as crawler:
        all_products = []

        for category in CATEGORIES:
            print(f"Scraping category: {category}")
            products = await crawl_category(crawler, category, session_id)
            all_products.extend(products)
            print(f"Found {len(products)} products in {category}")

        if all_products:
            save_products_to_csv(all_products, "sarper_products.csv")
        else:
            print("No products scraped.")

if __name__ == "__main__":
    asyncio.run(main())
