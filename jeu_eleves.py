#!/usr/bin/env python3
# -*- coding: utf-8 -*-

#Projet créer par Yassine  et Matthieu  (Groupe 22 - NSI 2020/2021)
#https://www.youtube.com/watch?v=VNbo1AGqKrI

############ Importations
# Ceci permet d'importer tout depuis graphique_jeu.py

from graphique_jeu import *
from random import *
from copy import deepcopy #Note, rajouté par nous. Nous permet de copier une liste sans la synchronisé avec la liste copié.
from tkinter import * #Nous permet de créer un petit menu et aussi d'écrire et lire le fichier scorenormal.txt et scorehermine.txt.
from sauvegarde import * #Importe le fichier sauvegarde.py, un fichier qui s'occupe de tout ce qui est sauvegarde/écriture des fichier scorenormal.txt et scorehermine.txt.
from temps_jeu import attend #Nous permet de mettre un temps d'attente entre deux action. Tkinter ne supporte pas la fonction Time de python. Pour pouvoir utilisé Time, on a du créer un fichier unique à cette utilisation.
############ Fonctions pour le jeu

score=[0]
modele=0
sens=0


def assemble(phrase):
    """
    Au moment de demander le nom du joueur pour le High Score, le menu 'input' accepte qu'on y place une phrase.
    Le problème est que le programme, en lisant le fichier contenant le High Score, considère les espaces comme une fin/début de tableau.
    Ainsi: "J'aime les carottes" (du texte), se transforme en "[[J'aime],[les],[Carottes]]" (un tableau).
    Note: Impossible de stocker un simple tableau... ainsi le High Score, au lieu d'être un "[[Joueur 1],[Score 1],[Joueur 2],[Score 2]]" doit être
    "Joueur1 Score1 Joueur1 Score2" (donc, notre phrase remplacera "Score1" par "les" et "Joueur2" en "carottes", ce qui pause problème...

    Ce programme permet que si on écrit dans le 'input' une phrase, les espaces sont remplacé par "_".
    Donc: "J'aime les carottes" devient "J'aime_les_carottes", pour éviter le problème cité si dessus.

    Entrée: texte (str) donné par le joueur via le 'input'.
    Sorti: Le même texte (str), mais filtré.
    """
    nouvelle_phrase="" #Valeur d'initialisation, pour accueillir le texte "filtré".
    if phrase=="": #Si rien n'a été écrit dans le 'input' avant d'avoir envoyé le texte.
        phrase="Unknow" #Ecrit "Unknow". Puisque sinon, la valeur ne sera pas marqué dans le fichier, et tout sera décalé... (avoir un score de valeur "Joueur 2", c'est bizarre)
    for i in(phrase): #Parcour la phrase.
        if i!=" ": #Si il remarque que la valeur (i) n'est pas un espace.
            nouvelle_phrase=nouvelle_phrase+i #Rajoute la valeur au reste de la phrase (ce qui est normal).
        else: #Mais si c'est un espace.
            nouvelle_phrase=nouvelle_phrase+"_" #Marque "_" au lieu d'un espace.
    return(nouvelle_phrase) #Renvoi la nouvelle phrase ("J'aime les carottes" -> "J'aime_les_carottes")



def valide(grille, bloc):
    coordybloc=-1
    """
    Entrée:  grille -> La grille de jeu contenant les collisions. [list]
            bloc -> L'ensemble de pixels (ce qui forme le bloc). [list]

    Sorti:  False -> Le bloc ne peut pas entré dans cette emplacement, rejette le bloc [booléen]
            True -> Le bloc peut entré dans cette emplacement, valide le bloc [booléen]

    Principe:
        Test si en plaçant le bloc, celui-si ne va pas "manger" un bloc déjà ancré sur la grille
        (vérifie si il n'y a pas déjà un pixel ancré sur la grille au coordonné où l'un des pixel de bloc veut se placé (système de collisions).

    """

    #Initialisation
    soustabgrille=len(grille) #soustabgrille est le nombre de tableau contenant la matrice grille.
    soustabvaleurgrille=len(grille[0]) #soustabvaleurgrille est le nombre de valeurs contenuent dans le 1er tableau de la matrice grille.

    for soustab in(bloc): #Sélectionne un tableau de la matrice bloc (le tableau sélectionné se nommera "soustab"

        #Initialisation
        coordx=-1 #Valeur d'initialisation - Contiendra la 1ère valeur du tableau (correspondant à la position du pixel dans l'axe Y)
        coordy=-1 #Valeur d'initialisation - Contiendra la 2ème valeur du tableau (correspondant à la position du pixel dans l'axe X)

        #Sélection de la valeur à vérifié (Y puis X)
        for valeur in(soustab): #Sélectionne une valeur du tableau "soustab". A noté que les coordonnés d'un pixel sont sous la forme [Y,X] (/!\ ET NON [X,Y] /!\)
            if coordy==-1: #Si coordy contient encore sa valeur d'initialisation (donc si on est à la première valeur du tableau)
                coordy=valeur #coordy s'assigne la valeur correspondant à la position du pixel dans l'axe Y
            else:
                coordx=valeur #coordx s'assigne la valeur correspondant à la position du pixel dans l'axe X

        #Etape de Vérification
        #Les "print("false X")" permettent via la console, de savoir d'où vient l'erreur (pourquoi le jeu à rejeté le bloc).

        #1. Si le pixel (bloc) dépasse la limite de la grille du côté bas
        if coordy>soustabgrille-1: #Si la valeur Y du bloc est supérieur a la valeur maximum en axe Y que supporte la grille.
            print("false 1") #aide au développement
            return False

        #2. Si le pixel (bloc) dépasse la limite de la grille du côté droit
        if coordx>soustabvaleurgrille-1: #Si la valeur X du bloc est supérieur a la valeur maximum en axe X que supporte la grille.
            print("false 2") #aide au développement.
            return False

        #3. Si l'emplacement du pixel (bloc) correspond dans la grille à un pixel déjà placé.
        if grille[coordy][coordx]==1: #Test à l'aide des coordonnés du pixel à placé, si la case où sera placé ce pixel n'est pas déjà occupé.
            print("false 3") #aide au développement.
            return(False)
        #4. Si le pixel (bloc) dépasse la limite de la grille du côté gauche (coordx<0) ou haut (coordy<0).
        if coordx<0 or coordy<0: #Si l'axe X est inférieur à la valeur minimale de l'axe X que supporte la grille ou si l'axe Y est inférieur à la valeur minimale de l'axe Y que supporte la grille, renvoi False. if bloc[coordx][0]<0 or bloc[coordx][1]<0
            print("false 4",coordx) #aide au développement.
            return(False)

        #Si le pixel sélectionné n'a pas été confronté à l'un des problèmes si dessus, passe au prochain.

    return(True) #Si aucun des pixels du blocont été confronté au problème, valide le bloc.

def deplacebloc(grille, bloc, direction, hermine, grille_coloré):

    """
    Entrée:
        grille -> La grille de jeu contenant les collisions. [list]
        bloc -> L'ensemble de pixels (ce qui forme le bloc). [list]
        direction -> La direction de là où veut aller le bloc (Haut, Bas, Gauche, Droite) [str]
        hermine -> L'ensemble de pixels (ce qui forme le bloc mobile nommé Hermine). [list]
        grille_coloré -> La grille de jeu qui sera affiché à l'écran, avec ses couleurs. [list]

    Sorti:
        bloccopie -> Le bloc déplacé [list]
        copie -> Le bloc d'origine, celui reçu en entrée (dont il n'y a eu aucun changement) [list]

    Principe:
        En fonction de la demande du joueur (Haut, Gauche...), déplace un clône du bloc en fonction de la demande, et test le bloc
        si il ne rentrera pas en "concurrence" avec un bloc déjà placé sur la grille..

    """

    bloccopie=deepcopy(bloc) #Copie la matrice bloc dans la variable bloccopie.
    numéro_tableau=-1 #Valeur d'initialisation - La valeur de la variable est le numéro du tableau dans la matrice (si numéro_tableau==0 -> tableau 1)

    if hermine !=[0,0]: #Si on est dans le mode Tetris Hermine
        ancre_hermine(grille, grille_coloré, hermine,1) #On ancre temporairement Hermine

    #1. Si le joueur veut déplacé le bloc vers le haut.
    if direction=="H":
        for y in(bloccopie): #Sélectionne un tableau (qui sera nommé y) dans la matrice bloccopie
            numéro_tableau=numéro_tableau+1 #Rajoute 1 au numéro de tableau précédent (pour que numéro_tableau correspond au tableau à analysé)
            bloccopie[numéro_tableau][0]=(bloccopie[numéro_tableau][0])-1 #Enlève 1 a l'axe Y du bloc (pour le déplacé d'1 pixel vers le haut)

    #2. Si le joueur veut déplacé le bloc vers la droite.
    if direction=="D":
        for y in(bloccopie): #Sélectionne un tableau (qui sera nommé y) dans la matrice bloccopie
            numéro_tableau=numéro_tableau+1 #Rajoute 1 au numéro de tableau précédent (pour que numéro_tableau correspond au tableau à analysé)
            bloccopie[numéro_tableau][1]=(bloccopie[numéro_tableau][1])+1 #Rajoute 1 a l'axe X du bloc (pour le déplacé d'1 pixel vers la droite)

    #3. Si le joueur veut déplacé le bloc vers la gauche.
    if direction=="G":
        for y in(bloccopie): #Sélectionne un tableau (qui sera nommé y) dans la matrice bloccopie
            numéro_tableau=numéro_tableau+1 #Rajoute 1 au numéro de tableau précédent (pour que numéro_tableau correspond au tableau à analysé)
            bloccopie[numéro_tableau][1]=(bloccopie[numéro_tableau][1])-1 #Enlève 1 a l'axe X du bloc (pour le déplacé d'1 pixel vers la gauche)

    #1. Si le joueur veut déplacé le bloc vers le bas.
    if direction=="B":
        for y in(bloccopie): #Sélectionne un tableau (qui sera nommé y) dans la matrice bloccopie
            numéro_tableau=numéro_tableau+1 #Rajoute 1 au numéro de tableau précédent (pour que numéro_tableau correspond au tableau à analysé)
            bloccopie[numéro_tableau][0]=(bloccopie[numéro_tableau][0])+1 #Rajoute 1 a l'axe Y du bloc (pour le déplacé d'1 pixel vers le bas)

    #Le bloc Hermine se fait dé-ancré
    if hermine !=[0,0]: #Si on est dans le mode Hermine Tetris
        ancre_hermine(grille, grille_coloré, hermine,0) #Dé-ancre Hermine

    if valide(grille,bloccopie)==True: #Si le bloc déplacé peut-être placé
        return(bloccopie) #Renvoi le bloc déplacé
    else: #Sinon, renvoi le bloc d'origine (sans tenir compte des déplacements demandé par l'utilisateur)
        return(bloc)

def nouveau_bloc(largeur):
    milieu=int(largeur/2)
    """
    Entrée:
        largeur -> Largeur de la grille [int]

    Sortie: "return bloc, type_de_bloc, rotation" (exemple: return b,"b","0")
        bloc -> Le nouveau bloc à utilisé (Renvoi le contenu de la variable b ou cl ou cc ou cf...) [list]
        type_de_bloc -> L'identité du bloc (si c'est un bloc T (b), carré (cc)...[str]
        rotation -> Le sens de rotation du bloc ("0" signifie par défaut, celle donné à l'origine) [int]

    Principe:
        Renvoi un bloc choisit au hasard.
        "milileu" (issus de largeur, en entré)  permet d'affiché le bloc au milieu haut de la grille.
    """

    #Stockage des blocs:
    b=[[0,1+milieu],[1,0+milieu],[1,1+milieu],[2,1+milieu]]     #BLOC T #Format: [coordonnée Y, coordonnée X] (même chose pour les blocs suivants...)
    cl=[[0,0+milieu],[1,0+milieu],[2,0+milieu],[3,0+milieu]]    # BLOC BARRE
    cc=[[0,0+milieu],[0,1+milieu],[1,0+milieu],[1,1+milieu]]    # BLOC CARREE
    cf=[[0,0+milieu],[1,0+milieu],[2,0+milieu],[2,1+milieu]]    # BLOC L
    cp=[[0,0+milieu]]                                           # Bloc .
    cz=[[0,0+milieu],[0,1+milieu],[1,1+milieu],[1,2+milieu]]    # Bloc Z
    cz2=[[1,0+milieu],[1,1+milieu],[0,1+milieu],[0,2+milieu]]   # Bloc Z à l'envers
    cf2=[[0,1+milieu],[1,1+milieu],[2,1+milieu],[2,0+milieu]]   #Bloc L à l'envers

    #Sélection d'un bloc de manière aléatoire.
    bloc_alea=(randint(0,7)) # Sélection un chiffre entre 0 et 7 compris.

    #Association du numéro tiré au bloc
    if bloc_alea==0: #SI LE NOMBRE CHOISIT EST 0, RENVOIE LE BLOC B (Forme T)
        return b,"b","0" #return bloc, type_de_bloc, rotation

    if bloc_alea==1: #SI LE NOMBRE CHOISIT EST 1, RENVOIE LE BLOC cl (forme Barre)
        return cl,"cl","0"

    if bloc_alea==2: #SI LE NOMBRE CHOISIT EST 2, RENVOIE LE BLOC cc (forme Carré)
        return cc,"cc","0"

    if bloc_alea==3: #SI LE NOMBRE CHOISIT EST 3, RENVOIE LE BLOC cf (forme L)
        return cf,"cf","0"

    if bloc_alea==4: #SI LE NOMBRE CHOISIT EST 4, RENVOIE LE BLOC cp (forme Point)
        return cp,"cp","0"

    if bloc_alea==5: #SI LE NOMBRE CHOISIT EST 5, RENVOIE LE BLOC Z (forme Z)
        return cz,"cz","0"

    if bloc_alea==6: #SI LE NOMBRE CHOISIT EST 6, RENVOIE LE BLOC Z à l'envers (forme Z2)
        return cz2,"cz2","0"

    if bloc_alea==7: #SI LE NOMBRE CHOISIT EST 7, RENVOIE LE BLOC cf à l'envers (forme Z2)
        return cf2,"cf2","0"



def cree_grille(largeur:int,hauteur:int):

    """
    Entrée:
        largeur -> La largeur de la grille à créer [int]
        hauteur -> La hauteur de la grille à créer [int]

    Renvoi/Sortie:
        grille -> La grille créer sous forme de matrice. Avec le nombre *hauteur* de tableau dans la matrice, avec à l'intérieur le nombre *largeur* de 0.

    Principe:
        Créer une grille (matrice) en fonction de la taille hauteur*largeur demandé par l'utilisateur.

    """
    #Erreur affiché si il n'a pas reçus en entrée des nombres:
    assert type(largeur) == int, "largeur n'est pas un entier ! (cree_grille)"
    assert type(hauteur) == int,  "hauteur n'est pas un entier ! (cree_grille)"

    #Valeurs minimum (il est donc impossible de créer une grille de 1*1, puisqu'il est est impossible de "joué" avec une tel grille !
    if largeur<3: #Si largeur est inférieur à 3, la largeur sera 3
        largeur=3
    if hauteur<4: #Si la hauteur est inférieur à 3, la largeur sera 3
        hauteur=4

    grille=[[0]*largeur for i in range(hauteur)] #Créer la grille.

    return grille




def rotation(grille, bloc, modele, sens):
    print("rotation",bloc, modele, sens)
    """
    Entrée:
        grille -> La grille de jeu contenant les collisions. [list]
        bloc -> L'ensemble de pixels (ce qui forme le bloc).  [list]
        modele -> Le type de bloc (Carré, T, L...) [str]
        sens -> sens de rotation [int]

    Renvoie:
        bloc (le bloc reçus en entrée, si il est impossible de faire la rotation) OU bloc1 (le bloc avec la rotation effectué) [list]
        modele -> Le type de bloc [str]
        sens -> Le nouveau sens de rotation (si la rotation a été effectué, sinon, le sens de rotation reçu en entrée) [int]

    Principe:
        Fait tourné le bloc, en vérifiant toute fois si cette rotation en possible (si le bloc après ça ne va pas dépassé la grille,
        ne va pas rentré en concurrence avec un bloc déjà placé...).
    """
    #DISPOSITION:
    #    Si ce le type_de_bloc est X (bloc T, bloc L...):
    #       Si le sens actuelle est Y (Rotation d'origine (0), 1 rotation effectué (1), 2 rotation effectué (2)...):
    #           Alors tourne le bloc ou non.

    #REMARQUE: Les explications seront donné seulement pour le bloc "b" (bloc en forme de T), puisque c'est le même principe pour les blocs suivant...

    #Si c'est le bloc en forme de T qu'il faut tourner:
    if modele=="b": #Si c'est le bloc b
        if sens=="0": #Si il est dans le sens d'origine
            bloc1=[[bloc[0][0],bloc[0][1]],[bloc[1][0],bloc[1][1]],[bloc[2][0],bloc[2][1]],[bloc[3][0]-1,bloc[3][1]+1]] #Fait tourné le bloc (modifie la position de chaque pixels)
            if valide(grille,bloc1)==True: #Si le bloc une fois tourné, sera toujours valide dans la grille (ne la dépasse pas...).
                sens="1" #Redéfinie le nouveau sens (c'est désormais le sens 1, et plus celui d'origine)
                return bloc1,modele,sens #Renvoi le bloc tourné
            else:
                return bloc,modele,sens #Renvoi le bloc non tourné
        if sens=="1": #Si il est dans le sens 1
            bloc1=[[bloc[0][0],bloc[0][1]],[bloc[1][0]+1,bloc[1][1]+1],[bloc[2][0],bloc[2][1]],[bloc[3][0],bloc[3][1]]] #Fait tourné le bloc (modifie la position de chaque pixels)
            if valide(grille,bloc1)==True: #Si le bloc une fois tourné, sera toujours valide dans la grille (ne la dépasse pas...).
                sens="2" #Redéfinie le nouveau sens (c'est désormais le sens 2, et plus le sens 1)
                return bloc1,modele,sens #Renvoi le bloc tourné
            else:
                return bloc,modele,sens #Renvoi le bloc non tourné

        if sens=="2": #Si il est dans le sens 2
            bloc1=[[bloc[0][0]+1,bloc[0][1]-1],[bloc[1][0],bloc[1][1]],[bloc[2][0],bloc[2][1]],[bloc[3][0],bloc[3][1]]] #Fait tourné le bloc (modifie la position de chaque pixels)
            if valide(grille,bloc1)==True: #Si le bloc une fois tourné, sera toujours valide dans la grille (ne la dépasse pas...).
                sens="3" #Redéfinie le nouveau sens (c'est désormais le sens 3, et plus le sens 2)
                return bloc1,modele,sens #Renvoi le bloc tourné
            else:
                return bloc,modele,sens #Renvoi le bloc non tourné
        if sens=="3": #Si il est dans le sens 3
            bloc1=[[bloc[0][0]-1,bloc[0][1]+1],[bloc[1][0]-1,bloc[1][1]-1],[bloc[2][0],bloc[2][1]],[bloc[3][0]+1,bloc[3][1]-1]] #Fait tourné le bloc (modifie la position de chaque pixels)
            if valide(grille,bloc1)==True: #Si le bloc une fois tourné, sera toujours valide dans la grille (ne la dépasse pas...).
                sens="0" #Redéfinie le nouveau sens (c'est désormais le sens 0 (celui d'origine), et plus le sens 3)
                return bloc1,modele,sens #Renvoi le bloc tourné
            else:
                return bloc,modele,sens #Renvoi le bloc non tourné

    if modele=="cl":
        if sens=="0":
            bloc1=[[bloc[0][0]+1,bloc[0][1]+1],[bloc[1][0],bloc[1][1]+2],[bloc[2][0]-1,bloc[2][1]],[bloc[3][0]-2,bloc[3][1]-1]]
            if valide(grille,bloc1)==True:
                sens="1"
                return bloc1,modele,sens
            else:
                return bloc,modele,sens

        if sens=="1":
            bloc1=[[bloc[0][0]-1,bloc[0][1]-1],[bloc[1][0],bloc[1][1]-2],[bloc[2][0]+1,bloc[2][1]],[bloc[3][0]+2,bloc[3][1]+1]]
            if valide(grille,bloc1)==True:
                sens="0"
                return bloc1,modele,sens
            else:
                return bloc,modele,sens

    if modele=="cc" or modele=="cp": #C'est un carré... Il est donc impossible de le faire tourné dans notre jeu Tetris, donc aucun changement à effectué.
        return bloc,modele,sens

    if modele=="cf":
        if sens=="0":
            bloc1=[[bloc[0][0],bloc[0][1]+2],[bloc[1][0],bloc[1][1]],[bloc[2][0]-1,bloc[2][1]+2],[bloc[3][0]-1,bloc[3][1]]]
            if valide(grille,bloc1)==True:
                sens="1"
                return bloc1,modele,sens
            else:
                return bloc,modele,sens
        if sens=="1":
            bloc1=[[bloc[0][0],bloc[0][1]-1],[bloc[1][0]-1,bloc[1][1]],[bloc[2][0],bloc[2][1]-1],[bloc[3][0]+1,bloc[3][1]]]
            if valide(grille,bloc1)==True:
                sens="2"
                return bloc1,modele,sens
            else:
                return bloc,modele,sens
        if sens=="2":
            bloc1=[[bloc[0][0]+1,bloc[0][1]],[bloc[1][0]+1,bloc[1][1]],[bloc[2][0]+1,bloc[2][1]-1],[bloc[3][0]-1,bloc[3][1]+1]]
            if valide(grille,bloc1)==True:
                sens="3"
                return bloc1,modele,sens
            else:
                return bloc,modele,sens
        if sens=="3":
            bloc1=[[bloc[0][0]-1,bloc[0][1]-1],[bloc[1][0],bloc[1][1]],[bloc[2][0],bloc[2][1]],[bloc[3][0]+1,bloc[3][1]-1]]
            if valide(grille,bloc1)==True:
                sens="0"
                return bloc1,modele,sens
            else:
                return bloc,modele,sens

    if modele=="cz":
        if sens=="0":
            bloc1=[[bloc[0][0]+1,bloc[0][1]],[bloc[1][0],bloc[1][1]],[bloc[2][0],bloc[2][1]],[bloc[3][0]+1,bloc[3][1]-2]]
            if valide(grille,bloc1)==True:
                sens="1"
                return bloc1,modele,sens
            else:
                return bloc,modele,sens
        if sens=="1":
            bloc1=[[bloc[0][0]-1,bloc[0][1]],[bloc[1][0],bloc[1][1]],[bloc[2][0],bloc[2][1]],[bloc[3][0]-1,bloc[3][1]+2]]
            if valide(grille,bloc1)==True:
                sens="0"
                return bloc1,modele,sens
            else:
                return bloc,modele,sens

    if modele=="cz2":
        if sens=="0":
            bloc1=[[bloc[0][0],bloc[0][1]],[bloc[1][0],bloc[1][1]],[bloc[2][0],bloc[2][1]-1],[bloc[3][0]+2,bloc[3][1]-1]]
            if valide(grille,bloc1)==True:
                sens="1"
                return bloc1,modele,sens
            else:
                return bloc,modele,sens
        if sens=="1":
            bloc1=[[bloc[0][0],bloc[0][1]],[bloc[1][0],bloc[1][1]],[bloc[2][0],bloc[2][1]+1],[bloc[3][0]-2,bloc[3][1]+1]]
            if valide(grille,bloc1)==True:
                sens="0"
                return bloc1,modele,sens
            else:
                return bloc,modele,sens

    if modele=="cf2":
        if sens=="0":
            bloc1=[[bloc[0][0],bloc[0][1]-1],[bloc[1][0],bloc[1][1]],[bloc[2][0]-1,bloc[2][1]+1],[bloc[3][0]-1,bloc[3][1]]]
            if valide(grille,bloc1)==True:
                sens="1"
                return bloc1,modele,sens
            else:
                return bloc,modele,sens
        if sens=="1":
            bloc1=[[bloc[0][0],bloc[0][1]],[bloc[1][0]+1,bloc[1][1]-1],[bloc[2][0]-1,bloc[2][1]-1],[bloc[3][0],bloc[3][1]]]
            if valide(grille,bloc1)==True:
                sens="2"
                return bloc1,modele,sens
            else:
                return bloc,modele,sens
        if sens=="2":
            bloc1=[[bloc[0][0],bloc[0][1]],[bloc[1][0]-2,bloc[1][1]+2],[bloc[2][0],bloc[2][1]],[bloc[3][0],bloc[3][1]+2]]
            if valide(grille,bloc1)==True:
                sens="3"
                return bloc1,modele,sens
            else:
                return bloc,modele,sens
        if sens=="3":
            bloc1=[[bloc[0][0],bloc[0][1]+1],[bloc[1][0]+1,bloc[1][1]-1],[bloc[2][0]+2,bloc[2][1]],[bloc[3][0]+1,bloc[3][1]-2]]
            if valide(grille,bloc1)==True:
                sens="0"
                return bloc1,modele,sens
            else:
                return bloc,modele,sens



def ancre_hermine(grille, grille_coloré, hermine, estancré):

    """
    Entrée:
        grille -> La grille de jeu contenant les collisions. [list]
        grille_coloré -> La grille de jeu qui sera affiché à l'écran, avec ses couleurs. [list]
        hermine -> L'ensemble de pixels (ce qui forme le bloc mobile nommé Hermine). [list]
        estancré -> Demande du jeu [int]

    Renvoi:
        rien

    Principe:
        En fonction de la demande du jeu, la fonction va ancré ou désancré le bloc mobile "Hermine".
        A certains moments, on a besoin que le jeu considère Hermine comme un bloc ancré.
        Par exemple, pour déterminé si avec la présence d'Hermine, une ligne devient pleine. (si oui, la partie se termine).
        Ou on a besoin de dé-ancré le bloc Hermine (pour qu'il redevient une entité mobile).
        Pour continuer notre exemple, cela serait une fois qu'on a terminé de vérifié si les lignes sont pleines ou non, et qu'on reprend le jeu;
        il faut donc qu'Hermine redevient mobile afin de le contrôlé.

    """

    coord_y_tab1=-1 #Valeur d'initialisation - Contiendra la 1ère valeur du tableau du 2ème tableau sélectionné (correspondant à la position du 2ème pixel dans l'axe Y)
    coord_x_tab1=-1 #Valeur d'initialisation - Contiendra la 2ème valeur du tableau du 2ème tableau sélectionné (correspondant à la position du 2ème pixel dans l'axe X)

    for tableau in hermine: #Sélectionne un tableau de la matrice Hermine
        memoire_coord_y=-1 #Valeur d'initialisation - Permet de gardé la valeur Y du premier tableau (premier pixel en partant du haut).

        for coordonné in tableau: #Sélectionne la valeur Y puis X du tableau sélectionné précédemment.

            #Ici, on s'occupe de la position Y (au total, le bloc en a 2, car les valeurs Y des 2 pixels sont différente).
            if memoire_coord_y==-1: #Si la valeur de memoire_coord_y est encore celle d'initialisation.
                memoire_coord_y=coordonné #On sauvegarde la valeur Y (la première valeur du tableau sélectionné) dans memoire_coord_y.
                if coord_y_tab1==-1: #Si la valeur de coord_y_tab1 est encore celle d'initialisation.
                    coord_y_tab1=coordonné #On sauvegarde la valeur Y (la première valeur du tableau sélectionné) dans coord_y_tab1.

            else:
                #Si il est demandé d'ancré le bloc Hermine:
                if coord_x_tab1!=-1 and estancré==1: #Si on arrive à la fin de la matrice, et qu'il est demandé qu'on ancre Hermine... Alors on ancre Hermine.
                    grille[coord_y_tab1][coord_x_tab1]=1 #Ancre sur la grille le premier pixel (en partant du haut)
                    grille_coloré[coord_y_tab1][coord_x_tab1]="hermine" #Ancre sur la grille_coloré le premier pixel (en partant du haut)
                    grille[memoire_coord_y][coordonné]=1 #Ancre sur la grille le deuxième pixel (en partant du haut)
                    grille_coloré[memoire_coord_y][coordonné]="hermine" #Ancre sur la grille_coloré le deuxième pixel (en partant du haut)
                    return

                #Si il est demandé de dé-ancré le bloc Hermine:
                if coord_x_tab1!=-1 and estancré==0: #Si on arrive à la fin de la matrice, et qu'il est demandé qu'on dé-ancre Hermine... Alors on dé-ancre Hermine.
                    grille[coord_y_tab1][coord_x_tab1]=0 #Dé-Ancre sur la grille le premier pixel (en partant du haut)
                    grille_coloré[coord_y_tab1][coord_x_tab1]=0 #Dé-ancre sur la grille_coloré le premier pixel (en partant du haut)
                    grille[memoire_coord_y][coordonné]=0 #Dé-Ancre sur la grille le deuxième pixel (en partant du haut)
                    grille_coloré[memoire_coord_y][coordonné]=0 #Dé-Ancre sur la grille_coloré le deuxième pixel (en partant du haut)
                    #print("nb_de_bloc",coord_y_tab1,coord_x_tab1)
                    return

                #Ici, on s'occupe de la position X (il y en a qu'une, car les deux pixels ont la même)
                if coord_x_tab1==-1: #Si cette variable a encore sans valeur d'initialisation (donc qu'on est au tableau 1).
                    coord_x_tab1=coordonné #Sauvegarde la valeur X du tableau dans coord_x_tab1.




def validation(grille, bloc, score, modele, grille_coloré, hermine):
    """
    Entrée:
        grille -> La grille de jeu contenant les collisions. [list]
        bloc -> L'ensemble de pixels (ce qui forme le bloc).  [list]
        score -> Le score du joueur avant modification (si il y en a) [int]
        grille_coloré -> La grille de jeu qui sera affiché à l'écran, avec ses couleurs. [list]
        hermine -> L'ensemble de pixels (ce qui forme le bloc mobile nommé Hermine). [list]

    Sortie:
        newbloc -> Un nouveau bloc a affiché sur la grille (vu que l'ancien à été ancré) [list]
        OU
        [[0,0]] -> Cela signifi que le jeu est terminé (le nouveau bloc ne peut pas apparaître normalement sur la grille, Game Over classique dans un Tetris) (on ne peut pas renvoyé un "False" ou autre qu'une liste, car le reste du jeu comprend que c'est un bloc qui est renvoyé, et pas autre chose !).

    Principe:
        Ancre sur la grille le bloc actuelle (tout en vérifiant, au cas où, que si on l'ancre, il ne va pas "manger" ou rentré en concurrence avec un bloc déjà ancré).

    """
    if valide(grille, bloc)==True: #Si on peut ancré le bloc
        for tableauu in(bloc): #Parcour les tableaux de la matrice bloc.
            nbvaleur=0 #VALEUR D'INITIALISATION - Garde la valeur Y du tableau sélectionné
            valeur1=0 #VALEUR D'INITIALISATION - Indique (si valeur1==1), que la valeur Y a été gardé par nbvaleur.
            for valeurr in(tableauu): #Parcour les valeurs du tableau tableauu
                if nbvaleur==0: #Si c'est encore la valeur d'initialisation (donc on est à la première valeur du tableau, soit la valeur Y)
                    valeur1=valeurr #Garde la valeur Y du tableau sélectionné
                    nbvaleur=1 #Indique que la valeur Y a été gardé.
                else:
                    grille[valeur1][valeurr]=1 #"valeurr" correspond a la position du pixel dans l'axe X, et valeur1 correspond a la position du pixel dans l'axe Y. Il ancre le pixel dans la grille.
                    grille_coloré[valeur1][valeurr]=modele #Parreil, mais il va ancré le type de bloc (modele) dans la grille_coloré.
        if hermine!=[0,0]: #Si la valeur hermine ne contient pas la valeur d'initialisation (si on est dans le mode Tetris Hermine):
            ancre_hermine(grille, grille_coloré, hermine,1) #Va ancrer Hermine par la fonction ancre_hermine.

        score[0]=score[0]+10 #Rajoute 10 points au score.

        newbloc=nouveau_bloc(len(grille[0])) #Invoque un nouveau bloc
        if valide(grille, newbloc[0])==False: #Vérifie si le nouveau bloc pourrait être placé, si c'est non:
            return ([[0,0]]) #Renvoi un bloc vide (le script supporte uniquement des blocs, renvoyer un "False" était impossible). Car le nouveau bloc ne peut apparaître dans la grille.
        if hermine !=[0,0]: #Va dé-ancrer hermine
            ancre_hermine(grille, grille_coloré, hermine,0)
        return(newbloc) #Renvoi le nouveau bloc, qui peut apparaître normalement dans la grille.



def reclassementtab(grille,largeur):

    """
    Entrée:
        grille -> La grille de jeu contenant les collisions. [list]
        largeur -> La largeur de la grille [int]

    Renvoie:
        rien

    Principe:
        Reclasse la grille en emmenant la ligne vide situé tout en bas de la grille au sommet de cette grille.
        Utilité: dans supprligne, on créer une nouvelle ligne vide, et elle apparais tout en bas. On doit donc la remonté pour
                 donner l'illusion que les blocs ont descendu.

    """

    for i in range(len(grille)): #Fait varier i dans "l'index" de la grille (si i==0 -> ligne 1, si i==1 -> ligne 2...).
        if i<len(grille)-1: #Si la ligne "sélectionné" n'est pas la dernière en partant du haut.
            grille[len(grille)-i-1]=list(grille[len(grille)-i-2]) #Copie la ligne en dessous sur la ligne au dessus.

            #Représentation de l'idée.
            #ligne 0 [0,1,1,1,0,0,0]
            #ligne 1 [1,0,0,0,0,0,0] --\ copie cette ligne
            #ligne 2 [1,0,0,0,0,0,0] <-/ et colle la ligne ici.
            #ligne 3 [0,1,0,1,0,1,0] (puisque la ligne 2 avait été juste avant copié et collé sur la ligne 3).
        else: #Si c'est la dernière ligne de la grille qui est actuellement "sélectionné" par i. Si il n'y avait pas "if i<len(grille)-1", cela signifierais que la dernière ligne serait copié et collé sur la première... Ce qui est inutile.
            grille[0]=[0]*largeur #On réinitialise la première ligne (puisque celle-si est en double avec la deuxième ligne)

def supprligne(grille,largeur,score,grille_coloré,hermine, continuer, texte):

    """
    Entrée:
        grille -> La grille de jeu contenant les collisions. [list]
        largeur -> Largeur de la grille [int]
        score -> Le score du joueur [int]
        grille_coloré -> La grille de jeu qui sera affiché à l'écran, avec ses couleurs. [list]
        hermine -> L'ensemble de pixels (ce qui forme le bloc mobile nommé Hermine). [list]
        continuer -> l'Etat du jeu
        texte -> le texte qui est affiché sur le côté du jeu

    Sortie:
        score -> Le score avec 100 points rajoutés
        hermine -> #le bloc Hermine
        continuer -> "None" Si Hermine a été éliminé (si un ou plusieurs pixels du blocs ont été supprimé )

    Principe:
        Si une (ou plusieurs) ligne est pleine de 1 dans la grille (si il n'y a plus aucun 0 sur celle-ci), supprime cette ligne, et en créer une nouvelle (et qui sera déplacé au sommer de la grille).
        Et (si on est dans le mode Tetris Hermine) s'il remarque que parmis les pixels supprimé, il y a ceux d'Hermine, renvoi un Game Over.

    """
    if hermine !=[0,0]: #Va ancrer hermine, si on est dans le mode Tetris Hermine
        ancre_hermine(grille, grille_coloré, hermine,1)
    nbligne=-1 #Valeur d'initialisation du nombre de ligne (valeur Y) dans la grille.
    for axey in(grille): #Sélectionne un tableau (qui sera nommé axey) dans la matrice grille.
        nbligne=nbligne+1 #Indique le numéro du tableau actuelle.
        nbde1=0 #Valeur d'initialisation du nombre de pixel ancré sur une ligne
        nb_hermine=0 #Valeur d'initialisation du nombre de pixel nommé "hermine" dans une ligne qui va être supprimé
        nbcolonne=-1 #Désigne la position X dans la ligne.
        for axex in(axey): #Sélectionne une valeur dans le tableau sélectionné.
            nbcolonne=nbcolonne+1 #Indique le numéro correspondant à la valeur dans le tableau.
            if axex==1: #Si c'est un 1 qui a été sélectionné
                nbde1=nbde1+1 #Rajoute 1 au nombre de 1 se situant dans la grille
            if grille_coloré[nbligne][nbcolonne]=="hermine": #Si il trouve un pixel nommé "hermine" sur une ligne de la grille grille_coloré.
                nb_hermine=1 #Indique qu'il a trouvé un pixel à Hermine
                grille[nbligne][nbcolonne]=0 #Supprime l'occupation du pixel dans la grille, grille
            if nbde1==len(axey): #Si il n'y a que des 1 dans la grille

                #Exécute une animation de clignotement
                for i in range(2):
                    attend(0.1)
                    grille[nbligne]=[0]*largeur #Cache les pixels de la ligne
                    affiche_jeu(grille,[[-99,-99]],texte,"b",grille_coloré,hermine,1)
                    attend(0.2)
                    grille[nbligne]=[1]*largeur #Les refait apparaître
                    affiche_jeu(grille,[[-99,-99]],texte,"b",grille_coloré,hermine,1)
                    attend(0.1)
                del grille[nbligne] #Supprime la ligne (dans grille)
                grille.append([0]*largeur) #Créer une nouvelle ligne (dans grille)
                reclassementtab(grille,largeur) #Reclasse la grille, grille.
                score=[score[0]+100] #Rajoute 100 points au score
                del grille_coloré[nbligne] #Supprime la ligne (dans grille_coloré)
                grille_coloré.append([0]*largeur) #Créer une nouvelle ligne (dans grille_coloré)
                reclassementtab(grille_coloré,largeur) #Reclasse la grille grille_coloré.
                if nb_hermine==1: #Si sur la ligne qui a été supprimé, il y a eu un pixel nommé "hermine" (venant de Hermine)
                    continuer=None #Vu qu'Hermine à été éliminé, le jeu met fin à la parti (remarque: on s'attendrait à ce que continuer=False, mais pour que ça soit plus simple, si continuer=False -> Joueur 1 Game Over, si cantinuer=None -> Joueur 2 Game Over.
                    return(score, hermine, continuer) #Indique qu'on doit arrêté le jeu, car Hermine à été éliminé (continuer==None)

    if hermine!=[0,0]: #Si on est pas dans le mode Tetris Hermine, hermine==[0,0]. "hermine" n'existe donc pas !
        ancre_hermine(grille, grille_coloré, hermine,0) #Dé-ancre Hermine (car si elle était éliminé, le jeu se serait arrêté avant d'être arrivé ici.
        hermine=deplacebloc(grille,hermine,"B", hermine, grille_coloré) #Déplace automatiquement hermine vers le bas (puisque une ligne a disparu de la grille)
        hermine=deplacebloc(grille,hermine,"B", hermine, grille_coloré) #Déplacement en trop (?) (dans tout les cas, cela ne changerais rien..).
        return(score, hermine, True) #Indique qu'on continu le jeu (continuer==True)
    else:
        return(score)

def levels(score):
    """
    Entrée:
        score -> Le score (int)

    Sortie:
        niveau -> Le niveau du joueur dans le jeu (int)

    Principe:
        A partir du score, calcule le niveau (1150 points = Niveau 1, 10584 = Niveau 10...).
    """

    #calcule le niveau en prenant le score en entrée et en renvoyant le niveau.
    niveau=int(score[0]*0.001+1)
    return niveau


def cree_hermine(grille):

    """
    Entrée:
        grille -> La grille de jeu (list)

    Sortie:
        hermine -> Le bloc Hermine (list)

    Principe:
        Créer Hermine, un bloc mobile de 2 pixels, qui apparaîtra au milieu du sol.
    """

    hauteur=int(len(grille)) #Hauteur de la grille de jeu
    largeur=int(len(grille[0])/2) #Milieu de la grille de jeu
    hermine=[[hauteur-2,largeur],[hauteur-1,largeur]] #Créer Hermine au milieu du sol
    return(hermine)

def deplace_hermine(grille, hermine, direction, grille_coloré):
    """
    Entrée:
        grille -> La grille de jeu avec les collisions (list)
        hermine -> Le bloc hermine (list)
        direction -> La direction où le joueur veut qu'Hermine se déplace.
        grille_coloré -> La grille de jeu, contenant les couleurs de bloc (qui est visible par le joueur)

    Principe:
        Déplace vers la gauche ou la droite Hermine.

    Explication:

    Il va testé plusieurs possibilité:
    1. Si hermine peut aller à gauche/droite:
        --> Si oui, teste si après déplacement il y a un bloc sous Hermine: -> Oui: déplace Hermine.
                                                                            -> Non: Essaye en plus de faire descendre Hermine.  -> Oui: Déplace Hermine
       Sinon, il va essayé de déplacer Hermine en lui faisant un saut juste avant:
            --> Si oui, teste si il y aura toujours après le déplacement, un bloc pour accueullir Hermine.

       En d'autre terme, plusieurs choix pour déplacé: Direction / Descente+Direction / Saut+Direction

       Il renvoi les nouvelles coorodnnés d'Hermine (le bloc, si déplacé), sinon les anciennes.
    """

    #REMARQUE: les "[[-1,-1],[-1,-1]]" servent à empêcher un bug. En effet, le jeu déplace en même temps Hermine. Le problème est que si hermine_copie et déplacé comme hermine, alors hermine_copie==hermine... Et ce n'est pas bon !
    hermine_copie=deepcopy(hermine) #Copie le bloc "Hermine"
    if direction=="G": #Si le joueur 2 veut déplacé Hermine à la gauche
        if hermine==deplacebloc(grille, hermine_copie, "G", hermine, grille_coloré): #Si le jeu ne peut pas déplacé Hermine simplement par la gauche
            if hermine!=deplacebloc(grille, hermine_copie, "H", [[-1,-1],[-1,-1]], grille_coloré): #Si le jeu peut faire sauter Hermine
                hermine_copie=deplacebloc(grille, hermine_copie, "H", [[-1,-1],[-1,-1]], grille_coloré)
                if hermine_copie!=deplacebloc(grille, hermine_copie, "G", [[-1,-1],[-1,-1]], grille_coloré): #Si le jeu peut faire déplacé Hermine par la gauche
                    hermine=deplacebloc(grille, hermine, "H", [[-1,-1],[-1,-1]], grille_coloré)
                    return(deplacebloc(grille, hermine, "G", [[-1,-1],[-1,-1]], grille_coloré))
                else:
                    return(hermine)
            else:
                return(hermine)
        else: #Si elle peut le déplacer par la gauche.
            hermine_copie=deplacebloc(grille,hermine_copie, "G", hermine, grille_coloré)
            if hermine_copie==deplacebloc(grille,hermine_copie, "B", hermine, grille_coloré): #Vérifie si après le déplacement vers la gauche, il y a bien un pixel sous Hermine:
                return(deplacebloc(grille, hermine, "G", hermine, grille_coloré)) #Renvoi Hermine déplacé simplement par la gauche
            else: #Va faire descendre Hermine après l'avoir déplacé à la gauche.

                if hermine_copie!=deplacebloc(grille, hermine_copie, "B", hermine, grille_coloré): #Si après s'être déplacé à la gauche, Hermine peut descendre
                    hermine_copie=deplacebloc(grille, hermine_copie, "B", hermine, grille_coloré)
                    hermine_copie=deplacebloc(grille, hermine_copie, "D", hermine, grille_coloré)
                    if hermine_copie==deplacebloc(grille, hermine_copie, "B", hermine, grille_coloré): #Et si il y a un bloc pouvant l'accueillir après sa descente à gauche.
                        return(hermine_copie)
                    else:
                        return(hermine)
                else:
                    return(hermine)

    if direction=="D": #Si le joueur 2 veut déplacé Hermine à la gauche
        if hermine==deplacebloc(grille, hermine_copie, "D", hermine, grille_coloré): #Si le jeu ne peut pas déplacé Hermine simplement par la gauche
            if hermine!=deplacebloc(grille, hermine_copie, "H", [[-1,-1],[-1,-1]], grille_coloré): #Si le jeu peut faire sauter Hermine
                hermine_copie=deplacebloc(grille, hermine_copie, "H", [[-1,-1],[-1,-1]], grille_coloré)
                if hermine_copie!=deplacebloc(grille, hermine_copie, "D", [[-1,-1],[-1,-1]], grille_coloré): #Si le jeu peut faire déplacé Hermine par la gauche
                    hermine=deplacebloc(grille, hermine, "H", [[-1,-1],[-1,-1]], grille_coloré)
                    return(deplacebloc(grille, hermine, "D", [[-1,-1],[-1,-1]], grille_coloré))
                else:
                    return(hermine)
            else:
                return(hermine)
        else: #Si elle peut le déplacer par la gauche.
            hermine_copie=deplacebloc(grille,hermine_copie, "D", hermine, grille_coloré)
            if hermine_copie==deplacebloc(grille,hermine_copie, "B", hermine, grille_coloré): #Vérifie si après le déplacement vers la gauche, il y a bien un pixel sous Hermine:
                return(deplacebloc(grille, hermine, "D", hermine, grille_coloré)) #Renvoi Hermine déplacé simplement par la gauche
            else: #Va faire descendre Hermine après l'avoir déplacé à la gauche.
                if hermine_copie!=deplacebloc(grille, hermine_copie, "B", hermine, grille_coloré): #Si après s'être déplacé à la gauche, Hermine peut descendre
                    hermine_copie=deplacebloc(grille, hermine_copie, "B", hermine, grille_coloré)
                    hermine_copie=deplacebloc(grille, hermine_copie, "G", hermine, grille_coloré)
                    if hermine_copie==deplacebloc(grille, hermine_copie, "B", hermine, grille_coloré): #Et si il y a un bloc pouvant l'accueillir après sa descente à gauche.
                        return(hermine_copie)
                    else:
                        return(hermine)
                else:
                    return(hermine)




############ Fonction principale

def jeu(largeur, hauteur, modejeu):

    """
    Entrée:
        largeur -> largeur de la grille donné par le joueur
        hauteur -> hauteur de la grille donné par le joueur
        modejeu -> Mode de jeu (1 = Tetris Classique, 2= Tetris Hermine)
    """
    """ largeur et hauteur sont les dimensions voulues du jeu.

    Règles du jeu :
      MODE TETRIS NORMAL:
        Des blocs aléatoire descende, et l'objectif est de faire des ligne complète de blocs (des lignes pleine).
        On gagne 10 points si on arrive à placé un bloc, 100 points si on arrive à supprimé une ligne.
        En revanche, si le jeu n'arrive plus à placé de nouveau bloc, cela marque la fin de votre parti.
        Votre défis est donc de faire un maximum de point sans jamais atteindre le sommet.

        Sachant que plus votre niveau augmente, plus le jeu va vite. Une limite de vitesse est mise à partir du niveau 7.

        Touches:
            Espace -> Fai tourner le bloc
            Flèche Gauche -> Déplace le bloc à gauche
            Flèche Droite -> Déplace le bloc à droite
            Flèche Bas -> Déplace le bloc en bas
            Flèche haut -> MET EN PAUSE LE JEU

      MODE TETRIS HERMINE:
        Joueur 1: Joue à Tetris normalement (mais dois éliminé Hermine)
        Joueur 2: Contrôle Hermine, et dois essayer de survivre, sans se faire éliminer.

        On incarne Hermine (représenté par de 2 bloc de couleur vert claire, et géré par un joueur 2), et notre objectif est de ne pas nous faire éliminé.
        En d'autre terme, on est un bloc au sol mais pouvant se déplacé de gauche à droite, voir de haut.
        A chaque fois que le joueur 1 ancre un bloc, le jeu vérifiera si il peut ou non éliminé une ligne si Hermine est présente dessus.
        Si il l'élimine alors qu'il y a Hermine, alors le joueur 1 gagne (car il a éliminé Hermine).
        Si Hermine résiste, et que le joueur 1 perd (avec un Game Over classique sur un Tetris), le joueur 2 gagne.

        Concept fortement inspiré d'une des vidéos du vidéaste Mister Flech: https://youtu.be/IV9it6tEpbM?t=971 (Reset System - Tetris)

        Touches: les mêmes que dans le mode Tetris Classique

        Contrôle d'Hermine:
            Touche A -> Déplace Hermine vers la gauche
            Touche Z -> Déplace Hermine vers la droite

            ATTENTION: A et Z sont si vous utilisé le jeu sur Windows (EduPython. Pour Linux (Spyders)., ça A -> Q et Z -> W (configuration des touches de bases dans le jeu (en clavier Qwerty, et non Azerty...)
    """

    fen1.destroy() #Fait fermer le menu

    print(modejeu,"type jeu")
    #INITIALISATION DES VARIABLES
    modele=0 #Valeur d'initialisation du modèle de bloc (valeur inutilisé, elle sera remplacé)
    sens=0 #Valeur d'initialisation du sens du bloc (valeur inutilisé, elle sera remplacé)
    repère_temps=0 #Cette variable nous permet de nous "repérer" dans le temps. Afin de faire descendre automatiquement les blocs
    repère_temps2=0 #Parreil, mais dans l'idée où il y a un un temps d'attente avant que le bloc décide à s'ancré.
    evite_erreur=0 #Parfois, il arrive que le jeu plante si le bloc se déplace en même temps qu'il s'ancre dans la grille. La variable permet d'éviter ça.
    pause=0 #Si pause=0: le jeu est en marche. Si pause=1, le jeu est en pause.
    ancre_auto=[0,0] #Variable permettant de garder en tête le bloc actuel pour le comparer.
    maximum=99 #Temps que descend pixel par pixel le bloc.
    niveau=1 #Valeur d'initialisation

    grille=cree_grille(largeur,hauteur) #Créer une grille de largeur*hauteur
    grille_coloré = deepcopy(grille) #Copie la grille "grille". Elle permet de stocker le type de pixel dans la grille (et afficher la couleur)
    bloc=nouveau_bloc(largeur) #Créer notre premier bloc
    hermine=[0,0] #Valeur d'initialisation
    print("modejeuuuu",modejeu)
    if modejeu==2: #Si le mode Tetris Hermine est choisit:
        hermine=cree_hermine(grille) #Créer Hermine


    modele=bloc[1] #Le Type de bloc (T, L, Z...)
    sens=bloc[2] #Le sens du bloc (pas défaut, sur le côté...)
    bloc=bloc[0] #La matrice contenant les tableaux ayant les coordonnés de chaque pixel
    score=[0] #Initialisation du score
    #print(bloc,"yoyo")

    texte=[["Mode de jeu"],["Niveau X"],["Score XXXXXXXXX"],["Joueur TOP 1 "],["score TOP 1"],["Joueur TOP 2 "],["Score TOP 2"],["Joueur TOP 3 "],["Score TOP 3"]] #Texte d'initialisation
    menuu=0

    if modejeu==1: #Si on joue à Tetris Classique
        read=readnormal().split()
    else:
        read=readhermine().split()
    for i in range(6):
        texte[3+i]=read[i]
    print(texte)

    #JEU

    # Cela permet de s'interrompre quand la variable continuer devient False
    continuer = True
    while continuer:
        if pause==0: #Texte à affiché si le jeu est en marche
            if modejeu==1:
                texte[0][0]="Tetris Classique"
            else:
                texte[0][0]="Tetris Hermine"
            texte[1][0]="Niveau "+str(levels(score))
            texte[2][0]="Score "+str(score[0])

        else: #Texte à affiché si le jeu est en pause
            texte[0][0]="EN PAUSE !"

        # Gestion des évènements
        for event in pygame.event.get(): # Si on quitte
            if event.type == pygame.QUIT:
                pygame.quit()
                return
            # Si touche appuyée

            if event.type == pygame.KEYDOWN:
                if event.key== K_LEFT and pause==0: # appui sur la touche "flèche gauche". Et si le jeu n'est pas en pause.
                    evite_erreur=1
                    bloc=deplacebloc(grille, bloc, "G", hermine, grille_coloré)#mettre à jour le bloc selon s'il s'est déplacé ou non.
                    evite_erreur=0

                elif event.key == K_RIGHT and pause==0: #Si on appuie sur la touche directionnel "droite". Et si le jeu n'est pas en pause.
                    evite_erreur=1
                    bloc=deplacebloc(grille, bloc, "D", hermine, grille_coloré) #Va à droite
                    evite_erreur=0

                elif event.key == K_UP: #Dans un vrai Tetris, on ne peut pas déplacé un bloc vers le haut. Ainsi, cette touche sert à mettre en pause le jeu.
                    evite_erreur=1
                    if pause==0: #Met en pause le jeu
                        pause=1
                    else:        #Reprend le jeu
                        pause=0
                    evite_erreur=0

                elif event.key == K_DOWN and pause==0: #Appui sur la touche "flèche bas". Et si le jeu n'est pas en pause.
                    evite_erreur=1
                    bloc=deplacebloc(grille, bloc, "B", hermine, grille_coloré) #Fait descendre le bloc
                    evite_erreur=0

                elif event.key == K_RETURN and pause==9: # touche entrée pour valider le bloc. Et si le jeu n'est pas en pause.
                    # à compléter : valider ou non le bloc, créer éventuellement un bloc, vérifier si on a perdu...
                    evite_erreur=1 #Bloque la descente automatique du bloc, le temps que celui si s'ancre.
                    bloc=validation(grille,bloc,score,modele,grille_coloré,hermine) #Vérifie si le nouveau bloc peut s'ancré
                    if bloc==[[0,0]]: #Si le nouveau bloc renvoyé est "vide", arrête le jeu
                        continuer=False
                        #Fin de la partie
                    else: #Sinon, exécute le script normalement.
                        #print(bloc,"SALUT A TOUSSS LEZAMI")
                        modele=bloc[1] #Définie Le type de bloc (bloc T, Z, L...)
                        sens=bloc[2] #Définie Le sens du bloc
                        bloc=bloc[0] #Définie La matrice contenant les tableaux des coordonnés de chaque pixel
                        #print(bloc,"bloc",modele,"modele",sens,"sens YO LES GENSSSSSS")
                        score=supprligne(grille,largeur,score,grille_coloré,hermine, continuer,texte) #Si la ligne est pleine, elle est supprimé et remplacé et il reçois le nouveau score + les nouvelles coordonnés du bloc hermine.
                        if hermine!=[0,0]: #Si on est pas dans le mode Tetris Hermine, hermine=[0,0]. "hermine" n'existe donc pas !
                            hermine=score[1] #Redéfinie le bloc hermine
                            continuer=score[2] #Redéfinie la valeur continuer
                            score=score[0] #Redéfinie le score par la vrai valeur score.
                        evite_erreur=0 #Débloque la descente automatique.

                elif event.key == K_SPACE and pause==0: #Si la touche "ESPACE" est pressé. Et que le jeu n'est pas en pause.
                    evite_erreur=1
                    #print("sonic le plus beau")
                    rota=rotation(grille, bloc, modele, sens) #Va envoyé le bloc actuel avec son type de bloc et son sens, puis "rota" aura le bloc déplacé, son type de bloc, et son nouveau sens.
                    #print(rota)
                    bloc=rota[0]
                    modele=rota[1]
                    sens=rota[2]
                    evite_erreur=0

                elif event.key == K_q and pause==0 and modejeu==2:
                    hermine=deplace_hermine(grille,hermine,"G",grille_coloré)
                elif event.key == K_w and pause==0 and modejeu==2:
                    hermine=deplace_hermine(grille,hermine,"D",grille_coloré)

        # à chaque tour de boucle, on affiche l'état du jeu
        affiche_jeu(grille,bloc,texte,modele,grille_coloré,hermine,modejeu) # à compléter

        # Cette instruction permet d'éviter que la boucle n'aille pas plus vite que fps tours de boucle/seconde.
        clock.tick(fps)
        repère_temps=repère_temps+1
        repère_temps2=repère_temps2+1

        if repère_temps2>3:
            if pause==0 and evite_erreur==0:
                ancre_auto=deepcopy(bloc)
                if hermine!=[0,0]:
                    ancre_hermine(grille, grille_coloré, hermine,1)
                if bloc==deplacebloc(grille, ancre_auto, "B", hermine, grille_coloré):
                    evite_erreur=1 #Bloque la descente automatique du bloc, le temps que celui si s'ancre.
                    #print("entrée")
                    bloc=validation(grille,bloc,score,modele,grille_coloré,hermine) #Vérifie si le nouveau bloc peut s'ancré
                    if bloc==[[0,0]]: #Si le nouveau bloc renvoyé est "vide", arrête le jeu
                        continuer=False
                        #Fin de la partie
                    else: #Sinon, exécute le script normalement.
                        #print(bloc,"SALUT A TOUSSS LEZAMI")
                        modele=bloc[1] #Définie Le type de bloc (bloc T, Z, L...)
                        sens=bloc[2] #Définie Le sens du bloc
                        bloc=bloc[0] #Définie La matrice contenant les tableaux des coordonnés de chaque pixel
                        #print(bloc,"bloc",modele,"modele",sens,"sens YO LES GENSSSSSS")
                        score=supprligne(grille,largeur,score,grille_coloré,hermine,continuer,texte) #Si la ligne est pleine, elle est supprimé et remplacé et il reçois le nouveau score + les nouvelles coordonnés du bloc Hermine.
                        if hermine!=[0,0]: #Si on est pas dans le mode Tetris Hermine, hermine=[0,0]. "hermine" n'existe donc pas !
                            hermine=score[1] #Redéfinie Hermine par ses nouvelles valeurs
                            continuer=score[2] #Redéfinie la valeur continuer
                            score=score[0] #Redéfinie score par sa vrai valeur
                        evite_erreur=0 #Débloque la descente automatique.
                        print("Oui 3")
                else:
                    if hermine !=[0,0]:
                        ancre_hermine(grille, grille_coloré, hermine,0)
                    repère_temps2=0
            else:
                deplacebloc(grille, ancre_auto, "H", hermine, grille_coloré)

        #niveau=11
        niveau=8-levels(score)
        if niveau<2:
            niveau=2
        while repère_temps>niveau: #Fait descendre le bloc tout les "temps"*15 d'images.
            #print(repère_temps)
            if evite_erreur!=1 and pause==0: #Si le jeu n'est pas en pause, et si il ancre pas un bloc (ou autre)
                #print("laupok")
                bloc=deplacebloc(grille, bloc, "B", hermine, grille_coloré) #Fait descendre le bloc.
                levels(score)
            repère_temps=0
    # Si on sort de la boucle, c'est que le jeu s'arrête... que faire alors ?
    if modejeu==2: #Si le Game Over se passe dans le mode Hermine
        if continuer==None: #Si continuer!=True, le jeu s'arrête. Mais si continuer==None, la défaite est donné au joueur 2. Si continuer!=True et continuer!=None, alors la défaite est donné au joueur 1
            texte[0][0]="Victoire: Joueur 1 !"
            affiche_jeu(grille,[[0,-555]],texte,modele,grille_coloré,hermine,modejeu)
            print("Game Over Joueur 2")
        else:
            texte[0][0]="Victoire: Joueur 2 !"
            affiche_jeu(grille,[[0,-555]],texte,modele,grille_coloré,hermine,modejeu)
            print("Game Over Joueur 1")
    else:
        texte[0][0]="GAME OVER"
        affiche_jeu(grille,[[0,-555]],texte,modele,grille_coloré,hermine,modejeu)
        print("Game Over")

    ##### Ici, nous allons remplacé ou non les valeurs du High Score.

    #Si le score est au dessus de celui du joueur ayant le meilleur Score
    if score[0]>int(texte[4]):
        texte[4]=score[0] #Sauvegarde le score
        texte[3]=assemble(input("Félicitation, vous entrez dans le High Score (1er) ! Entrez votre prénom:"))
    #Si le score est au dessus de celui du deuxième joueur ayant le meilleur Score, mais en dessous du premier
    elif score[0]>int(texte[6]):
        texte[6]=score[0] #Sauvegarde le score
        texte[5]=assemble(input("Félicitation, vous entrez dans le High Score (2ème) ! Entrez votre prénom:"))
    #Si le score est au dessus de celui du troisième joueur ayant le meilleur Score, mais en dessous du deuxième
    elif score[0]>int(texte[8]):
        texte[8]=score[0] #Sauvegarde le score
        texte[7]=assemble(input("Félicitation, vous entrez dans le High Score (3ème) ! Entrez votre prénom:"))
    if modejeu==1: #Si on est dans le mode de jeu Tetris Classique, sauvegarde dans le fichier prévu pour ce mode
        savenormal(str(texte[3])+" "+str(texte[4])+" "+str(texte[5])+" "+str(texte[6])+" "+str(texte[7])+" "+str(texte[8]))
    else: #Sinon, on est dans le mode de jeu Tetris Hermine et sauvegarde dans le fichier prévu pour ce mode
        savehermine(str(texte[3])+" "+str(texte[4])+" "+str(texte[5])+" "+str(texte[6])+" "+str(texte[7])+" "+str(texte[8]))

modejeu=0
#jeu(15,22,modejeu)



####################MENU


def tetrisclassique(): #Si mode tetrisclassique sélectionné
    jeu(15,22,1)
    fen1.destroy() #Supprime la fenêtre
    return

def tetrishermine(): #Si mode tetrishermine sélectionné.
    jeu(15,22,2)
    fen1.destroy() #Supprime la fenêtre
    return

##################################CREATION DU MENU DE SELECTION DE MODE

fen1 = Tk() #Créer une fenêtre vide
tex1 = Label(fen1, text='-- Super Tetris 3000 --', fg='red') #Intègre du texte à la fenêtre
tex1.pack() #Composant de la fenêtre.
bou1 = Button(fen1, text="Mode Tetris Classique",command=tetrisclassique).pack() #Bouton 1 qui fait appel à la fonction tetrisclassique()
bou2 = Button(fen1, text="Mode Tetris Hermine",command=tetrishermine).pack() #Bouton 2 qui fait appel à la fonction tetrishermine()
tex2 = Label(fen1, text='                                                              ', fg='red').pack() #Texte nous permettant de faire un espace entre les boutons
fen1.mainloop() #Permet de garder la fenêtre tout le temps allumé

###################################





