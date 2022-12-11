"""
Ce fichier comprend les transformations correspondant à
$F(R_{i-1},K_i)$ (permutation, S-box, etc.) appliquées au cas particulier du DES.
"""
from permutation import *

"""
Dictionnaire des 8 S-BOX  (voir énoncé du projet).
"""
A, B, C, D, E, F = 10, 11, 12, 13, 14, 15

S_BOX_BANK = [
    [4, A, 9, 2, D, 8, 0, E, 6, B, 1, C, 7, F, 5, 3],
    [E, B, 4, C, 6, D, F, A, 2, 3, 8, 1, 0, 7, 5, 9],
    [5, 8, 1, D, A, 3, 4, 2, E, F, C, 7, 6, 0, 9, B],
    [7, D, A, 1, 0, 8, 9, F, E, 4, 6, C, B, 2, 5, 3],
    [6, C, 7, 1, 5, F, D, 8, 4, A, 9, E, 0, 3, B, 2],
    [4, B, A, 0, 7, 2, 1, D, 3, 6, 8, 5, 9, C, F, E],
    [D, B, 4, 1, 3, F, 5, 9, 0, A, E, 7, 6, 8, 2, C],
    [1, F, D, 0, 5, 7, A, 4, 9, 2, 3, E, 6, B, 8, C]
]

S_BOX_RFC = [
    [C, 4, 6, 2, A, 5, B, 9, E, 8, D, 7, 0, 3, F, 1],
    [6, 8, 2, 3, 9, A, 5, C, 1, E, 4, 7, B, D, 0, F],
    [B, 3, 5, 8, 2, F, A, D, E, 1, 7, 4, C, 9, 6, 0],
    [C, 8, 2, 1, D, 4, F, 6, 7, 0, A, 5, 3, E, 9, B],
    [7, F, 5, A, 8, 1, 6, D, 0, 9, 3, E, B, 4, 2, C],
    [5, D, F, 6, 9, 2, C, A, B, 7, 8, 1, 4, 3, E, 0],
    [8, E, 2, 5, 6, 9, 1, C, F, 4, B, 0, D, A, 3, 7],
    [1, 7, E, D, 0, 5, 8, 3, 4, F, A, 6, 9, C, B, 2],
]

def apply_sbox(data, s_box):
    """
    Cette fonction applique les 8 s-box sur un entier de 32 bits et ressort l'entier de
    32bits correspondant. (voir énoncé du projet).
    Chacun des 8 groupes de 4 bits doit être remplacé en utilisant la S-BOX correspondante.
    Les 4 bits de poids le plus forts utilisent la première S-BOX, les 4 suivants la deuxième, etc.
    :param s_box: s_box utilisée, fournie sous forme de liste de liste.
        Le premier élément de la liste est utilisée pour les 4 bits les plus fort.
    :param data: Un entier de 32 bits.
    :return: L'entier de 32 bits modifié.
    """
    var = 0b0
    for i in range(8):                                      #pour parcourir les 8 groupes de 4 bits
        bits = (data >> (32 - (4 * (i + 1)))) & 0b1111      #Recuperer les 4 bits  de la clé
        var |= (s_box[i][bits] & 0b1111)                    #ajouter a la fin de la variable
        var <<= 4                                           #shift left pour avoir 4 bits 0 pour l'etape suivante

    var >>= 4                                               #supprimer les 4 bits de 0 ajouter en sortie de la boucle

    return var

def gost_feistel_function(key, data, s_box=S_BOX_RFC):
    """
    Cette fonction applique l'ensemble des transformations consistuant la fonction de Feistel spécifique au GOST:
    - Application de l'addition modulo
    - Appliquation des S-box
    - Application du shift de 11 bits
    :param s_box: s_box utilisée sous la forme de liste de liste
    :param key: La clé de 32 bits locale au round.
    :param data: Les 32 bits de données sur lesquels appliquer la fonction de Feistel
    :return: Les 32 bits transformés suivant la fonction de Feistel
    """
    data = (data + key) % (1 << 32)     #addition et module 2 exposant 32
    data = apply_sbox(data, s_box)      #envoie vers la fonction sbox
    data = shift_left(data, 32, 11)     #shift left de 11 bits

    return data
