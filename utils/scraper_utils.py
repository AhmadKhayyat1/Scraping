import os
from typing import List, Set, Tuple
from bs4 import BeautifulSoup
from crawl4ai import AsyncWebCrawler, BrowserConfig, CrawlerRunConfig, CacheMode
from config import CSS_PRODUCT_NAME, CSS_PRODUCT_PRICE, CSS_PRODUCT_CURRENCY, CSS_PRODUCT_SKU, PAGINATION_FORMAT


def get_browser_config() -> BrowserConfig:
    """Returns browser configuration for crawling."""
    return BrowserConfig(
        browser_type="chromium",
        headless=True,
        user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36..."
    )


async def fetch_product_page(
    crawler: AsyncWebCrawler,
    page_number: int,
    base_url: str,
    category: str,
    css_selector: str,
    session_id: str,
    required_keys: List[str],
    seen_skus: Set[str],
) -> Tuple[List[dict], bool]:
    """Fetches and extracts products from a single category page."""

    page_url = f"{base_url}{category}{PAGINATION_FORMAT.format(page=page_number)}"
    print(f"Fetching: {page_url}")

    # Fetch the page using AsyncWebCrawler
    result = await crawler.arun(
        url=page_url,
        config=CrawlerRunConfig(
            cache_mode=CacheMode.BYPASS,  # Avoid caching issues
            session_id=session_id,
            css_selector=css_selector,
        ),
    )

    if not result.success:
        print(f"❌ Failed to fetch {page_url}")
        return [], False

    # Parse the fetched HTML using BeautifulSoup
    #soup = BeautifulSoup(result.cleaned_html, "html.parser")
    soup = BeautifulSoup(result.cleaned_html, "html.parser")
    print("=== DEBUG: Sample HTML ===")
    print(soup.prettify()[:2000])  # Print the first 2000 characters of fetched HTML
    print("===========================")

    products = []

    for product_link in soup.select(css_selector):
        name_elem = product_link.select_one(CSS_PRODUCT_NAME)
        price_elem = product_link.select_one(CSS_PRODUCT_PRICE)
        if price_elem:
            print(f"🔎 Found Price Element: {price_elem}")
        else:
            print("⚠️ No price found for this product!")

        currency_elem = product_link.select_one(CSS_PRODUCT_CURRENCY)
        sku_elem = product_link.select_one(CSS_PRODUCT_SKU)

        name = name_elem.get_text(strip=True) if name_elem else "Unknown"
        sku = sku_elem.get_text(strip=True) if sku_elem else "N/A"

        def clean_price(price_text):
            """Remove extra spaces and non-numeric characters."""
            return "".join(filter(lambda x: x.isdigit() or x == ".", price_text.replace("\xa0", ""))).strip()
        def clean_price(price_text):
            """Removes extra spaces, &nbsp;, and keeps only numeric values with decimals."""
            return price_text.replace("\xa0", "").replace(",", ".").strip()  # Removes &nbsp; and fixes decimal

        price = clean_price(price_elem.get_text()) if price_elem else "Price Missing"
        currency = clean_price(currency_elem.get_text()) if currency_elem else ""

        full_price = f"{price} {currency}" if currency else price  # Combine price with currency
        
        print(f"🔹 Extracted Product: {name} | Price: {full_price} | SKU: {sku}")  # Debug output

        if sku in seen_skus:
            continue  

        product = {
            "name": name,
            "sku": sku,
            "price": full_price,  # Always include price
        }

        products.append(product)
        seen_skus.add(sku)

    no_results = len(products) == 0
    return products, no_results
