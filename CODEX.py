"""
# 0. CODEX.py

"""
import pygments as pygments
from reportlab.lib import pygments2xpre
from reportlab.lib.enums import TA_JUSTIFY
from reportlab.lib.styles import ParagraphStyle
from reportlab.lib.utils import getStringIO
from reportlab.platypus import XPreformatted

"""
# 0.1 Intro

This book is the printout of the Python 3.0 program that
Creates a PDF file that contains text
of this program on the dark (odd) sheets with
comments extracted onto light (even) sheets.

Also, it generates this README.md file.

"""
import re

""" # Z. Used libraries"""
import math
import random

from reportlab.lib.colors import black, white, Color, yellow
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfgen.canvas import Canvas
from reportlab.lib.units import inch, cm
from reportlab.pdfbase.ttfonts import TTFont

FONT_NAME = "AnglicanText"
pdfmetrics.registerFont(TTFont(FONT_NAME, 'AnglicanText.ttf'))


def int_to_roman(input):
    """ # Z. Convert an integer to a Roman numeral. """

    if not isinstance(input, type(1)):
        raise TypeError("expected integer, got %s" % type(input))
    if not 0 < input < 4000:
        raise ValueError("Argument must be between 1 and 4000")
    ints = (1000, 900, 500, 400, 100, 90, 50, 40, 10, 9, 5, 4, 1)
    nums = ('M', 'CM', 'D', 'CD', 'C', 'XC', 'L', 'XL', 'X', 'IX', 'V', 'IV', 'I')
    result = []
    for i in range(len(ints)):
        count = int(input / ints[i])
        result.append(nums[i] * count)
        input -= ints[i] * count
    return ''.join(result)


def primes(n):
    """ # Z. Returns  a list of primes < n """
    sieve = [True] * n
    for i in range(3, int(n ** 0.5) + 1, 2):
        if sieve[i]:
            sieve[i * i::2 * i] = [False] * ((n - i * i - 1) // (2 * i) + 1)
    return [2] + [i for i in range(3, n, 2) if sieve[i]]


def ROMAN_NUMBERS_GENERATOR(R, only_length=4):
    for X in R:
        result = int_to_roman(X)
        if len(result) == only_length:
            yield result


def DRAW_PAGE_BACKGROUND(c, w, h, corners_font_size, roman_number, background_color, stroke_colors,
                         corner_decoration_alpha):
    def GET_CORNER_DECORATION_COLOR():
        return Color(random.uniform(0.8, 1),
                     random.uniform(0.8, 1),
                     random.uniform(0.8, 1),
                     corner_decoration_alpha)

    c.saveState()
    c.setFillColor(background_color)
    c.rect(0, 0, w * cm, h * cm, fill=1)
    c.setStrokeColor(stroke_colors[0])

    c.line(0, 0, w * cm, h * cm)
    c.line(w * cm, 0, 0, h * cm)

    K = corners_font_size * 23.8

    for x in range(0, int(w * cm), 2):
        c.setLineWidth(w * cm / K / math.sqrt(abs(w * cm / 2 - x)))

        c.setStrokeColor(stroke_colors[1])
        c.line(x, 0, x, h * cm)

    for y in range(0, int(h * cm), 2):
        c.setLineWidth(h * cm / K * (w / h) / math.sqrt(abs(h * cm / 2 - y)))
        c.line(0, y, w * cm, y)

    c.restoreState()

    MARGIN_WIDTH = 0.1 * cm
    MARGIN_HEIGHT = 0.03 * cm

    c.setFont(FONT_NAME, corners_font_size)

    c.saveState()
    c.translate(MARGIN_WIDTH, MARGIN_HEIGHT)
    angle = -math.atan(w / h / 2)
    c.rotate(math.degrees(angle))

    c.setFillColor(GET_CORNER_DECORATION_COLOR())
    c.drawCentredString(0, 0, f"{roman_number[0]}")
    c.restoreState()

    c.saveState()
    c.translate(w * cm - MARGIN_WIDTH, MARGIN_HEIGHT)
    c.rotate(-math.degrees(angle))

    c.setFillColor(GET_CORNER_DECORATION_COLOR())
    c.drawCentredString(0, 0, f"{roman_number[1]}")
    c.restoreState()

    c.saveState()
    c.translate(w * cm - MARGIN_WIDTH, h * cm - MARGIN_HEIGHT)
    c.rotate(math.degrees(angle) + 180)

    c.setFillColor(GET_CORNER_DECORATION_COLOR())
    c.drawCentredString(0, 0, f"{roman_number[2]}")
    c.restoreState()

    c.saveState()
    c.translate(MARGIN_WIDTH, h * cm - MARGIN_HEIGHT)
    c.rotate(180 - math.degrees(angle))

    c.setFillColor(GET_CORNER_DECORATION_COLOR())
    c.drawCentredString(0, 0, f"{roman_number[3]}")
    c.restoreState()


def SECTIONS_UNSORTED(filename):
    """Before reading, file with path `filename` should be opened. `open` returns a *file handle* f"""
    f = open(filename, "r")
    """read whole file to a string"""
    source_code = f.read()
    """after reading file should be closed"""
    f.close()

    COMMENT_DEMARKATOR = '\"\"\"'
    sections = []
    current_section = {"code": "", "comment": ""}
    currently_inside_of_comment = False
    last_comment_demarkator_index = 0
    for i in range(len(source_code)):
        if source_code[i:i + len(COMMENT_DEMARKATOR)] == COMMENT_DEMARKATOR:
            if currently_inside_of_comment:
                current_section["comment"] = source_code[
                                             last_comment_demarkator_index + len(COMMENT_DEMARKATOR):i].lstrip()
            else:
                current_section["code"] = source_code[
                                          last_comment_demarkator_index + len(COMMENT_DEMARKATOR):i].lstrip()
                sections.append(current_section)
                current_section = {}

            currently_inside_of_comment = not currently_inside_of_comment

            last_comment_demarkator_index = i

    return sections


def CHAPTERS_GENERATOR(filename):
    sections = SECTIONS_UNSORTED(filename)

    chapters = []
    current_chapter = None
    for section in sections:
        if section["comment"].startswith("#"):
            if current_chapter is not None:
                chapters.append(current_chapter)
            current_chapter = {"title": "", "sections": []}
            current_chapter["title"] = re.findall(r'#+\s*([^\n]*)',section["comment"] )[0] ## fixme cut ## and end of line
            current_chapter["index"] = re.findall(r'#+\s*(\w+\.?\w*)', section["comment"])[0]
        if current_chapter is not None:
            current_chapter["sections"].append(section)

    chapters = sorted(chapters, key=lambda item: item["index"])
    return chapters

def CHAPTER_LINE_BY_LINE_GENERATOR(chapter):
    for section in chapter["sections"]:
        for comment_line, code_line in zip(section["comment"].split("/n"),section["code"].split("/n")):
            yield comment_line, code_line

"""
## 0.2 `MAIN` function call
"""

def MAIN():
    """Lets print a filename of this Python script into console. Note `f` before opening quote of *string* - it allows
    using variables between handlebars `{` `}` within string"""
    print(f"... {__file__} is started")

    CHAPTERS = CHAPTERS_GENERATOR(__file__)

    for chapter in CHAPTERS:
        print(chapter["title"].upper())
        for section in chapter["sections"]:
            print(section["comment"])

    """
    # 1. Options
    """

    """
    Note how 'argparse' is imported. It's comes with standard library of Python. 
    You can install 3rd party packages with 
    
       pip install package-name
    
    command in a Command Line of your OS.
    """
    import argparse

    """
    Program './CODEX.Py' supports following options:
    """

    parser = argparse.ArgumentParser(description='This program prints out itself as a PDF book')
    """* '--width 1024' - of the output page"""
    parser.add_argument('--width', action="store", dest="width", type=float, default=21.0)
    """* '--height 768' - of the output page"""
    parser.add_argument('--height', action="store", dest="height", type=float, default=29.7)

    """
         * '--translate RU' - use Google Translate to translate the book
         * '--use-codex-ai' - make a call to CodexAI to get a Python code for extraction of the CAPS WORDS from the book into the list of terms
        """

    parser.add_argument('--font_size_min', action="store", dest="font_size_min", type=int, default=30)
    parser.add_argument('--font_size_max', action="store", dest="font_size_max", type=int, default=6660)
    parser.add_argument('--prime_font_sizes_only', dest='prime_font_sizes_only', action='store_true', default=True)

    """
    There are other options. You can see whole list by running

        ./CODEX.py --help
    """

    """Here we call method `.parse_args()` on object `parser` and assign result to the variable `ARGS`"""
    ARGS = parser.parse_args()

    """Lets create a variable and assign a *String* containing output file name to it"""
    OUTPUT_FILE_NAME = "BOOK.pdf"
    """Lets assign 2 variables with names `WIDTH` and `HEIGHT` the contents of the members `.width` and `.height` of 
    vairable `ARGS`"""
    (WIDTH, HEIGHT) = (ARGS.width, ARGS.height)
    """Same goes for `FONT_SIZE_MIN` and `FONT_SIZE_MAX`"""
    (FONT_SIZE_MIN, FONT_SIZE_MAX) = (ARGS.font_size_min, ARGS.font_size_max)
    """And variable `PRIME_FONT_SIZES_ONLY`"""
    PRIME_FONT_SIZES_ONLY = ARGS.prime_font_sizes_only
    """Create (PDF)[https://ru.wikipedia.org/wiki/Portable_Document_Format] file with given file name and
    page dimensions"""
    c = Canvas(OUTPUT_FILE_NAME, pagesize=(WIDTH * cm, HEIGHT * cm))

    """Assign range from `FONT_SIZE_MIN` to `FONT_SIZE_MAX` to variable `FONT_SIZES`"""
    FONT_SIZES = range(FONT_SIZE_MIN, FONT_SIZE_MAX)

    """If option `--prime_font_sizes_only` is selected, filter out
    non-[Prime](https://en.wikipedia.org/wiki/Prime_number) font sizes"""
    if PRIME_FONT_SIZES_ONLY:
        """Getting all Prime numbers"""
        ALL_PRIMES = primes(FONT_SIZE_MAX)
        """For each `font_size` in `FONT_SIZES`, if font_size is in `ALL_PRIMES` - include it into *list* that 
        is assigned to `FONT_SIZES` after whole iteration"""
        FONT_SIZES = [font_size for font_size in FONT_SIZES if font_size in ALL_PRIMES]

    """Print `FONT_SIZES` variable into console"""
    print(f"Sizes of the corner decoration font: {FONT_SIZES}pt")

    """Get all Roman numbers from 1 to 4000 that contain exactly 4 letters"""
    ROMAN_NUMBERS = list(iter(ROMAN_NUMBERS_GENERATOR(range(1, 4000))))

    """Lets start with first page"""
    PAGE = 1

    current_chapter_lines = CHAPTER_LINE_BY_LINE_GENERATOR(CHAPTERS[0])
    CHAPTERS = CHAPTERS[1:]

    """For each `FONT_SIZE` in `FONT_SIZES` limited by length of `ROMAN_NUMBERS`, in reversed order"""
    for FONT_SIZE in reversed(FONT_SIZES[:len(ROMAN_NUMBERS) - 1]):
        """Even and odd pages should contain same `ROMAN_NUMBER`. `ROMAN_NUMBERS[5]` returns 6th element of 
        `ROMAN_NUMBERS` *list*"""
        ROMAN_NUMBER = ROMAN_NUMBERS[PAGE]

        """Draw background for odd page - page with comments"""
        DRAW_PAGE_BACKGROUND(c, WIDTH, HEIGHT, FONT_SIZE, ROMAN_NUMBER,
                             background_color=white,
                             stroke_colors=[Color(1, 0.3, 0.4, 0.1), Color(1, 0.3, 0.4, 0.4)],
                             corner_decoration_alpha=0.666)


        c.showPage()
        """Draw background for even page - page with code"""
        DRAW_PAGE_BACKGROUND(c, WIDTH, HEIGHT, FONT_SIZE, ROMAN_NUMBER,
                             background_color=black,
                             stroke_colors=[Color(1, 1, 1, 0.01), Color(0.6, 0.6, 0.6, 0.07)],
                             corner_decoration_alpha=0.018)


        c.showPage()

        PAGE += 1
        print(f"  -  {ROMAN_NUMBER}")
    c.save()

    # Use a breakpoint in the code line below to debug your script.
    print(f'SAVING : {OUTPUT_FILE_NAME}')  # Press Ctrl+F8 to toggle the breakpoint.


"""
## 0.1 `MAIN` function call
"""

"""`__name__` is a magical *variable*". It's equal to *string* `"__main__"` if this file is launched as a program 
(as oppose to being used as a library from different program)"""
if __name__ == '__main__':
    """Lets call `MAIN` function"""
    MAIN()
