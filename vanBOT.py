# -*- coding: utf-8 -*-
"""
Created on Wed May  5 14:28:54 2021

@author: caldwell
"""

from generateurs import degrade, etoiles, lsysteme, pastel, planete, text, voronoi
import random
import time
from tqdm import trange
from os import mkdir
import numpy as np


## Parametres

taille = (1920, 1080)

## Art
ART = """
 _   _            ______  _____ _____
| | | |           | ___ \|  _  |_   _|
| | | | __ _ _ __ | |_/ /| | | | | |
| | | |/ _` | '_ \| ___ \| | | | | |
\ \_/ / (_| | | | | |_/ /\ \_/ / | |
 \___/ \__,_|_| |_\____/  \___/  \_/

"""

## Les generateurs de fonds et de sujets.
# Un fond est une image qui sera utilsé en arière-plan, alors
# que le sujet le sera au premier plan.
FONDS = [degrade, pastel, voronoi, text, etoiles]
SUJETS = [lsysteme, planete, etoiles, voronoi, None]


## Fonctions pour assiter à l'interface utilisateur --------------------------
def demander_choix(liste_choix):
    """
    Facilite le fait de demander à l'utilisateur de choisir entre plusieurs
    questions.

    liste_choix: liste (de chaines) des differents choix à afficher
    """
    liste = list(enumerate(liste_choix))
    for i, c in liste:
        print(f"\t{i + 1}) {c}") # \t <=> caractère de tabulation

    print(f"Votre choix (nombre compris entre 1 et {len(liste_choix)}):")

    while True:
        choix = input(">> ")

        if not choix.isdigit():
            continue # pas un chiffre

        choix = int(choix)
        if 1 < choix > len(liste_choix):
            continue # pas dans les bornes

        break # si on atteind ce niveau là, le choix est valide

    return liste_choix[choix - 1]

def demander_ouinon():
    """
    Demande à l'utilisateur de repondre par oui ou par non.
    Si la reponse est affirmative, True est retourné, False sinon.
    """
    print("Votre choix (oui/non):")

    while True:
        choix = input(">> ")

        if choix in ("oui", "o", "yes", "y"):
            return True
        elif choix in ("non", "n", "no"):
            return False

## Fonctions en raport avec la seed ------------------------------------------
# Une graine aléatoire (aussi appelée germe aléatoire, ou tout simplement seed
# en anglai) est un nombre utilisé pour l'initialisation d'un générateur de
# nombres pseudo-aléatoires.
# Toute la suite de nombres aléatoires produits par le générateur découle de
# façon déterministe de la valeur de la graine. Par contre, deux graines
# différentes produiront des suites de nombres aléatoires complètement
# différentes les unes des autres.
def maj_seed(seed):
    """
    Met à jour la seed du générateur aléatoire.

    seed: nombre représentant la seed
    """
    random.seed(seed)

    if seed > 2**32: # limitation de numpy
        seed = random.randint(0, 2**32)
    np.random.seed(seed)

def texte_en_nombre(texte):
    """
    Converti du texte en un nombre.

    texte: le texte à convertir
    """
    val = ""
    for c in texte:
        val += str(ord(c))

    return int(val)

def demander_seed(premiere_fois=True):
    """
    Demande à l'utilisateur de rentrer une seed, ou bien la crée à partir de
    l'heure actuelle.

    premiere_fois: Si c'est la premiere fois qu'on à demandé à l'utilisateur
                   une seed. Utilisé pour ne pas repeter deux fois les mêmes
                   informations.
    """
    if not premiere_fois:
        print("Veillez indiquer la seed:")

    seed = input(">> ")

    # pas de seed donné, on prend l'heure actuele
    if not seed:
        return time.time_ns()

    # l'utilisateur à rentré une seed
    if seed.isdigit(): # dans le cas ou c'est un nombre
        return int(seed)
    else:
        return texte_en_nombre(seed) # dans le cas contraire

# Fonctions pour la génération d'images --------------------------------------
def generer_image(taille, seed, generateurs=None, print_=True):
    """
    Génére une image avec des paramètres et des méthodes aléatoires.

    taille: les dimentions de l'image
    seed: la seed
    generateurs: les generateurs d'images a utiliser (optionel)
    print_: Si on doit afficher l'état de l'avancement de la création de
            l'image dans la console. Utilisé pour ne pas polluer la console
            lorsqu'on crée plusieurs images à la suite.
    """
    maj_seed(seed)

    if generateurs is None:
        gen_fond = random.choice(FONDS)
        gen_sujet = random.choice(SUJETS)
    else:
        gen_fond, gen_sujet = generateurs

    # Génération du fond de l'image -----------------------
    if print_:
        print("Génération du fond...", flush=True)
    if not print_ and gen_fond == pastel:
        fond = gen_fond.generer_fond(taille, nobar=True)
    else:
        fond = gen_fond.generer_fond(taille)

    # Génération du sujet de l'image ----------------------
    # réinitialisation de la seed pour obtenir des résultats
    # consitents lorsqu'on change la taille de l'image
    maj_seed(seed)
    if print_:
        print("Génération du sujet...")
    if gen_sujet is not None:
        # cas particulier, le diagrame voronoi prend toute l'image lorsqu'il
        # est un sujet
        if gen_sujet == voronoi:
            taille_sujet = taille
        else:
            taille_sujet = min(taille)

        sujet = gen_sujet.generer_sujet(taille_sujet)

        if taille_sujet == taille:
            pos = (0, 0)
        else:
            # on centre le sujet
            millieu = (taille[0] / 2, taille[1] / 2)
            pos = (
                round(millieu[0] - taille_sujet / 2),
                round(millieu[1] - taille_sujet / 2)
                )

        # collage du sujet sur le fond
        fond.paste(sujet, pos, sujet)

    return fond

def aff_sauv_img(img, seed):
    """
    Affiche et sauvergarde l'image générée.
    """
    nom = f"img_{seed}.png"

    print("Sauvegarde...")
    image.show()
    image.save(nom)
    print(f"Fini! L'image se trouve dans le même dossier que ce programe et se nomme {nom}")
    print("Elle à également été ouverte.")
    print("")


## Programe principal --------------------------------------------------------
print(ART)
print("Bienvenue sur VanBOT!")
print("")

while True:
    # Menu principal ------------------------------------------
    print("Menu principal:")
    menu = (
            "Changer la taille des images",
            "Genérer une image à partir d'une seed",
            "Genérer une image en choisisant les générateurs",
            "Genérer plusieurs images",
            "Quitter VanBOT"
            )
    choix_menu = demander_choix(menu)

    # Changement de la taille des images ----------------------
    if choix_menu == menu[0]:
        print("Veillez preciser les dimentions des images sous cette forme \"largeur/hauteur\":")

        while True:
            dim = input(">> ")

            if "/" not in dim: # pas de separateur / donc invalide
                continue

            n_taille = []
            for d in dim.split("/"):
                if d.isdigit():
                    n_taille.append(int(d))

            # dans le cas ou une des dimentions n'est pas un nombre valide,
            # il n'est pas ajouté à la liste, donc le meilleur moyen de
            # vérifier que l'utilisateur a rentré correctement une largeur et
            # une hauteur est de verifier la longueur de la liste n_taille
            if len(n_taille) != 2:
                continue

            taille = tuple(n_taille)
            break

        print(f"Entendu! Les images feront desomais cette taille: {taille}")
        print("")

    # Génération d'une image avec une seed -----------------------------------
    elif choix_menu == menu[1]:
        print(
              "Veuillez indiquer une seed. Une seed peut être soit un nombre, soit du "
              "texte qui sera converti en un nombre. Une seed permet de retrouver une "
              "image avec une generation similaire. Vous pouvez ne rien mettre, dans "
              "ce cas la seed sera déterminée en fonction de l'heure actuelle."
              )
        seed = demander_seed()
        while True:
            print("")
            print(f"Seed: {seed}")
            print("")

            image = generer_image(taille, seed)
            aff_sauv_img(image, seed)

            print("Voulez-vous créer une autre image ?")
            if not demander_ouinon():
                print("Ok, retour au menu.")
                print("")
                break
            print("")
            seed = demander_seed(False)

    # Generation d'une image avec fond et sujet personalisé ------------------
    elif choix_menu == menu[2]:
        while True:
            print("Veuillez choisir le générateur à utiliser pour le fond:")
            # Ici, on fabrique des dictionaires pour pouvoir facilement établir
            # une relation entre le nom du générateur et le générateur lui même
            gens_fond = {gen.__name__.split(".")[-1]:gen for gen in FONDS}
            nom_fond = demander_choix([g for g in gens_fond])
            gen_fond = gens_fond[nom_fond]

            print("Veuillez maintenant choisir le générateur à utiliser pour le sujet:")
            # Même chose ici, sauf que on dois prendre en compte le None qui
            # est dans la liste SUJETS (qui represente le fait de ne pas
            # générer de sujet)
            gens_sujet = {(gen.__name__.split(".")[-1] if gen else "Ne pas générer un sujet"):gen for gen in SUJETS}
            nom_sujet = demander_choix([g for g in gens_sujet])
            gen_sujet = gens_sujet[nom_sujet]

            print(f"Ok, génération d'une image en utilisant le fond \"{nom_fond}\" et le sujet \"{nom_sujet}\".")

            seed = time.time_ns()

            print("")
            print(f"Seed: {seed}")
            print("")

            image = generer_image(taille, seed, (gen_fond, gen_sujet))
            aff_sauv_img(image, seed)

            print("Voulez-vous créer une autre image ?")
            if not demander_ouinon():
                print("Ok, retour au menu.")
                print("")
                break

    # Génération de plusieurs images -----------------------------------------
    elif choix_menu == menu[3]:
        print("Combien d'images souhaitez-vous générer ?")

        # on essaye d'optenir un nombre valide
        while True:
            nb = input(">> ")

            if nb.isdigit():
                nb = int(nb)
                break

        print(f"Génération de {nb} images en cours...", flush=True)

        # création du dossier dans lequel seront stockée toutes les images
        # générées
        dossier = f"batch_{int(time.time())}"
        mkdir(dossier)

        for i in trange(nb):
            seed = time.time_ns()
            image = generer_image(taille, seed, print_=False)
            image.save(f"{dossier}/img_{i}_{seed}.png")

        print(f"Fini! Les images se trouvent toutes dans le dosier {dossier}")
        print("")

    # Fin du programe, adios! ------------------------------------------------
    else:
        print("Vous quittez VanBOT, adios!")
        break
