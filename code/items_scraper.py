import argparse
import requests
from bs4 import BeautifulSoup, Tag
from dataclasses import dataclass
from typing import List
import tqdm
import pandas as pd
import os

BASE_URL = "https://bindingofisaacrebirth.fandom.com"
ITEMS_PAGE_URL = f"{BASE_URL}/wiki/Collection_Page_(Repentance)"


@dataclass
class Item:
    name: str
    url: str
    type_: str
    image_url: str
    image_path: str
    effects: List[str]
    interactions: str


def main(images_output_path: str, metadata_output_path: str):

    create_output_paths(images_output_path, metadata_output_path)

    r = requests.get(ITEMS_PAGE_URL)

    soup = BeautifulSoup(r.content, "html.parser")

    tables = soup.find_all("table", class_="wikitable")

    items = []

    print(f"Downloading images at {images_output_path}...")
    for table in tqdm.tqdm(tables):
        for a_element in table.find_all("a"):

            img_element = a_element.find("img")
            image_url = get_item_image_url(img_element)

            name = get_item_name(a_element)
            url = get_item_url(a_element)

            item = Item(
                name=name,
                url=url,
                type_=None,
                image_url=image_url,
                image_path=f"{images_output_path}/{name}.png",
                effects=None,
                interactions=None
            )

            download_item_image(item.image_url, item.image_path)
            items.append(item)

    print(f"Generating metadata CSV file at {metadata_output_path}...")
    metadata = pd.DataFrame([item.__dict__ for item in items])
    metadata.to_csv(f"{metadata_output_path}/metadata.csv", index=False)

def create_output_paths(images_output_path, metadata_output_path):
    """Check if output paths exists. If not, create them."""
    if not os.path.exists(images_output_path):
        os.makedirs(images_output_path)

    if not os.path.exists(metadata_output_path):
        os.makedirs(metadata_output_path)


def get_item_url(a_element: Tag) -> str:
    """Return item url given an <a href=...> element"""
    return BASE_URL + "/" + a_element["href"]


def get_item_name(a_element: Tag) -> str:
    """Return item name from an <a href=...> element"""
    return a_element["title"].replace("/", "_")


def get_item_image_url(img_element: Tag) -> str:
    """ Return item image url given an <img ...> element of an item. """
    if "base64" in img_element["src"]:
        image_url = img_element["data-src"]
    else:
        image_url = img_element["src"]

    return image_url


def get_item_page_section_by_id(soup: BeautifulSoup, section_id: str) -> Tag:
    """ Return the page section of an item page given an id.
    If the page does not have the section, return None."""

    span_element = soup.find("span", attrs={"id": section_id})

    if span_element:
        ul_section = span_element.find_next("ul")

        return ul_section


def download_item_image(url: str, path: str):
    """ Download the item imagen at url and save it in path """
    try:
        r = requests.get(url)
        r.raise_for_status()
    except requests.exceptions.HTTPError as err:
        print(err)
        raise

    with open(path, 'wb') as f:
        f.write(r.content)


def retrieve_item_page(url: str) -> str:
    """ Return the webpage at url as string """
    try:
        r = requests.get(url)
        r.raise_for_status()
    except requests.exceptions.HTTPError as err:
        print(err)
        raise

    return r.text


if __name__ == "__main__":
    parser = argparse.ArgumentParser()

    parser.add_argument("--images_path", required=True,
                        help="Output path for the images", type=str)
    parser.add_argument("--metadata_path", required=True,
                        help="Output path for the metadata CSV file.", type=str)

    args = parser.parse_args()

    main(args.images_path, args.metadata_path)
