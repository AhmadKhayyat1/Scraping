'''
import csv

#from models.venue import Venue
from models.venue import Product


def is_duplicate_venue(venue_name: str, seen_names: set) -> bool:
    return venue_name in seen_names


def is_complete_venue(venue: dict, required_keys: list) -> bool:
    return all(key in venue for key in required_keys)

'''
'''
def save_venues_to_csv(venues: list, filename: str):
    if not venues:
        print("No venues to save.")
        return

    # Use field names from the Venue model
    fieldnames = Venue.model_fields.keys()

    with open(filename, mode="w", newline="", encoding="utf-8") as file:
        writer = csv.DictWriter(file, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(venues)
    print(f"Saved {len(venues)} venues to '{filename}'.")
'''
'''
def save_venues_to_csv(products: list, filename: str):
    if not products:
        print("No products to save.")
        return

    # Use field names from the Product model
    fieldnames = Product.model_fields.keys()

    with open(filename, mode="w", newline="", encoding="utf-8") as file:
        writer = csv.DictWriter(file, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(products)
    print(f"Saved {len(products)} products to '{filename}'.")
    
'''
import csv
from models.venue import Product


def is_duplicate_venue(product_name: str, seen_names: set) -> bool:
    return product_name in seen_names


def is_complete_venue(product: dict, required_keys: list) -> bool:
    return all(key in product for key in required_keys)


def save_venues_to_csv(products: list, filename: str):
    if not products:
        print("No products to save.")
        return

    # Use field names from the Product model
    fieldnames = ["name", "price", "unit", "category", "date", "source"]

    #fieldnames = Product.model_fields.keys()

    with open(filename, mode="w", newline="", encoding="utf-8") as file:
        writer = csv.DictWriter(file, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(products)
    print(f"Saved {len(products)} products to '{filename}'.")
