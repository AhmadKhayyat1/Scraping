from pydantic import BaseModel

class Product(BaseModel):
    """
    Represents product data from Sarper Market.
    """
    name: str
    price: str
    sku: str
