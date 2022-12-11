"""
Ce fichier comprend toutes les foncitons liées aux permutations.

Bon ok, il n'y en a qu'une.
"""


def permutation(block, new_position, input_size):
    """
    CETTE FONCTION N'EST UTILISEE QUE POUR LA VERSION AVANCEE DE GENERATION DE CLE, A FAIRE A LA FIN!!!
    Cette fonction permet de permuter un bloc de bits suivant une liste contenant les nouveaux indices et en précisant
    la taille du block.
    Par exemple, si le block donné est '0b101' et les nouvelles positions voulues est [2 3 1] (input_size=3)
    alors la fonction retournera '0b011'.

    !!! Attention !!! Les indices commence à 1 pour le premier élément.
    :param block: Block de bits à permuter (sous forme d'entier).
    :param new_position: Liste de nouveaux indices (1 = premier élément)
    :param input_size: Nombre de bits du block initial.
    :return: un block de bits permuté (sous forme d'entier).
    """
    var = 0b0
    for i in new_position:
        one_bit = block >> (input_size - i)    #shift right pour mettre le bit a droite et AND Pour recuperer le  bit
        mask = 1
        one_bit = one_bit & mask               #Ajout du mask pour recuperer la variable avec un OR
        var = (var | one_bit) << 1             #shift left pour add un 0 en sortant de la boucle pour etape suivante
    var = var >> 1                             #Pour faire disparaitre dernier 0 ajouté en fin de boucle

    return var

def shift_left(data, input_size, n_bit):
    """
    Cette fonction doit être capable de barrel-shifter vers la gauche de n_bit éléments
    l'argument data de taille input_size
    :param data: L'entier à shifter.
    :param input_size: La taille en bits de data.
    :param n_bit: nombre de bit à shifter
    :return: L'entier data shifté de 1 vers la gauche
    """
    left = data >> (input_size - n_bit)         #Recupere les bits left
    right_temp = data << n_bit                  #shift vers la gauche les n bits

    mask = ((1 << input_size) - 1)              #preparation du masque 1<<inptsize - 1 pour avoir le masque 0b1111

    right_temp = right_temp & mask              #applique le mask pour recuperer les bits
    var = right_temp | left                     #OR pour additionner les bits
    return var

