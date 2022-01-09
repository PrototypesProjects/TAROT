

import pandas as pd
import math
from reportlab.lib.colors import black, white, Color, yellow
from reportlab.lib.styles import ParagraphStyle
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfgen.canvas import Canvas
from reportlab.lib.units import inch, cm
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.platypus import Paragraph

FONT_NAME = "UnifrakturMaguntia"
pdfmetrics.registerFont(TTFont(FONT_NAME, 'UnifrakturMaguntia.ttf'))

tarot_cards = pd.read_csv("tarot.csv")

# WIDTH, HEIGHT = (4.711 * inch, 6.282 * inch) #ipad mini
WIDTH, HEIGHT = (2.539 * inch, 5.496 * inch) #iphone


CORNER_SQUARE_SIDE = 0.4 * inch
CORNER_BORDER = 0.1 * inch

F_COLOR, B_COLOR, D_COLOR, FADE_COLOR, HALF_FADE_COLOR = (white, black, Color(0.13, 0, 0), Color(0.3, 0.33, 0.33), Color(0.4, 0.43, 0.43))

c = Canvas("TAROT.pdf", pagesize=(WIDTH, HEIGHT))
def draw_corner(c, x1, y1, x2, y2, s, bottom_corner_flip=False):
    c.saveState()

    c.setFont("Helvetica", 10)
    c.setStrokeColor(FADE_COLOR)
    c.setFillColor(D_COLOR)
    c.setLineWidth(0.01)

    c.rect(x1, y1, CORNER_SQUARE_SIDE, CORNER_SQUARE_SIDE, fill=1, stroke=1)
    # c.line(x1, y1, x2, y2)
    # c.line(x2, y1, x1, y2)

    if isinstance(s, str):

        c.setFillColor(F_COLOR)
        c.setStrokeColor(F_COLOR)
        c.setLineWidth(3)
        x_center = x1 + (x2 - x1) / 2.0
        y_center = y1 + (y2 - y1) / 2.0
        x_1st_4th = x1 + (x2 - x1) / 4.0
        x_2nd_4th = x1 + (x2 - x1) / 4.0 * 2.0
        x_3rd_4th = x1 + (x2 - x1) / 4.0 * 3.0

        y1_border = y1 + (y2 - y1) / 6.0
        y2_border = y2 - (y2 - y1) / 6.0



        if s == "X":
            c.setStrokeColor(HALF_FADE_COLOR)
            c.line(x_1st_4th, y1_border, x_3rd_4th, y2_border)
            c.line(x_3rd_4th, y1_border, x_1st_4th, y2_border)

        if s == "V":
            c.setStrokeColor(HALF_FADE_COLOR)
            c.line(x_1st_4th, y2_border, x_center, y1_border)
            c.line(x_center, y1_border, x_3rd_4th, y2_border)
            c.line(x_center, y1_border-CORNER_SQUARE_SIDE*0.03, x_center, y1_border+CORNER_SQUARE_SIDE*0.03)

        if s == "\\":
            c.setStrokeColor(FADE_COLOR)
            c.line(x_1st_4th, y2_border, x_3rd_4th, y1_border)
        if s == "/":
            c.setStrokeColor(FADE_COLOR)
            c.line(x_1st_4th, y1_border, x_3rd_4th, y2_border)

        if s == "I":
            c.setStrokeColor(HALF_FADE_COLOR)
            c.line(x_center, y1_border, x_center, y2_border)

        if s == "II":
            c.setStrokeColor(HALF_FADE_COLOR)
            x_1st_3rd = x1 + (x2-x1)/3.0
            x_2nd_3rd = x1 + (x2-x1)/3.0*2.0
            c.line(x_1st_3rd, y1_border, x_1st_3rd, y2_border)
            c.line(x_2nd_3rd, y1_border, x_2nd_3rd, y2_border)


        if s == "III":
            c.setStrokeColor(HALF_FADE_COLOR)
            c.line(x_1st_4th, y1_border, x_1st_4th, y2_border)
            c.line(x_2nd_4th, y1_border, x_2nd_4th, y2_border)
            c.line(x_3rd_4th, y1_border, x_3rd_4th, y2_border)

        if s =="🞡":
            c.setStrokeColor(FADE_COLOR)
            if bottom_corner_flip:
                c.transform(1, 0, 0, -1, 0, y1 + CORNER_SQUARE_SIDE + CORNER_BORDER)
            c.line(x_center, y1_border, x_center, y2_border)
            y_sword = y1_border + (x_3rd_4th - x_1st_4th)/2.0
            c.line(x_1st_4th, y_sword, x_3rd_4th, y_sword)

        if s == "O":
            c.setStrokeColor(FADE_COLOR)

            if bottom_corner_flip:
                c.transform(1, 0, 0, -1, 0, y1 + CORNER_SQUARE_SIDE + CORNER_BORDER)

            c.setLineWidth(2.2)

            r = CORNER_SQUARE_SIDE * 0.38
            c.circle(x_center,y_center, r, fill=0)
            c.setLineWidth(1.2)

            pentagon = []
            for n in range(0, 5):
                x = x_center + r * math.cos(math.radians(90 + n * 72))
                y = y_center + r * math.sin(math.radians(90 + n * 72))
                pentagon.append([x, y])
            c.line(pentagon[0][0], pentagon[0][1], pentagon[2][0], pentagon[2][1])
            c.line(pentagon[2][0], pentagon[2][1], pentagon[4][0], pentagon[4][1])
            c.line(pentagon[4][0], pentagon[4][1], pentagon[1][0], pentagon[1][1])
            c.line(pentagon[1][0], pentagon[1][1], pentagon[3][0], pentagon[3][1])
            c.line(pentagon[3][0], pentagon[3][1], pentagon[0][0], pentagon[0][1])

        if s == "U":
            c.setStrokeColor(FADE_COLOR)

            if bottom_corner_flip:
                c.transform(1, 0, 0, -1, 0, y1 + CORNER_SQUARE_SIDE + CORNER_BORDER)

            c.setLineWidth(2)

            y_cup_bottom = y_center-CORNER_SQUARE_SIDE * 0.09
            c.arc(x_1st_4th, y_cup_bottom, x_3rd_4th, y2+CORNER_SQUARE_SIDE * (1.0/3.0), 180, 180)
            # c.line(x_1st_4th, y2_border, x_1st_4th, y_center)
            c.line(x_center, y_cup_bottom, x_center, y1_border)
            c.line(x_1st_4th, y1_border, x_3rd_4th, y1_border)


        c.restoreState()

for i, upper_left, upper_right, bottom_left, bottom_right, card_name in \
        zip(
            tarot_cards.index,
            tarot_cards["a"],
            tarot_cards["b"],
            tarot_cards["c"],
            tarot_cards["d"],
            tarot_cards["e"]
        ):
    # card_name = card_name.upper()
    print(f"{upper_left} {card_name} {upper_right}\n{bottom_left}      {bottom_right}\n \n")


    c.setFillColor(B_COLOR)
    c.rect(0, 0, WIDTH, HEIGHT, fill=1)

    from PIL import Image

    im_path = f"my_images_dark/{i}.png"
    im = Image.open(im_path)
    img_width, img_height = im.size
    scaled_img_width = (img_width/img_height) * HEIGHT
    c.drawImage(im_path, WIDTH/2.0 - scaled_img_width/2.0, 0, height=HEIGHT, width=scaled_img_width, preserveAspectRatio=True)

    c.setFillColor(F_COLOR)
    FONT_NAME = "UnifrakturMaguntia"
    FONT_SIZE = 17
    c.setFont(FONT_NAME, FONT_SIZE)

    style_card_name = ParagraphStyle('card-name', fontName=FONT_NAME, fontSize=FONT_SIZE, textColor=F_COLOR)
    p = Paragraph(card_name, style=style_card_name)
    text_width, text_height = p.wrapOn(c, 111111111, 11111111)
    # p.drawOn(c, WIDTH - text_width/2.0, HEIGHT - CORNER_SQUARE_SIDE/2.0 - CORNER_BORDER - text_height/2.0)
    c.setFillColor(FADE_COLOR)
    c.drawCentredString(WIDTH/2.0, CORNER_SQUARE_SIDE/2.0 + CORNER_BORDER - text_height/2.0, card_name)

    draw_corner(c, CORNER_BORDER, CORNER_BORDER, CORNER_SQUARE_SIDE+CORNER_BORDER, CORNER_SQUARE_SIDE+CORNER_BORDER, bottom_left)
    draw_corner(c, WIDTH-CORNER_SQUARE_SIDE-CORNER_BORDER, CORNER_BORDER, WIDTH-CORNER_BORDER, CORNER_SQUARE_SIDE+CORNER_BORDER, bottom_right, True)

    draw_corner(c, CORNER_BORDER, HEIGHT-CORNER_SQUARE_SIDE-CORNER_BORDER, CORNER_SQUARE_SIDE+CORNER_BORDER, HEIGHT-CORNER_BORDER, upper_left)
    draw_corner(c, WIDTH-CORNER_SQUARE_SIDE-CORNER_BORDER, HEIGHT-CORNER_SQUARE_SIDE-CORNER_BORDER, WIDTH-CORNER_BORDER, HEIGHT-CORNER_BORDER, upper_right)

    c.showPage()


c.save()

