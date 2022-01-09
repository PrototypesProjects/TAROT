import pandas as pd
import requests
from lxml import html

tarot_cards = pd.read_csv("tarot.csv")


def fetch_content(url, name):
    print(f"FETCHING {url}")
    res = requests.get(url)
    tree = html.fromstring(res.content)
    xpath = "//img[@width >200]"
    image_tag = tree.xpath(xpath)[0]

    image_url = image_tag.get("data-src")

    r = requests.get(image_url)
    with open(f'thoth_images/{name}.jpg', 'wb') as f:
        f.write(r.content)

    pass

h = [fetch_content(url, i) for url, i in zip(tarot_cards["f"], tarot_cards.index)]
