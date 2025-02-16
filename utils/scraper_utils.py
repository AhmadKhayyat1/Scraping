
import json
from bs4 import BeautifulSoup
from config import CATEGORY_PAGE_SELECTOR
import os
from typing import List, Set, Tuple

from crawl4ai import (
    AsyncWebCrawler,
    BrowserConfig,
    CacheMode,
    CrawlerRunConfig,
    LLMExtractionStrategy,
)

#from models.venue import Venue
from models.venue import Product  # Update this line
from utils.data_utils import is_complete_venue, is_duplicate_venue


def get_browser_config() -> BrowserConfig:
    """
    Returns the browser configuration for the crawler.

    Returns:
        BrowserConfig: The configuration settings for the browser.
    """
    # https://docs.crawl4ai.com/core/browser-crawler-config/
    return BrowserConfig(
        browser_type="chromium",  # Type of browser to simulate
        headless=False,  # Whether to run in headless mode (no GUI)
        verbose=True,  # Enable verbose logging
    )




def get_llm_strategy() -> LLMExtractionStrategy:
    
    return LLMExtractionStrategy(
        provider="groq/deepseek-r1-distill-llama-70b",
        api_token=os.getenv("GROQ_API_KEY"),
        schema=Product.model_json_schema(),  # Use the Product schema
        extraction_type="schema",
        instruction=(
            "Extract all product objects with 'name', 'price', 'old_price', 'discount', "
            "'store_name', 'product_url', 'image_url', 'category', 'brand', 'availability', "
            "'rating', and 'reviews' from the following content."
        ),
        input_format="markdown",
        verbose=True,
     )


async def check_no_results(
    crawler: AsyncWebCrawler,
    url: str,
    session_id: str,
) -> bool:
    """
    Checks if the "No Results Found" message is present on the page.

    Args:
        crawler (AsyncWebCrawler): The web crawler instance.
        url (str): The URL to check.
        session_id (str): The session identifier.

    Returns:
        bool: True if "No Results Found" message is found, False otherwise.
    """
    # Fetch the page without any CSS selector or extraction strategy
    result = await crawler.arun(
        url=base_url,
        config=CrawlerRunConfig(
            cache_mode=CacheMode.BYPASS,
            session_id=session_id,
        ),
    )

    if result.success:
        if "No Results Found" in result.cleaned_html:
            return True
    else:
        print(
            f"Error fetching page for 'No Results Found' check: {result.error_message}"
        )

    return False




async def fetch_and_process_page(
    crawler: AsyncWebCrawler,
    url: str,
    css_selector: str,
    llm_strategy: LLMExtractionStrategy,
    session_id: str,
    required_keys: List[str],
    seen_names: Set[str],
) -> Tuple[List[dict], bool]:
    """
    Fetches and processes a single page of product data.
    """
    print(f"Loading page: {url}")

    # Fetch page content with the extraction strategy
    result = await crawler.arun(
        url=url,
        config=CrawlerRunConfig(
            cache_mode=CacheMode.BYPASS,
            extraction_strategy=llm_strategy,
            css_selector=css_selector,
            session_id=session_id,
        ),
    )

    if not (result.success and result.extracted_content):
        print(f"Error fetching page: {result.error_message}")
        return [], False
    
    # Parse extracted content
    extracted_data = json.loads(result.extracted_content)
    if not extracted_data:
        print(f"No products found on page: {url}")
        return [], False

    # Process products
    complete_products = []
    for product in extracted_data:
        # Debugging: Print each product to understand its structure
        print("Processing product:", product)

        # Ignore the 'error' key if it's False
        if product.get("error") is False:
            product.pop("error", None)

        if not is_complete_venue(product, required_keys):
            continue  # Skip incomplete products

        if is_duplicate_venue(product["name"], seen_names):
            print(f"Duplicate product '{product['name']}' found. Skipping.")
            continue  # Skip duplicate products

        # Add product to the list
        seen_names.add(product["name"])
        complete_products.append(product)

    if not complete_products:
        print(f"No complete products found on page: {url}")
        return [], False

    print(f"Extracted {len(complete_products)} products from page: {url}")
    return complete_products, False  # Continue crawling

from config import CATEGORY_PAGE_SELECTOR

async def extract_category_urls(crawler: AsyncWebCrawler, base_url: str) -> List[str]:
    """
    Extracts category URLs from the sidebar.
    """
    print(f"CATEGORY_PAGE_SELECTOR: {CATEGORY_PAGE_SELECTOR}")  # Debugging
    result = await crawler.arun(
        url=base_url,
        config=CrawlerRunConfig(
            cache_mode=CacheMode.BYPASS,
            css_selector=CATEGORY_PAGE_SELECTOR,
        ),
    )

    if not result.success:
        print(f"[ERROR] Error fetching categories: {result.error_message}")
        return []

    # Extract category URLs
    category_urls = []
    soup = BeautifulSoup(result.cleaned_html, "html.parser")
    for link in soup.select(CATEGORY_PAGE_SELECTOR):
        href = link.get("href")
        if href and "/kategori/" in href:
            category_urls.append(f"{BASE_URL}{href}")

    print(f"[INFO] Found {len(category_urls)} categories.")
    return category_urls


async def fetch_products_from_category(
    crawler: AsyncWebCrawler, category_url: str, llm_strategy: LLMExtractionStrategy, required_keys: List[str], seen_names: Set[str]
) -> List[dict]:
    """
    Extracts products from a given category page.
    """
    print(f"Scraping category: {category_url}")

    all_products = []
    page_number = 1

    while True:
        url = f"{category_url}?page={page_number}"  # Adjust if needed
        print(f"Fetching page {page_number} of category: {category_url}")

        result = await crawler.arun(
            url=url,
            config=CrawlerRunConfig(
                cache_mode=CacheMode.BYPASS,
                extraction_strategy=llm_strategy,
                css_selector="div.product-summary",  # Correct product selector
            ),
        )

        if not (result.success and result.extracted_content):
            print(f"Error fetching category page: {url}")
            break  # Stop if no data is found

        extracted_data = json.loads(result.extracted_content)
        if not extracted_data:
            print(f"No products found in {url}.")
            break  # Stop if no products are found

        for product in extracted_data:
            if not is_complete_product(product, required_keys):
                continue
            if is_duplicate_product(product["name"], seen_names):
                print(f"Duplicate product '{product['name']}' found. Skipping.")
                continue

            seen_names.add(product["name"])
            all_products.append(product)

        # Check if there's a next page
        if not await has_next_page(crawler, url):
            break  # Stop if no next page is found
        page_number += 1

    print(f"Extracted {len(all_products)} products from {category_url}.")
    return all_products
async def has_next_page(crawler: AsyncWebCrawler, url: str) -> bool:
    """
    Checks if there's a next page available.
    """
    result = await crawler.arun(
        url=url,
        config=CrawlerRunConfig(
            cache_mode=CacheMode.BYPASS,
            css_selector="ul.ngx-pagination a",  # Correct pagination selector
        ),
    )

    if not result.success:
        print(f"Error checking pagination: {result.error_message}")
        return False

    soup = BeautifulSoup(result.cleaned_html, "html.parser")
    next_page = soup.select("ul.ngx-pagination a")  # Look for next page link
    return bool(next_page)  # Return True if pagination exists
