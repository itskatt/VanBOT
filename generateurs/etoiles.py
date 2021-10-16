# -*- coding: utf-8 -*-
"""
Created on Wed May 26 11:07:27 2021

@author: rapha
aide pour les maths derière le traçage des étoiles:
    https://www.programmersought.com/article/74144516966/
"""

from PIL import Image, ImageDraw
import random
from colorsys import hsv_to_rgb
import math


def gen_coul():
    """
    Genere une couleur aléatoire vibrante.
    """
    h, s, v = (random.random(), random.uniform(0.9, 1), random.uniform(0.9, 1))
    return tuple([round(x * 255) for x in hsv_to_rgb(h, s, v)])

def gen_coul2():
    """
    Genere une couleur aléatoire adapté pour un ciel nocturne.
    """
    h, s, v = (random.uniform(226 / 360, 250 / 360), 1, random.uniform(0.2, 0.22))
    return tuple([round(x * 255) for x in hsv_to_rgb(h, s, v)])


def generer_sujet(taille):
    """
    Génére une étoile.
    """
    img = Image.new("RGBA", (taille, taille))
    draw = ImageDraw.Draw(img)
    
    # la couleur
    couleur = gen_coul()

    # nombre de sommets de l'etoile
    sommets = 5

    # l'angle entre les branches de l'etoile
    angle = 360 / sommets

    # centre de l'etoile
    centre = taille / 2

    # les cercles pour tracer l'etoile
    grand = taille / 2
    petit = grand / random.uniform(2, 3)

    coords = []
    # determination des points (voir aide pour explication detaillée avec images)
    for i in range(sommets):
        # coordonées des points sur le grand
        coords.append((
            centre + math.cos(angle * i / 180 * math.pi) * grand,
            centre + -math.sin(angle * i / 180 * math.pi) * grand
            ))

        # coordonées des points sur le petit cercle
        coords.append((
            centre + math.cos((angle / 2 + angle * i) / 180 * math.pi) * petit,
            centre + -math.sin((angle / 2 + angle * i) / 180 * math.pi) * petit
            ))


    draw.polygon(coords, couleur, "black")

    img = img.rotate(random.randint(0, 359))

    return img


def generer_fond(taille):
    """
    Génére un fond rempli d'étoiles.
    """
    larg, haut = taille
    
    # la couleur du fond
    coul_fond = gen_coul2()
    
    # nombre d'étoiles a générer
    nb_etoiles = max(40, round(min(taille) * 50 / 1000))
    
    # la taille des étoiles
    taille_etoile = min(taille) / 10
    
    # la variation de la taille des étoiles
    var = taille_etoile / 2
    
    # facteur d'écartement des étoiles (pour limiter le fait qu'elles
    # s'empilent les unes sur les autres)
    div = 2

    img = Image.new("RGBA", taille, coul_fond)
    
    # choix des coordonées des étoiles
    pos_x = random.sample(range(round(larg / div)), nb_etoiles)
    pos_y = random.sample(range(round(haut / div)), nb_etoiles)
    
    # génération et collage des étoiles
    for x, y in zip(pos_x, pos_y):
        etoile = generer_sujet(random.randint(taille_etoile - var, taille_etoile + var))
        img.paste(etoile, (round(x * div), round(y * div)), etoile)

    return img

if __name__ == "__main__":
    # img = generer_sujet(1000)
    img = generer_fond((1500, 1000))
    img.show("e.png")
