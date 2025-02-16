
import asyncio

from crawl4ai import AsyncWebCrawler
from dotenv import load_dotenv

#from config import BASE_URL, CSS_SELECTOR, REQUIRED_KEYS
from config import BASE_URL, CATEGORY_PAGE_SELECTOR, PRODUCT_PAGE_SELECTOR, REQUIRED_KEYS




from utils.data_utils import (
    save_venues_to_csv,
)
from utils.scraper_utils import (
    fetch_and_process_page,
    get_browser_config,
    get_llm_strategy,
    extract_category_urls,
)

load_dotenv()



async def crawl_products():
    """
    Main function to crawl all categories and products.
    """
    browser_config = get_browser_config()
    llm_strategy = get_llm_strategy()
    session_id = "product_crawl_session"

    all_products = []
    seen_names = set()

    async with AsyncWebCrawler(config=browser_config) as crawler:
        print(f"[INFO] Fetching categories from {BASE_URL}")
        category_urls = await extract_category_urls(crawler, BASE_URL)

        if not category_urls:
            print("[ERROR] No categories found. Stopping crawl.")
            return

        print(f"[INFO] Found {len(category_urls)} categories. Starting product crawl.")

        for category_url in category_urls:
            print(f"[INFO] Crawling category: {category_url}")

            page_number = 1
            while True:
                url = f"{category_url}?page={page_number}"  # Ensure pagination
                print(f"[INFO] Fetching page {page_number} of {category_url}")

                products, no_results_found = await fetch_and_process_page(
                    crawler,
                    url,
                    PRODUCT_PAGE_SELECTOR,  # ✅ Use correct product selector
                    llm_strategy,
                    session_id,
                    REQUIRED_KEYS,
                    seen_names,
                )

                if no_results_found:
                    print(f"[INFO] No more products found in category: {category_url}")
                    break  # Stop pagination when no results are found

                if not products:
                    print(f"[WARN] No products extracted from page {page_number}.")
                    break  # Stop if no products are found

                all_products.extend(products)
                page_number += 1  # Move to next page

                await asyncio.sleep(2)  # Avoid getting blocked

    if all_products:
        save_products_to_csv(all_products, "market_prices.csv")
        print(f"[SUCCESS] Saved {len(all_products)} products to 'market_prices.csv'.")
    else:
        print("[ERROR] No products were found during the crawl.")

    llm_strategy.show_usage()



async def main():
    """
    Entry point of the script.
    """
    await crawl_products()


if __name__ == "__main__":
    asyncio.run(main())
