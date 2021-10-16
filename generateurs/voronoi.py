# -*- coding: utf-8 -*-
"""
Created on Wed May  5 19:25:08 2021

@author: rapha

source et inspiration:
https://www.generativehut.com/post/robots-and-generative-art-and-python-oh-my
"""

import random
import numpy as np
from scipy.spatial import Voronoi
import matplotlib.pyplot as plt
from matplotlib.collections import LineCollection
from PIL import Image


def gen_couls():
    """
    Genere deux couleurs oposée.
    """
    rgb1 = (random.random(), random.random(), random.random())
    rgb2 = tuple([1 - x for x in rgb1])
    return rgb1, rgb2


def generer_voronoi(taille, est_fond=True):
    """
    Genere notre diagrame de voronoi.
    
    taille: la taille de l'image
    est_fond: si cette valeure est False, le fond sera transparent
    """
    width, height = taille
    # conversion de pixels en pouces
    width, height = round(width / 70), round(height / 70)

    ## Paramètres -------------------------------------------------------
    # nombre de points a placer sur le diagrame (200)
    num_points = 200

    # pourcentage de polygones a appliquer l'effet des lignes (0.5)
    percent_to_fill = random.uniform(0.25, 0.6)

    # nombre de ligne dans les polygones (5)
    n_fill_lines = random.randint(3, 6)

    # taille min du polygone (dans les polygones) le plus petit (0.1)
    min_scalar = random.uniform(0.1, 0.4)
    
    # les couleurs (figure, fond)
    couls = gen_couls()
    
    # epaiseur du trait (3)
    ep_trait = min(taille) * 3 / 1000
    
    # anti crenelage (recommandé)
    aalias = True
    
    ## ------------------------------------------------------------------

    # tailles x et y
    x_bounds = np.array([0, width], dtype=object)
    y_bounds = np.array([0, height], dtype=object)

    x_buffer, y_buffer = 1, 1

    x_plot = x_bounds + np.array([x_buffer, -x_buffer], dtype=object)
    y_plot = y_bounds + np.array([y_buffer, -y_buffer], dtype=object)

    # on place des points aleatoirement
    x = np.random.uniform(*x_bounds, size=num_points).reshape((num_points, 1))
    y = np.random.uniform(*y_bounds, size=num_points).reshape((num_points, 1))
    pts = np.hstack([x, y])

    # on les relie grace au diagrame de Voronoi
    vor = Voronoi(pts)
    verts = vor.vertices
    shapes_ind = vor.regions

    # on filtre les polygones invalides (trop petit, impossibles,...), puis
    # on les ferme (ajout d'un coté)
    shapes_ind = [s + s[0:1] for s in shapes_ind if len(s) > 0 and -1 not in s]
    shapes = [verts[s] for s in shapes_ind]

    # on choisi au hazard des polygones...
    n_shapes_to_fill = round(percent_to_fill * len(shapes))
    shapes_to_fill = np.random.choice(np.array(shapes, dtype=object), size=n_shapes_to_fill, replace=False)

    fill = []
    # ...et on leurs ajoute l'effet des lignes
    for s in shapes_to_fill:
        center = np.mean(s, axis=0)
        for scaler in np.linspace(min_scalar, 1, num=n_fill_lines, endpoint=False):
            scaled = scaler * (s - center) + center
            fill.append(scaled)

    # taille et aspect du graphique
    fig, ax = plt.subplots(figsize=(width, height))
    ax.set_aspect("auto")

    # on enleve les lignes des abscices/ordonées
    plt.grid(False)
    plt.axis("off")

    # pour tenter de supprimer les espaces blancs autours du graphe
    # https://stackoverflow.com/a/27227718
    plt.gca().set_axis_off()
    plt.subplots_adjust(top=1, bottom=0, right=1, left=0, hspace=0, wspace=0)
    plt.margins(0, 0)
    plt.gca().xaxis.set_major_locator(plt.NullLocator())
    plt.gca().yaxis.set_major_locator(plt.NullLocator())

    # tracage du graphe...
    ax.set_xlim(*x_plot)
    ax.set_ylim(*y_plot)
    lc = LineCollection(shapes + fill, ep_trait, couls[0], aalias)
    ax.add_collection(lc)

    # si le diagrame est utilisé comme un fond, son fond sera une couleur opaque
    if est_fond:
        fig.patch.set_color(couls[1])
    else:
        # dans le cas contraire le fond est transparent
        fig.patch.set_alpha(0)

    fig.canvas.draw()

    return fig

def generer_fond(taille):
    """
    Genere le diagrame mais pour être utilisé en fond.
    """
    fig = generer_voronoi(taille, True)
    
    img = Image.frombytes("RGB", fig.canvas.get_width_height(), fig.canvas.tostring_rgb())
    
    return img

def generer_sujet(taille):
    """
    Genere le diagrame mais avec un fond transparent.
    """
    fig = generer_voronoi(taille, False)
    
    img = Image.frombytes("RGB", fig.canvas.get_width_height(), fig.canvas.tostring_rgb())
    
    # mise en place de la transparence
    imgt = img.copy().convert("RGBA")
    
    # on remplace les pixels blanc par des pixels transparents manuelement
    # c'est peut être pas la façon la plus rapide, mais ça marche
    data = img.getdata()
    datat = []
    for pix in data:
        if pix == (255, 255, 255):
            datat.append((0, 0, 0, 0))
        else:
            datat.append(pix)

    imgt.putdata(datat)
    
    return imgt

if __name__ == "__main__":
    # img = generer_sujet((1000, 1000))
    img = generer_fond((1000, 1000))
    img.show("e.png")
