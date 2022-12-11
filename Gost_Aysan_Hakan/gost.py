"""
Ce fichier reprend les fonctions permettant un chiffrement
et un déchiffrement GOST suivant différents modes d'opération
"""
from Gost_Aysan_Hakan.utilities import _64bits_block_to_bytearray
from gost_feistel_function import gost_feistel_function
from key_generator import *
from utilities import *

def feistel(block, key, swap=True):
    """
    Cette fonction applique l'ensemble des transformations effectuées à chaque round.

    :param block: Le block de 64 bits à transformer
    :param key: La clé de 32 bits locale au round
    :param swap: Booléen permettant de spécifier si un swap final entre les parties L et R est requis.
    :return: Le bloc de 64 bits transformé.
    """
    right = block & 0xff_ff_ff_ff                   #Recuper les 32 bits droits du block
    left = (block >> 32) & 0xff_ff_ff_ff            #Recuper les 32 bits gauche du block

    left = left ^ gost_feistel_function(key, right) #la partie droite est envoyé pour chiffrer et fait un xor aec gauche

    if swap:                        #Condition est utiliser a la fin des round pour ne plus inversé la partie right left
        data = right << 32 | left
        return data
    else:
        data = left << 32 | right
        return data


def encrypt_block(block, key_array):
    """
    Cette fonction permet de chiffrer un bloc de 64 bits suivant la méthode GOST.
    :param block: bloc de 64 bits à chiffrer
    :param key_array: liste ordonnée des 32 clés locales pour chaque round
    :return: Le bloc de 64 bits chiffré.
    """
    for key in key_array[:-1]:                  #parcours chaque clé dans la liste
        block = feistel(block, key)             #chiffre les block avec les clé,valeur chiffré devient le bloc suivant
    return feistel(block, key_array[-1], False) #pour la derniere clé on n'inverse plus la droite et la gauche(if swap)


def encryptECB(blocks, key_array):
    """
    Cette fonction applique le chiffrement GOST à une liste de blocs de 64 bits suivant le mode d'opération ECB.
    :param blocks: Liste de blocs à chiffrer.
    :param key_array: liste ordonnée des 32 clés locales pour chaque round
    :return: la liste de blocs chiffrés.
    """
    blocks_final = []                               #Chiffrement classique ECB avec clé simple
    for block in blocks:                            #Chaque bloque est chiffrer de la meme maniere
        block = encrypt_block(block, key_array)
        blocks_final.append(block)
    return blocks_final


def encryptCBC(blocks, key_array):
    """
    Cette fonction applique le chiffrement GOST à une liste de blocs de 64 bits suivant le mode d'opération CBC.
    :param blocks: Liste de blocs à chiffrer.
    :param key_array: liste ordonnée des 32 clés locales pour chaque round
    :return: la liste de blocs chiffrés avec le vecteur initial utilisé en première position.
    """
    i_v = rdm_IV_generator()                      #Chiffrement avec vecteur initial
    blocks_final = [i_v]                          #chiffrer le premier bloc de données
    for block in blocks:                          #puis utilise le résultat du chiffrement pour chiffrer le bloc suivant
        block = block ^ i_v
        i_v = encrypt_block(block, key_array)
        blocks_final.append(i_v)
    return blocks_final


def encryptCTR(blocks, key_array):
    """
    Cette fonction applique le chiffrement GOST à une liste de blocs de 64 bits
    suivant le mode d'opération CTR.
    :param blocks: Liste de blocs à chiffrer.
    :param key_array: liste ordonnée des 32 clés locales pour chaque round
    :return: la liste de blocs chiffrés.
    """
    i_v = rdm_IV_generator()                    #utilise un compteur(i) pour chiffrer chaque bloc de données
    blocks_final = [i_v]                        #Contrairement aux autres qui utilise le bloc precedent chiffré(ecb;cbc)
    for i, block in enumerate(blocks):
        block_xor_index = i_v ^ i
        encrypted_block_xor_index = encrypt_block(block_xor_index, key_array)
        blocks_final.append(block ^ encrypted_block_xor_index)
    return blocks_final


def encrypt(blocks, key_array, operation_mode="ECB"):
    """
    Cette fonction applique le chiffrement GOST à une liste de blocs de 64 bits.
    :param blocks: Liste de blocs à chiffrer.
    :param key_array: liste ordonnée des 32 clés locales pour chaque round
    :param operation_mode: string spécifiant le mode d'opération ("ECB", "CBC" ou "CTR")
    :return: la liste de blocs chiffrés avec le vecteur initial utilisé en première position.
    """
    if operation_mode == "ECB":
        return encryptECB(blocks, key_array)

    if operation_mode == "CBC":
        return encryptCBC(blocks, key_array)

    if operation_mode == "CTR":
        return encryptCTR(blocks, key_array)

    print('Le mode d''operation introuvable, chiffrement par defaut ECB')
    return encryptECB(blocks, key_array)


def decrypt_block(block, key_array):
    """
    Cette fonction permet de déchiffrer un bloc de 64 bits qui a été chiffré préalablement
     suivant la méthode GOST.
    :param block: bloc de 64 bits à chiffrer
    :param key_array: liste ordonnée des 32 clés locales pour chaque round
    :return: Le bloc de 64 bits déchiffré.
    """
    for key_round in reversed(key_array[1:]):    #(1,[2,3,4,5])   --->   [5,4,3,2]  iv [0]
        block = feistel(block, key_round)
    return feistel(block, key_array[0], False)


def decryptECB(blocks, key_array):
    """
    Cette fonction dé-chiffre une liste de blocs de 64 bits qui a été préalablement chiffrée
    avec la méthode GOST suivant le mode d'opération ECB.
    :param blocks: Liste de blocs à déchiffrer.
    :param key_array: liste ordonnée des 32 clés locales pour chaque round.
    Identique à celle utilisée pour le chiffrement.
    :return: la liste de blocs déchiffrés.
    """
    blocks_final = []                               #Inverse le processus de chiffrement
    for block in blocks:
        block = decrypt_block(block, key_array)
        blocks_final.append(block)
    return blocks_final


def decryptCBC(blocks, key_array):
    """
    Cette fonction dé-chiffre une liste de blocs de 64 bits qui a été préalablement chiffrée
    avec la méthode GOST suivant le mode d'opération CBC.
    :param blocks: Liste de blocs à déchiffrer.
    :param key_array: liste ordonnée des 32 clés locales pour chaque round.
    Identique à celle utilisée pour le chiffrement.
    :return: la liste de blocs déchiffrés.
    """
    i_v = blocks[0]
    blocks_final = []

    for block in blocks[1:]:
        block = decrypt_block(block, key_array) ^ i_v
        blocks_final.append(block)
        i_v = block
    return blocks_final

def decryptCTR(blocks, key_array):
    """
    Cette fonction dé-chiffre une liste de blocs de 64 bits qui a été préalablement chiffrée
    avec la méthode GOST suivant le mode d'opération CTR.
    :param blocks: Liste de blocs à déchiffrer.
    :param key_array: liste ordonnée des 32 clés locales pour chaque round.
    Identique à celle utilisée pour le chiffrement.
    :return: la liste de blocs déchiffrés.
    """
    i_v = blocks[0]
    blocks_final = []

    for i, block in enumerate(blocks[1:]):
        block_xor_index = i_v ^ i
        encrypted_block_xor_index = encrypt_block(block_xor_index, key_array)
        blocks_final.append(block ^ encrypted_block_xor_index)

    return blocks_final


def decrypt(blocks, key_array, operation_mode="ECB"):
    """
    Cette fonction dé-chiffre une liste de blocs de 64 bits qui a été préalablement chiffrée
    avec la méthode GOST suivant le mode d'opération CBC ou ECB.
    :param blocks: Liste de blocs à déchiffrer.
    :param key_array: liste ordonnée des 32 clés locales pour chaque round.
    Identique à celle utilisée pour le chiffrement.
    :param operation_mode: string spécifiant le mode d'opération ("ECB", "CBC" ou "CTR")
    :return: la liste de blocs déchiffrés.
    """
    if operation_mode == "ECB":
        return decryptECB(blocks, key_array)

    if operation_mode == "CBC":
        return decryptCBC(blocks, key_array)

    if operation_mode == "CTR":
        return decryptCTR(blocks, key_array)

    print('Le mode d''operation introuvable, déchiffrement par defaut ECB')
    return decryptECB(blocks, key_array)

def encrypt_file(input_filename, output_filename, operation_mode="CTR", simple_key=True):
    """
    Cette fonction chiffre un fichier avec la méthode GOST suivant le mode d'opération CBC ou ECB.
    Les fonctions de lecture du fichier fournies dans utilities.py peuvent être utiles
    :param input_filename: Nom du fichier à chiffrer
    :param output_filename: Nom du fichier chiffré
    :param operation_mode: string spécifiant le mode d'opération ("ECB", "CBC" ou "CTR")
    :param simple_key: utilise la clé de base du GOST si True, sinon utilise le schéma avancé(voir énoncé)
    :return: La clé utilisée pour le chiffrement.
    """
    data = load_txt_file(input_filename).strip()
    blocks = bytearray_to_64bits_block(bytearray(data, 'utf-8'))

    if simple_key:
        random_key = rdm_key_generator()
        keys = gost_key_generator(random_key)
    else:
        random_key = rdm_key_generator(128)
        keys = gost_advanced_key_generator(random_key)

    encrypted_blocks = encrypt(blocks, keys, operation_mode)

    save_to_bin(output_filename, _64bits_block_to_bytearray(encrypted_blocks))

    return random_key




def decrypt_file(input_filename, output_filename, key, operation_mode="ECB", simple_key=True):
    """
    Cette fonction dé-chiffre un fichier qui a été préalablement chiffré
    avec la méthode GOST suivant le mode d'opération CBC ou ECB.
    Les fonctions de lecture du fichier fournies dans utilities.py peuvent être utiles

    :param input_filename: le nom du fichier chiffré.
    :param output_filename: le nom du fichier déchiffré
    :param key: La clé de 64 bits utilisée pour chiffrer le fichier.
    :param operation_mode: string spécifiant le mode d'opération ("ECB", "CBC" ou "CTR")
    """
    data = load_from_bin(input_filename)
    blocks = bytearray_to_64bits_block(bytearray(data))

    if simple_key:
        keys = gost_key_generator(key)
    else:
        keys = gost_advanced_key_generator(key)

    decrypted_blocks = decrypt(blocks, keys, operation_mode)
    save_to_bin(output_filename, _64bits_block_to_bytearray(decrypted_blocks))



def main():
    e_d = input('Inserer E pour Encrypt D pour Decrypt:')
    fichier_input = input('Entrez le nom du fichier en entrée')
    fichier_output = input('Entrez le nom de fichier en sortie')
    if e_d == "E":
        methode = input('Inserer la methode de chiffrement ECB,CBC,CTR:')
        key = encrypt_file(fichier_input, fichier_output, methode)
        return print(f"Voici votre clé de déchiffrement :{key}")

    elif e_d == "D":
        methode = input('Inserer la methode de chiffrement (ECB,CBC,CTR):')
        key = input('Entrez la clé')
        decrypt_file(fichier_input, fichier_output, int(key), methode)
        return key

    else:
        print("Erreur")


if __name__ == '__main__':
    main()




