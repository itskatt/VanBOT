# -*- coding: utf-8 -*-
"""
Created on Fri May 21 17:49:44 2021

@author: rapha
"""

from PIL import Image, ImageDraw, ImageFont, ImageFilter
import random


TEXT = """\
We're no strangers to love
You know the rules and so do I
A full commitment's what I'm thinking of
You wouldn't get this from any other guy
I just wanna tell you how I'm feeling
Gotta make you understand
Never gonna give you up
Never gonna let you down
Never gonna run around and desert you
Never gonna make you cry
Never gonna say goodbye
Never gonna tell a lie and hurt you
We've known each other for so long
Your heart's been aching but you're too shy to say it
Inside we both know what's been going on
We know the game and we're gonna play it
And if you ask me how I'm feeling
Don't tell me you're too blind to see
Never gonna give you up
Never gonna let you down
Never gonna run around and desert you
Never gonna make you cry
Never gonna say goodbye
Never gonna tell a lie and hurt you
Never gonna give you up
Never gonna let you down
Never gonna run around and desert you
Never gonna make you cry
Never gonna say goodbye
Never gonna tell a lie and hurt you
Never gonna give, never gonna give
(Give you up)
We've known each other for so long
Your heart's been aching but you're too shy to say it
Inside we both know what's been going on
We know the game and we're gonna play it
I just wanna tell you how I'm feeling
Gotta make you understand
Never gonna give you up
Never gonna let you down
Never gonna run around and desert you
Never gonna make you cry
Never gonna say goodbye
Never gonna tell a lie and hurt you
Never gonna give you up
Never gonna let you down
Never gonna run around and desert you
Never gonna make you cry
Never gonna say goodbye
Never gonna tell a lie and hurt you
Never gonna give you up
Never gonna let you down
Never gonna run around and desert you
Never gonna make you cry
Never gonna say goodbye"""


def gen_couls():
    """
    Genere deux couleurs oposée
    """
    rgb1 = (random.randint(0, 255), random.randint(0, 255), random.randint(0, 255))
    rgb2 = tuple([255 - x for x in rgb1])
    return rgb1, rgb2


def generer_fond(taille):
    """
    Genere un fond avec du texte appliqué aleatoirement en décoration.
    """
    l, h = taille

    # les couleurs de l'image
    couleurs = gen_couls()

    # si on doit appliquer un filtre sur l'image
    filtre = random.choice((True, False))

    # les filtres à appliquer sur l'image
    filtres = [
        ImageFilter.GaussianBlur(random.randint(1, 3)),
        ImageFilter.CONTOUR(),
        ImageFilter.DETAIL(),
        ImageFilter.EDGE_ENHANCE(),
        ImageFilter.EMBOSS(),
        ImageFilter.FIND_EDGES(),
        ImageFilter.SHARPEN(),
        ImageFilter.SMOOTH()
        ]

    # les polices a utiliser
    polices = [
        "impact",
        "comic",
        "arial",
        "calibri",
        "consola",
        "corbel",
        "Gabriola",
        ]

    img = Image.new("RGB", taille, couleurs[0])
    draw = ImageDraw.Draw(img)
    police = ImageFont.truetype(random.choice(polices), round(50 * l / 1000))

    # arrangement du texte
    text = TEXT.splitlines() * 3
    random.shuffle(text)
    text = "\n".join(text)

    ## Transfome ça: -----------------------
    #   blablablabla
    #   blablabla
    #   blablablabla
    #
    ## En ça:
    #   blablablabla blablabla...  
    n_text = ""
    i = 0
    for c in text:
        # passage a la ligne suivante
        if i >= 70:
            i = 0
            n_text += "\n"

        if c == "\n": # on remplace les sauts à la ligne par des espaces
            n_text += " "
        else:
            n_text += c

        i += 1
    # --------------------------------------

    # les styles à appiliquer au texte
    styles = [
        n_text.upper, # BLABLA
        n_text.lower, # blabla
        n_text.title, # Bla Bla
        n_text.swapcase # bLA bLA
        ]
    style = random.choice(styles)

    draw.multiline_text((0, 0), style(), couleurs[1], police)

    if filtre:
        img = img.filter(random.choice(filtres))

    return img

if __name__ == "__main__":
    img = generer_fond((1000, 1000))
    img.show()