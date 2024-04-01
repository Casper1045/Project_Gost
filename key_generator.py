"""
Ce fichier comprend toutes les foncitons liées à la génération de clés.
"""

import random


from permutation import permutation, shift_left

"""
Liste d'indices de permutation permettant de dropper les bits de parité de la clé globale.
"""
PARITY_DROP_TABLE = [57, 49, 41, 33, 25, 17, 9, 1, 58, 50, 42, 34, 26, 18, 10, 2, 59, 51, 43, 35, 27, 19, 11, 3, 60, 52,
                     44, 36, 63, 55, 47, 39, 31, 23, 15, 7, 62, 54, 46, 38, 30, 22, 14, 6, 61, 53, 45, 37, 29, 21, 13,
                     5, 28, 20, 12, 4]


"""
Liste d'indices de permutation permettant de combiner les deux parties de 28 bits
pour créer la clé locale à chaque round (compression D-box dans 
https://academic.csuohio.edu/yuc/security/Chapter_06_Data_Encription_Standard.pdf
et dans l'énoncé du projet).
"""
D_BOX_TABLE = [14, 17, 11, 24, 1, 5, 3, 28, 15, 6, 21, 10, 23, 19, 12, 4, 26, 8, 16, 7, 27, 20, 13, 2, 41, 52, 31, 37,
               47, 55, 30, 40, 51, 45, 33, 48, 44, 49, 39, 56, 34, 53, 46, 42, 50, 36, 29, 32]

LEFT_ROTATION = [1, 1, 2, 2, 2, 2, 2, 2, 1, 2, 2, 2, 2, 2, 2, 1]

def rdm_key_generator():
    """
    Cette fonction doit pouvoir générer une clé aléatoire de 256bits
    :return: un entier représenté sur 256 bits généré de manière aléatoire.
    """
    return random.getrandbits(256)      #Genere une clé de 256 bits


def rdm_IV_generator():
    """
    Cette fonction doit pouvoir générer un nombre aléatoire de 64bits
    :return: un entier représenté sur 64 bits généré de manière aléatoire.
    """
    return random.getrandbits(64)       #Genere une clé de 64 bits


def gost_key_generator(key):
    """
    Cette fonction renvoie une liste des 32 clés nécessaires pour chacun des rounds du GOST avancé.
    Les clés doivent être ordonnées (premier élément = clé pour round 1, etc.). On considère que les 8
    bits les plus faibles sont utilisés pour le round 1.
    :param key: Clé globale de 256 bits
    :return: Liste ordonnée de 32 clés locales utilisées pour chacun des rounds.
    """
    key_final = []
    for i in range(8):                  #8 clé depuis 256 bits
        bits_32 = key & 0xffff_ffff     #mask pour recuperer les 32 bits du 256
        key_final.append(bits_32)       #Ajout de la sous clé dans la liste_finale
        key = key >> 32                 #Shift vers la droite pour recup les 32 bit suivant la prochaine fois

    return (key_final * 3) + key_final[::-1]  #3 fois de gauche a droite une fois de droite a gauche


def gost_advanced_key_generator(key):
    """
    Cette fonction renvoie une liste des 32 clés nécessaires pour chacun des rounds du GOST avancé.
    Les clés doivent être ordonnées (premier élément = clé pour round 1, etc.)
    :param key: Clé globale de 128 bits
    :return: Liste ordonnée de 32 clés locales utilisées pour chacun des rounds.
    """

    keys_final = []

    right = key & 0xffff_ffff_ffff_ffff                       #recupere les 64 bits de droite
    left = (key >> 64) & 0xffff_ffff_ffff_ffff                #recupere les 64 bits de gauche

    left_keys = gost_advanced_subkey_generator(left)          #utilisation de la fct pour les subkey gauche
    right_keys = gost_advanced_subkey_generator(right)        #utilisation de la fct pour les subkey droite


    for i in range(16):
        keys_final.append(right_keys[i])
        keys_final.append(left_keys[i])


    return keys_final                                         #32 keys = [r, l, r, l...l]

def gost_advanced_subkey_generator(key_lr):
    """
    Cette fonction renvoie une liste des 16 clés nécessaires pour chacun des rounds du GOST avancé
    à partir d'une sous-clé de 64 bits gauche ou droite (voir énoncé).
    Les clés doivent être ordonnées (premier élément = clé pour round 1, etc.)
    :param key_lr: Clé de 64 bits issue d'une clé globale de 128 bits
    :return: Liste ordonnée de 16 clés locales.
    """
    subkeys = []
    key_droped_56 = permutation(key_lr, PARITY_DROP_TABLE, 64)   #permutation pour reduire la clé en 56 bits avec PARITY

    left_key = (key_droped_56 >> 28) & 0xfff_ffff                #Recupere la partie de gauche de la clé de 56 bits
    right_key = key_droped_56 & 0xfff_ffff                       #Recupere la partie de droite de la clé de 56 bits

    for i in range(16):
        shift = LEFT_ROTATION[i]                                 #Definit le nombre de shift depuis la table

        left_key = shift_left(left_key, 28, shift)               #shift_left la partie de gauche de 1 ou 2
        right_key = shift_left(right_key, 28, shift)             #shift_left la partie de droite de 1 ou 2

        left_right = (left_key << 28) | right_key                #shift left la gauche de 28 et faire OR avec coté droit

        left_right = permutation(left_right, D_BOX_TABLE, 56)    #permutation pour reduire la clé en 48 bits avec D_BOX

        subkeys.append(left_right & 0xffff_ffff)                 #Recuperer les 32 bits des 48 bits

    return subkeys                                               #Liste de 16 clés de 32 bits