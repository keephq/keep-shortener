import hashlib

from google.cloud import datastore
from fastapi import Depends, HTTPException, Request

from app.models.customer import Customer

# init datastore client once
client = datastore.Client()


def get_datastore_client() -> datastore.Client:
    return client


def verify_customer(
    request: Request, datastore_client: datastore.Client = Depends(get_datastore_client)
) -> Customer:
    api_key = request.headers.get("X-API-KEY")
    if not api_key:
        raise HTTPException(status_code=401, detail="Missing API Key")

    api_key_hashed = hashlib.sha256(api_key.encode()).hexdigest()

    # get customer from google datastore
    key = datastore_client.key('Customers', api_key_hashed)
    item = client.get(key)
    if not item:
        raise HTTPException(status_code=401, detail="Invalid API Key")
    return Customer(**item)
