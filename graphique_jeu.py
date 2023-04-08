#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Jan  5 16:17:46 2021

@author: profinfo
"""

from pygame import *
import pygame
pygame.init()


############## Constantes pygame ################
size = largeur, hauteur = 800, 600
tsprite = 20 # taille d'un sprite en pixels
couleur_fond = (10, 10, 10) # gris foncé
couleur_contour = (100, 0, 0) # rouge foncé
couleur_blocs_statiques = (0,150,0) # vert
couleur_blocs_mobiles = (0,100,200) #  bleu un peu clair
couleur_hermine = (181,230,29) #Vert clair

pos_jeu = 10,10 # position du jeu par rapport à (0,0)

couleur_blocs_statiques_choisit = 0 #Valeur d'initialisation


# Le texte
couleur_texte=255, 255, 255 # noir
police = pygame.font.Font(None, 40) # police et taille du texte


fps = 15 # vitesse en frames/sec

############ Init du jeu ###################

# Initialisation de l'écran
screen = pygame.display.set_mode(size)

# Init de l'horloge
clock=pygame.time.Clock()

# pour rester appuyé sur une touche
pygame.key.set_repeat(100,5)

def convertit_coord_vers_rect(x,y, h, l):
    """ prend en argument des coordonnées dans la grille et
    les dimensions du rectangle, et les
    convertit en coordonnées pygame"""
    xr = x*tsprite + pos_jeu[0]
    yr = y*tsprite + pos_jeu[1]
    return Rect(xr,yr,h,l)



def affiche_jeu(grille,bloc,texte,modele,grille_coloré,hermine,modejeu):
    """ prend en argument une grille, un bloc "mobile" et une chaîne
    de caractère. Affiche le jeu sur la fenêtre pygame,
    et le texte à droite du jeu (score, message, ...)."""

    hjeu = len(grille)*tsprite
    ljeu = len(grille[0])*tsprite

    # position du texte, à droite
    xtexte = ljeu+tsprite + pos_jeu[0]
    ytexte = pos_jeu[1] + tsprite

    # Dessin du "fond"
    screen.fill(couleur_contour)
    pygame.draw.rect(screen, couleur_fond, convertit_coord_vers_rect(0,0,ljeu,hjeu))

    # Dessin des blocs "figés" de la grille
    for i in range(len(grille)):
        for j in range(len(grille[i])):
            if grille[i][j] == 1: #Si il y a un bloc entré, va mettre une couleur suivante (en fonction du type de bloc ancré)
                if grille_coloré[i][j] == "cf2":
                    couleur_blocs_statiques_choisit =(211,94,44) #Orange foncé bloc L A L'ENVERS
                if grille_coloré[i][j] == "b":
                    couleur_blocs_statiques_choisit =(55,218,253) #  bleu un peu clair BLOC T
                if grille_coloré[i][j] == "cl":
                    couleur_blocs_statiques_choisit =(200,150,0) #  Jaune Orangé BLOC BARRE
                if grille_coloré[i][j] == "cc":
                    couleur_blocs_statiques_choisit =(200,0,0) #  Rouge BLOC CARREE
                if grille_coloré[i][j] == "cf":
                    couleur_blocs_statiques_choisit =(55,160,247) #  Bleu BLOC L
                if grille_coloré[i][j] == "cp":
                    couleur_blocs_statiques_choisit =(150,0,200) #  Violet BLOC .
                if grille_coloré[i][j] == "cz":
                    couleur_blocs_statiques_choisit =(200,200,200) #  Blanc BLOC Z
                if grille_coloré[i][j] == "cz2":
                    couleur_blocs_statiques_choisit =(126,79,52) #  Marron BLOC Z A L'ENVERS
                if grille_coloré[i][j] == "hermine":
                    couleur_blocs_statiques_choisit =(181,230,29) #  Vert clair pour Hermine ancré

                pygame.draw.rect(screen, couleur_blocs_statiques_choisit, convertit_coord_vers_rect(j, i, tsprite, tsprite))

    # Dessin des blocs mobiles
    for i,j in bloc:
        pygame.draw.rect(screen, couleur_blocs_mobiles, convertit_coord_vers_rect(j,i, tsprite, tsprite))

    # Dessin de Hermine
    if modejeu==2:
        for i,j in hermine:
            pygame.draw.rect(screen, couleur_hermine, convertit_coord_vers_rect(j,i, tsprite, tsprite))

    # Dessin du texte
    a_afficher = police.render(str(texte[0][0]), 0, couleur_texte) #Affiche le Mode de jeu choisit
    screen.blit(a_afficher, (xtexte+150,ytexte))

    affiche_niveau = police.render(str(texte[1][0]), 0, couleur_texte) #Affiche le Niveau actuel
    screen.blit(affiche_niveau, (xtexte,ytexte+50))

    affiche_score = police.render(str(texte[2][0]), 0, couleur_texte) #Affiche le Score
    screen.blit(affiche_score, (xtexte,ytexte+80))

    affiche_niveau = police.render(str("-- High Score --"), 0, couleur_texte) #Affiche le meilleur joueur et son score
    screen.blit(affiche_niveau, (xtexte+100,ytexte+200))

    affiche_niveau = police.render(str("1er, "+texte[3]+" avec "+texte[4]+" points"), 0, couleur_texte) #Affiche le meilleur joueur et son score
    screen.blit(affiche_niveau, (xtexte,ytexte+230))

    affiche_niveau = police.render(str("2ème, "+texte[5]+" avec "+texte[6]+" points"), 0, couleur_texte) #Affiche le second deuxième meilleur joueur et son score
    screen.blit(affiche_niveau, (xtexte,ytexte+260))

    affiche_niveau = police.render(str("3ème, "+texte[7]+" avec "+texte[8]+" points"), 0, couleur_texte) #Affiche le 3ème meilleur joueur et son score.
    screen.blit(affiche_niveau, (xtexte,ytexte+290))
    # mise à jour de l'affichage
    pygame.display.flip()
