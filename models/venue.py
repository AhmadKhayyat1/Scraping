'''
from pydantic import BaseModel


#class Venue(BaseModel):
class Product(BaseModel):
    """
    Represents the data structure of a Venue.
    """

    name: str
    price: str
    old_price: str | None
    discount: str | None
    store_name: str
    product_url: str
    image_url: str
    category: str
    brand: str
    availability: str
    rating: float | None
    reviews: int | None

    #name: str
    #location: str
    #price: str
    #capacity: str
    #rating: float
    #reviews: int
    #description: str
'''
from pydantic import BaseModel


class Product(BaseModel):
    """
    Represents the data structure of a Product.
    """

    name: str
    price: str
    unit: str
    category: str
    date: str
    source: str
