import string
import random

from google.cloud import datastore
from validators import url as url_validator
from fastapi.responses import RedirectResponse
from fastapi import APIRouter, Depends, HTTPException

from app.core.config import config
from app.core.dependencies import get_datastore_client
from app.core.dependencies import verify_customer
from app.models.customer import Customer


router = APIRouter()


@router.get(
    "/{customer_unique_identifier}/{short_url_identifier}",
    description="Redirect to the original URL",
)
def redirect_to_original_url(
    customer_unique_identifier: str,
    short_url_identifier: str,
    datastore_client: datastore.Client = Depends(get_datastore_client),
):
    # get the original url from datastore
    key = datastore_client.key(
        "Urls", short_url_identifier, namespace=customer_unique_identifier
    )
    item = datastore_client.get(key)
    if not item:
        raise HTTPException(status_code=404, detail="URL not found")

    # increment the clicks
    item["clicks"] += 1
    datastore_client.put(item)

    return RedirectResponse(url=item["original_url"])


@router.post("", description="Create short URLs based on given long URLs")
def create_short_url(
    urls: list[str],
    customer: Customer = Depends(verify_customer),
    datastore_client: datastore.Client = Depends(get_datastore_client),
):
    if not any(urls):
        raise HTTPException(status_code=400, detail="No URLs provided")

    keep_api_url = config.get("KEEP_API_URL")

    # structure is {'old_url': 'new_short_url'}
    shortened_urls = {}
    # validate urls
    for url in urls:
        # If it is not a valid url, return the same url
        if not url_validator(url):
            shortened_urls[url] = url
            continue

        # check if the url was already shortened
        existing_entity = list(
            datastore_client.query(kind="Urls", namespace=customer.unique_identifier)
            .add_filter("original_url", "=", url)
            .fetch(limit=1)
        )
        # if the url was already shortened, return the existing one
        if existing_entity:
            shortened_urls[
                url
            ] = f"{keep_api_url}/{customer.unique_identifier}/{entity[0].key.name}"
            continue

        # generate a random string which will be the short url
        short_url_identifier = "".join(
            random.choices(string.ascii_lowercase + string.digits, k=7)
        )

        # insert the entity to datastore
        key = datastore_client.key(
            "Urls", short_url_identifier, namespace=customer.unique_identifier
        )

        # create the entity in datastore
        entity = datastore.Entity(key=key)
        entity["original_url"] = url
        entity["clicks"] = 0
        datastore_client.put(entity)

        shortened_urls[
            url
        ] = f"{keep_api_url}/{customer.unique_identifier}/{short_url_identifier}"
    return shortened_urls
