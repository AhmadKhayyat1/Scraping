BASE_URL = "https://www.sarpermarket.com"

CATEGORIES = [
    "/urun-grubu/atistirmalik/gofret",
]

# Select the <a> tag that contains product data
CSS_SELECTOR = "a[href*='/urunler/']"  # Product wrapper (each product link)

# Inside each product wrapper:
CSS_PRODUCT_NAME = "h2"  # Product name inside <h2>
CSS_PRODUCT_PRICE = "span.gt-price span.woocommerce-Price-amount"
CSS_PRODUCT_CURRENCY = "span.woocommerce-Price-currencySymbol font font"


CSS_PRODUCT_SKU = "div:nth-of-type(2)"  # SKU inside the second div

REQUIRED_KEYS = ["name", "price", "sku"]  # Remove "price" (some items might not have prices)
PAGINATION_FORMAT = "?page={page}"

MAX_RETRIES = 3
REQUEST_DELAY = 2
