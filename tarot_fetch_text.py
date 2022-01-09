import pandas as pd
import requests
from lxml import html

tarot_cards = pd.read_csv("tarot.csv")


def fetch_content(url):
    print(f"FETCHING {url}")
    res = requests.get(url)
    tree = html.fromstring(res.content)
    xpath = "(//*[not(self::script or self::style)]/text()[string-length() > 50])"
    output = "\n\n".join(tree.xpath(xpath))
    return output


h = [fetch_content(url) for url in tarot_cards["f"]]
i = [fetch_content(url) for url in tarot_cards["g"]]
tarot_cards_out = tarot_cards.assign(h=h)
tarot_cards_out = tarot_cards_out.assign(i=i)
tarot_cards_out.to_csv("tarot_with_text.csv")
