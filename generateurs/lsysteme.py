# -*- coding: utf-8 -*-
"""
Created on Thu May 13 19:55:17 2021

@author: rapha
"""

from PIL import Image, ImageDraw, ImageFilter
import math
import random
from random import randint, uniform


def gen_couls():
    """
    Genere deux couleurs oposée.
    """
    rgb1 = (random.randint(0, 255), random.randint(0, 255), random.randint(0, 255))
    rgb2 = tuple([255 - x for x in rgb1])
    return rgb1, rgb2


class Pile():
    """
    Une Pile FIFO.
    """
    def __init__(self):
        self.pile = []

    def vide(self):
        return len(self.pile) == 0

    def empile(self, elem):
        self.pile.append(elem)

    def depile(self):
        return self.pile.pop()


class Generateur:
    """
    Le générateur L-Système.
    
    img: l'image sur laquelle tracer les l-systèmes
    couleurs: les couleurs a utiliser (2-tuple)
    epaisseur: epaisseur des traits
    variance_angle/taille: intensité des variation
    """
    def __init__(self, img, couleurs, epaisseur, variance_angle, variance_taille):
        self.img = img
        self.draw = ImageDraw.Draw(img)

        self.couls = couleurs
        self.ep = epaisseur
        self.var_angle = variance_angle
        self.var_taille = variance_taille

    def trait(self, debut, long, angle, coul, ep = 1):
        """
        Trace un trait partant d'un point avec un angle.
        
        debut: origine du trait
        long: longeur du trait
        angle: angle du trait (0* correspond à un trait vertical |)
        coul: couleur du trait
        ep: epaisseur du trait
        """
        x, y = debut
        angle -= 90 # ajustement, comme ça on pointe vers le haut
        dx = math.cos(math.radians(-angle)) * long
        dy = math.sin(math.radians(-angle)) * long

        fin = (round(x + dx), round(y - dy))
        self.draw.line([(x, y), fin], coul, round(ep))

        return fin

    def point(self, pos, taille, coul):
        """
        Trace un point.
        
        pos: position du point
        taille: rayon du point
        coul: couleur du point
        """
        self.draw.ellipse([
            (pos[0] - taille, pos[1] - taille),
            (pos[0] + taille, pos[1] + taille)
            ], coul)
        
    def gen_regle(self, taille, niv=0):
        """
        Genere une regle aleatoire.
        
        taille: longeur de la regle en caracteres
        niv: niveau de recusivité (utilisé en interne)
        """
        regles = ["F", "X", "+", "-", "[]"]
    
        regle = ["F"]
        for n in range(taille):
            invalide = True
            while invalide:
                regle_a = random.choice(regles)

                if regle_a == "[]" and taille - n >= 3 and niv < 2:
                    imbrique = self.gen_regle(math.floor((taille - n) / 4), niv + 1)
                    regle.append(f"[{imbrique}]")

                elif regle_a == "X" and regle[-1] == "X":
                    invalide = True
                elif regle_a == "+" and regle[-1] == "-":
                    invalide = True
                elif regle_a == "-" and regle[-1] == "+":
                    invalide  = True
                else:
                    invalide = False
            regle.append(regle_a)
        return "".join(regle)

    def lsysteme(self, pos, regle, gen_taille, niveau_max, hauteur, angle):
        """
        Trace une figure l-systeme.
        
        pos: position de depart
        regle: la regle a utiliser pour tracer le l-systeme
        gen_taille: taille de la regle aleatoire
        niveau_max: niveau maximal de detail
        hauteur: hauteur du l-systeme
        angle: angle entre les branches
        """
        p = Pile()
        angle_actuel = 0
        pos_actuel = pos

        def lsys(regle, niveau, taille):
            """
            Fonction recursive en interne qui trace le l-systeme.
            """
            nonlocal angle_actuel, pos_actuel

            if niveau == 0:
                # on trace un trait avec les variations de taille et d'angle
                pos_actuel = self.trait(pos_actuel,
                    uniform(taille - self.var_taille, taille + self.var_taille),
                    randint(angle_actuel - self.var_angle, angle_actuel + self.var_angle),
                    self.couls[0], self.ep
                    )

            else:
                for r in regle:
                    if r == "F":
                        lsys(regle, niveau - 1, taille / 3)
                    elif r == "X":
                        self.point(pos_actuel, math.sqrt(taille / 10), self.couls[1])
                    elif r == "+":
                        angle_actuel -= angle
                    elif r == "-":
                        angle_actuel += angle
                    elif r == "[":
                        p.empile((pos_actuel, angle_actuel))
                    elif r == "]":
                        if not p.vide():
                            pos_actuel, angle_actuel = p.depile()
                        else:
                            raise SyntaxError("Il manque un crochet ouvert ([)")
                    else:
                        raise SyntaxError(f"Caractere invalide ({r})")

        if regle is None:
            regle = self.gen_regle(gen_taille)
        lsys(regle, niveau_max, hauteur)


def generer_sujet(taille):
    """
    Genere un l-systeme.
    """
    ## Paramètres -----------------------------------------------------

    # couleurs de l'arbre
    couleurs = gen_couls()

    # niveau de detail
    detail = random.randint(2, 4)

    # epaisseur des branches
    epaisseur = taille * 6 / 1000

    # angle des branches
    angle = random.randint(10, 90)

    # hauteur de l'arbre
    hauteur = taille * 0.9

    # variations
    variance_taille = taille * 0.02
    variance_angle = 7

    # La regle a utiliser
    # regle = "F[+FX]F[-FX]FX"
    
    # si on genere une regle aleatoire
    regle = None
    
    # la taille de la regle aleatoire, si on l'utilise
    gen_taille = random.randint(10, 15)

    ## ----------------------------------------------------------------

    img = Image.new("RGBA", (taille, taille))
    gen = Generateur(img, couleurs, epaisseur, variance_angle, variance_taille)
    og = (taille / 2, taille / 2)

    gen.lsysteme(og, regle, gen_taille, detail, hauteur, angle)

    return img.filter(ImageFilter.GaussianBlur(1)) # flou pour limiter le crenenelage


if __name__ == "__main__":
    img = generer_sujet(1000)
    img.show()
