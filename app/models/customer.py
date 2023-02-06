from pydantic import BaseModel


class Customer(BaseModel):
    unique_identifier: str
