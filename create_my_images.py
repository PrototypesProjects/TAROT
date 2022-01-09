import pandas as pd
from PIL import Image

import random

from PIL import ImageDraw

MINIMUM_WORDS = 100

tarot_cards = pd.read_csv("tarot.csv")


SIZE_PX = (1536, 2048)

for card_words_str, card_name in zip(tarot_cards["words"], tarot_cards.index):
    thoth_file = f"thoth_images/{card_name}.jpg"
    print(thoth_file)
    card_words = card_words_str.split(" ")
    while len(card_words) < MINIMUM_WORDS:
        card_words *= 2
    random.shuffle(card_words)
    card_words_str = " ".join(card_words).upper()
    print(card_words_str)


    img = Image.new('RGB', SIZE_PX, color = 'red')

    draw = ImageDraw.Draw(img)
    draw.line((0, 0) + img.size, fill=128, width=10)
    draw.line((0, img.size[1], img.size[0], 0), fill=128, width=10)
    draw.ellipse(((0,0), img.size), width=20)


    im_insert = Image.open(f'thoth_images/{card_name}.jpg', 'r')
    im_insert_basewidth = SIZE_PX[0]+390
    wpercent = (im_insert_basewidth/float(im_insert.size[0]))
    hsize = int((float(im_insert.size[1])*float(wpercent)))

    im_insert = im_insert.resize((im_insert_basewidth,hsize), Image.ANTIALIAS)

    im_insert_w, im_insert_h = im_insert.size
    offset = ((SIZE_PX[0] - im_insert_w) // 2, (SIZE_PX[1] - im_insert_h) // 2)
    img.paste(im_insert, offset)

    img.save(f'my_images/{card_name}.png')


