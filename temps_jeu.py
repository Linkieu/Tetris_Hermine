from time import time, sleep

#Ce fichier nous permet de faire une "pause" temporaire dans le script, sans avoir de problème entre Tkinter et time.

def attend(durée):
    sleep(durée) #Fait attendre d'une durée de durée secondes.
    return