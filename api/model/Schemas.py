from pydantic import BaseModel


class Fruits(BaseModel):
    name: str
    price: str
