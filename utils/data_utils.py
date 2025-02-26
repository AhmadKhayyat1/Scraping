import csv
from typing import Set, Dict
from models.product import Product

def save_products_to_csv(products: list, filename: str):
    """Saves the scraped product data to a CSV file."""
    if not products:
        print("No products to save.")
        return

    fieldnames = Product.model_fields.keys()

    with open(filename, "w", newline="", encoding="utf-8") as file:
        writer = csv.DictWriter(file, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(products)

    print(f"Saved {len(products)} products to {filename}")

def clean_price(price_str: str) -> str:
    """Removes currency symbols and extra spaces from price strings."""
    return price_str.replace("$", "").replace("₺", "").strip()
