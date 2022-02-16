from turtle import title
import fire
import requests
from bs4 import BeautifulSoup
from dataclasses import dataclass
from typing import List
import tqdm

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


def main():
    r = requests.get(ITEMS_PAGE_URL)
    
    soup = BeautifulSoup(r.content, "html.parser")

    tables = soup.find_all("table", class_ = "wikitable")

    items = []

    print("Generating Items metadata...")

    for table in tqdm.tqdm(tables):
        for a_element in table.find_all("a"):
            img_element = a_element.find("img")

            if "base64" in img_element["src"]:
                image_url = img_element["data-src"]
            else:
                image_url = img_element["src"]

            name = a_element["title"].replace("/","_")

            item = Item(
                name = name,
                url = BASE_URL + "/" + a_element["href"],
                type_ = None,
                image_url = image_url,
                image_path = f"data/images/{name}.png",
                effects = None,
                interactions = None
            )
            
            items.append(item)

    print("Generating data...")
    for item in tqdm.tqdm(items):
        # Save image
        r = requests.get(item.image_url)

        with open(item.image_path, 'wb') as f:
            f.write(r.content)

        # Retrieve items page
        r = requests.get(item.url) 
        print(item.url)
        soup = BeautifulSoup(r.content, "html.parser")

        ul_element = soup.find("span", attrs = {"id":"Effects"}).find_next("ul")
        print(ul_element)

        # li_elements = 
        # print(li_elements)
        for li in ul_element.find_next("li"):
            print(li)

        break

    


if __name__ == "__main__":
    fire.Fire(main)