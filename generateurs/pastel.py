# -*- coding: utf-8 -*-
"""
Created on Wed May  5 14:32:00 2021

@author: caldwell

source et inspiration: https://github.com/erdavids/WatercolorClouds
"""

import cairo
import math
from random import randint, uniform, choice
from PIL import Image
from tqdm import trange


def octagon(x_orig, y_orig, side):
    """
    Crée un octogone.
    
    x/y_orig: coordonées d'origines
    side: longueur des cotés
    """
    x = x_orig
    y = y_orig
    d = side / math.sqrt(2)

    oct = []

    oct.append((x, y))

    x += side
    oct.append((x, y))

    x += d
    y += d
    oct.append((x, y))

    y += side
    oct.append((x, y))

    x -= d
    y += d
    oct.append((x, y))

    x -= side
    oct.append((x, y))

    x -= d
    y -= d
    oct.append((x, y))

    y -= side
    oct.append((x, y))

    x += d
    y -= d
    oct.append((x, y))

    return oct

def deform(shape, iterations, variance):
    """
    Deforme un polygone.
    
    shape: le plygone a deformer
    iterations: nombres d'iterations
    variance: intensité des deformations
    """
    for i in range(iterations):
        for j in range(len(shape) - 1, 0, -1):
            midpoint = (
                (shape[j-1][0] + shape[j][0])/2 + uniform(-variance, variance),
                (shape[j-1][1] + shape[j][1])/2 + uniform(-variance, variance)
                )
            shape.insert(j, midpoint)
    return shape


def gen_couleurs(nb):
    """
    Genere un certain nombre de couleurs aleatoires.
    """
    colors = []
    for i in range(nb):
        colors.append((uniform(0.4, 0.75), uniform(0.4, 0.75), uniform(0.4, 0.75)))
    return colors


def generer_fond(taille, nobar=False):
    """
    Genere notre pastel.
    
    taille: taille de l'image
    nobar: si on doit ne pas afficher de barre de progression pendant la
           création de l'image
    """
    # explication detaillée des paramètres:
    # https://tylerxhobbs.com/essays/2017/a-generative-approach-to-simulating-watercolor-paints
    ## Parametres -----------------------------------------------
    width, height = taille
    
    # deformation initiale (120)
    initial = 120
    # variance des deformations suivantes (50)
    deviation = 50

    # deformations avant que le polygone est ajouté (deformation brute des cotés, prend du temps) (1 ?)
    basedeforms = randint(1, 3)
    # deformations après qu'il soit ajouté (effet flou/pastel) (3 ?)
    finaldeforms = randint(2, 4)

    # nombre min max de polygones
    minshapes = round(min(taille) * 20 / 1100)
    maxshapes = round(min(taille) * 25 / 1100)
    
    # taille des polygones
    taille_polygones = randint(
        round(min(taille) * 100 / 1000),
        round(min(taille) * 300 / 1000)
        )

    # transparance des polygones (0.05)
    shapealpha = uniform(0.03, 0.06)
    
    # nombre de couleurs (15)
    nb_coul = randint(14, 16)

    ## ----------------------------------------------------------
    
    colors = gen_couleurs(nb_coul)

    # preparatiuon de la surface
    ims = cairo.ImageSurface(cairo.FORMAT_ARGB32, width, height)
    cr = cairo.Context(ims)

    cr.set_source_rgb(.9, .9, .9)
    cr.rectangle(0, 0, width, height)
    cr.fill()

    cr.set_line_width(1)

    # si on dois afficher la barre de progression
    if nobar:
        r = range
    else:
        r = trange

    for p in r(-int(height * 0.2), int(height * 1.2), 60):
        # mise en place de la couleur
        cr.set_source_rgba(choice(colors)[0], choice(colors)[1], choice(colors)[2], shapealpha)

        shape = octagon(randint(-100, width + 100), p, taille_polygones)
        baseshape = deform(shape, basedeforms, initial)

        # empilement des polygones
        for j in range(randint(minshapes, maxshapes)):
            newshape = baseshape.copy()
            layer = deform(newshape, finaldeforms, deviation)

            # traçage des polygones
            for i in range(len(layer)):
                cr.line_to(layer[i][0], layer[i][1])
            cr.fill()

    # conversion de l'image pour PIL
    # https://www.cairographics.org/cookbook/pythoncairopil/
    img = Image.frombuffer("RGBA", (width, height), ims.get_data(), "raw", "RGBA", 0, 1)

    return img

if __name__ == "__main__":
    taille = (1000, 1000)
    img = generer_fond(taille)
    img.show()