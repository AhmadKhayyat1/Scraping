# config.py

#BASE_URL = "https://www.theknot.com/marketplace/wedding-reception-venues-atlanta-ga"
#CSS_SELECTOR = "[class^='info-container']"
#REQUIRED_KEYS = [
#    "name",
#    "price",
#    "location",
#    "capacity",
#    "rating",
#    "reviews",
#    "description",
#]

# config.py
'''
BASE_URL = "https://marketfiyati.org.tr/"
CSS_SELECTOR = ".product-item"  # Adjust based on the website's structure
REQUIRED_KEYS = [
    "name",
    "price",
    "old_price",
    "discount",
    "store_name",
    "product_url",
    "image_url",
    "category",
    "brand",
    "availability",
    "rating",
    "reviews",
 ]
'''
'''
# config.py

BASE_URL = "https://marketfiyati.org.tr"
CATEGORY_URL = "https://marketfiyati.org.tr/kategori/Meyve%20ve%20Sebze"
CSS_SELECTOR = "[class^='product-summary']"  # Adjust based on the website's structure
REQUIRED_KEYS = [
    "name",
    "price",
    "old_price",
    "discount",
    "store_name",
    "product_url",
    "image_url",
    "category",
    "brand",
    "availability",
    "rating",
    "reviews",
]
'''
BASE_URL = "https://marketfiyati.org.tr"
CATEGORY_PAGE_SELECTOR = ".d-flex a"  # Example selector for category links
PRODUCT_PAGE_SELECTOR = ".products-container .product-summary .product-details"
REQUIRED_KEYS = [
    "name",
    "price",
    "old_price",
    "discount",
    "store_name",
    "product_url",
    "image_url",
    "category",
    "brand",
    "availability",
    "rating",
    "reviews",
]