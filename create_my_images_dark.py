import pandas as pd
from PIL import Image, ImageEnhance

from PIL import Image

import random

from PIL import ImageDraw

SIZE_PX = (1536, 2048)

tarot_cards = pd.read_csv("tarot.csv")
for card_words_str, card_name in zip(tarot_cards["words"], tarot_cards.index):
    print(card_name)
    img = Image.new('RGBA', SIZE_PX, color = 'red')
    im_insert = Image.open(f"my_images/{card_name}.png", 'r')

    img.paste(im_insert)

    # img = ImageEnhance.Brightness(img).enhance(0.6)
    # img = ImageEnhance.Contrast(img).enhance(0.6)


    TINT_COLOR = (0, 0, 0)  # Black
    TRANSPARENCY = .7  # Degree of transparency, 0-100%
    OPACITY = int(255 * TRANSPARENCY)

    overlay = Image.new('RGBA', img.size, TINT_COLOR+(0,))
    draw = ImageDraw.Draw(overlay)  # Create a context for drawing things on it.
    draw.rectangle(((0, 0), SIZE_PX), fill=TINT_COLOR+(OPACITY,))
    img = Image.alpha_composite(img, overlay)


    img.save(f"my_images_dark/{card_name}.png")
