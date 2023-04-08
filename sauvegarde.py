# Créé par Matthieu, le 27/01/2021 en Python 3.7

from tkinter import *
"""
Ce fichier python nous permet de sauvegarder et de lire certains fichier txt.
Ainsi, le High Score du Tetris Classique, se situeras dans "scorenormal.txt".
Et le High Score du Tetris Hermine, se situeras dans "scorehermine.txt".
Pour "grille.txt", c'est une sauvegarde de la partie quitté.

Chaque fichier à 2 fonctions:
    -Une lecture
    -Une écriture

Le premier, servira pour jeu_eleves.py, si il a besoin d'information. (sous la forme: READ[nom](): )
L'autre, s'il veut conserver une information. (sous la forme: SAVE[nom](variable): )
"""
scorehermine = open('scorehermine.txt', 'r') #Ouvre le fichier scorehermine.txt en mode lecture

def readnormal():
    scorenormal = open('scorenormal.txt', 'r') #Ouvre le fichier "scorenormal.txt" en mode 'r' (Read, lecture), et conserve les données+paramètres dans la variable "scorenormal".
    read=scorenormal.read() #Donne la parti texte (qu'on vois en ouvrant le fichier avec un bloc-note par exemple) à la variable "read". ATTENTION: Si on fait juste read=scorenormal, read contiendra le texte + les paramètres du fichier !!!
    scorenormal.close() #Ferme le fichier "scorenormal.txt"
    return(read) #Renvoi le contenu du fichier, stocker dans "read"

def savenormal(highscore): #Prend en entrée le High Score sous forme de matrice: [[Joueur 1],[Score 1],[J2],[S2],|J3],[S3]]
    scorenormal = open('scorenormal.txt', 'w') #Ouvre le fichier "scorenormal.txt" en mode 'w' (Write, écriture), et conserve les données+paramètres dans la variable "scorenormal".
    scorenormal.write(highscore) #Ecrit (ramplace le contenu du fichier) le contenu de la variable "High Score" dans le fichier .txt. [[Matthieu],[5221],[Yassim],[2012],[Alfred],[1234]]
    scorenormal.close() #Ferme le fichier "scorenormal.txt"
    return #Renvoi rien car il a fait ce qu'il lui a été demandé.

def readhermine(): #Même chose que pour readnormal() à quelques modification près.
    scorehermine = open('scorehermine.txt', 'r')
    read=scorehermine.read()
    scorehermine.close()
    return(read)

def savehermine(highscore): #Même chose que pour savenormal() à quelques modification près.
    scorehermine = open('scorehermine.txt', 'w')
    scorehermine.write(highscore)
    scorehermine.close()
    return

def readgrille(): #Même chose que pour readnormal() à quelques modification près.
    scoregrille = open('scoregrille.txt', 'r')
    read=scoregrille.read()
    scoregrille.close()
    return(test)

def savegrille(grille): #Même chose que pour savenormal() à quelques modification près.
    scoregrille = open('scoregrille.txt', 'w')
    scoregrille.write(grille)
    scoregrille.close()
    return
