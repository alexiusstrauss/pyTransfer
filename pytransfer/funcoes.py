
# Funcoes

import hashlib
from random import choice, getrandbits


def genBalanceRandom():
    #Funcao para gerar Saldo randomico - possivel de implementações e regras.
    result = getrandbits(16)
    return result


def randomchar(tamanho):
    # funcao para dandomizar um char de tamanho definido
    caracteres  = '123456-78ABCDEFGHJK-MNPQRSTXabcdefghjkmnpqrstxz-'
    result  = ''    
    for char in range(tamanho):
        result += choice(caracteres)
    return result

def getnewtoken():
    # funcao para criar token no padrao sha1 usando 2 valores randomicos
    result = hashlib.sha1((randomchar(5) + randomchar(5)).encode('utf-8')).hexdigest()
    return result

