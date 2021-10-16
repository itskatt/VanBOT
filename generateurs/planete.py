# -*- coding: utf-8 -*-
"""
Created on Wed May 12 15:27:24 2021

@author: caldwell

source et inspiration: https://github.com/erdavids/Single-Planet/blob/master/Single_Planet.pyde
"""

from PIL import Image, ImageDraw
from colorsys import hsv_to_rgb
import random
    

def gen_coul():
    """
    Genere une couleur aleatoire.
    """
    h, s, v = (random.random(), random.uniform(0.9, 1), random.uniform(0.9, 1))
    return tuple([round(x) * 255 for x in hsv_to_rgb(h, s, v)])
    

def generer_sujet(taille):
    """
    Genere une planète avec anneaux.
    """
    # couleur de la planete
    couleur = gen_coul()

    # rayon de la planete a generer
    taille_planete = taille / 6.5
    
    # largeur et hauteur des anneaux de la planete
    larg_anneau = random.randint(round(taille_planete / 4), round(taille_planete / 2))
    haut_anneau = random.randint(round(taille_planete * 1.2), round(taille_planete * 1.4))


    img = Image.new("RGBA", (taille, taille))
    draw = ImageDraw.Draw(img)
    
    millieu = (round(taille / 2), round(taille / 2))
    
    # la planète
    draw.ellipse(
        [
            (millieu[0] - taille_planete, millieu[1] - taille_planete),
            (millieu[0] + taille_planete, millieu[1] + taille_planete)
            ], couleur, outline="black", width=round(taille_planete / 11.5)
        )
    
    # les anneaux
    for i in range(random.randint(3, 6)):
        draw.ellipse(
            [
                (millieu[0] - larg_anneau - i * 12, millieu[1] - haut_anneau - i * 30),
                (millieu[0] + larg_anneau + i * 12, millieu[1] + haut_anneau + i * 30)
                ], outline="black", width=round(taille_planete / 13.5)
            )
        
    # on recouvre les anneaux quand ils vont derriere la planète
    draw.chord([
                (
                    millieu[0] - taille_planete + round(taille_planete / 12.5),
                    millieu[1] - taille_planete + round(taille_planete / 12.5)
                    ),
                (
                    millieu[0] + taille_planete - round(taille_planete / 12.5),
                    millieu[1] + taille_planete - round(taille_planete / 12.5)
                    )
            ], 90, 270, couleur
        )

    return img.rotate(random.randint(0, 359), Image.BICUBIC)

if __name__ == "__main__":
    img = generer_sujet(1000)
    img.show()
