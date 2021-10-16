# -*- coding: utf-8 -*-
"""
Created on Wed May  5 14:28:54 2021

@author: caldwell
"""

from PIL import Image, ImageDraw, ImageFilter
import random
from colorsys import hsv_to_rgb, rgb_to_hsv
import math

## Générateurs de couleur -------------------------------------------

def gen_couleurs_rd(nb):
    """
    Génère des couleurs totalement aléatoires.
    """
    couls = []
    for _ in range(nb):
        couls.append((
            random.randint(0, 255),
            random.randint(0, 255),
            random.randint(0, 255)))

    return couls

def gen_couleurs_claire(nb):
    """
    Génère des couleurs alétoires plus claires.
    """
    couls = []
    for _ in range(nb):
        coul = [
            random.randint(0, 255),
            random.randint(150, 255),
            random.randint(150, 255)]
        random.shuffle(coul)
        couls.append(tuple(coul))

    return couls

def gen_couleurs_hue(nb):
    """
    Génère des couleurs avec une teinte aléatoire.
    """
    couls = []
    for _ in range(nb):
        h, s, v = (random.random(), 1, 1)
        rgb = tuple([round(x * 255) for x in hsv_to_rgb(h, s, v)])
        couls.append(rgb)

    return couls

## "Methodes" de trie -----------------------------------------------
# voir: https://www.alanzucconi.com/2015/09/30/colour-sorting/

def lum(rgb):
    """
    Renvoie l'indice de luminance d'une couleur.
    """
    r, g, b = rgb
    return math.sqrt(0.241 * r + 0.691 * g + 0.068 * b )

def lum2(rgb):
    """
    Renvoie l'indice de luminance d'une couleur en utilisant une methode
    plus affinée.
    """
    r, g, b = rgb
    return math.sqrt(0.299 * (r**2) + 0.587 * (g**2) + 0.114 * (b**2))

def teinte(rgb):
    """
    Renvoie une couleur sous sa forme HSV, ce qui nous donne sa teinte
    pour le tri.
    """
    r, g, b = rgb
    return rgb_to_hsv(r, g, b)

## Parametres de generation ------------------------------------------

def gen_param():
    """
    Génère les aléatoirement les parametres de génération de l'image.
    """
    param = {}

    # nombre de couleurs à generer (3-6)
    param["nb_coul"] = random.randint(3, 6)

    # le generateur de couleurs à utiliser
    param["gen"] = random.choice([
        gen_couleurs_rd,
        gen_couleurs_claire,
        gen_couleurs_hue
        ])

    # si on trie les couleurs
    param["trie"] = random.choice([True, False])

    # la méthode pour le trie
    param["meth"] = random.choice([
        lum, lum2, teinte
        ])

    # rotation du degradé (d = gauche-droite, h = bas-haut,...)
    param["rot"] = random.choice(["dh", "db", "gh", "gb"])

    # si on applique un flou sur l'image (recomandé)
    param["flou"] = True
    # l'intensité du flou (100)
    param["int"] = random.randint(90, 110)

    return param


def generer_fond(taille):
    """
    Génère le degradé.
    """
    largeur, hauteur = taille
    param = gen_param()

    img = Image.new("RGBA", (largeur, hauteur))
    draw = ImageDraw.Draw(img)
    couleurs = param["gen"](param["nb_coul"])

    if param["trie"]:
        couleurs.sort(key=param["meth"], reverse=("h" in param["rot"]))

    # orientation du degradé
    if "d" in param["rot"]:
        # gauche -> droite
        for i, c in enumerate(couleurs):
            long = round(largeur / param["nb_coul"])
            draw.rectangle(
                [(long * i, 0), (long * (i + 1), hauteur)], c
                )
    else:
        # haut -> bas
        for i, c in enumerate(couleurs):
            long = round(hauteur / param["nb_coul"])
            draw.rectangle(
                [(0, long * i), (largeur, long * (i + 1))], c
                )

    # application du flou
    if param["flou"]:
        img = img.filter(ImageFilter.GaussianBlur(param["int"] * max(taille) / 500))

    return img


if __name__ == "__main__":
    taille = (1000, 1000)
    img = generer_fond(taille)
    img.show()
