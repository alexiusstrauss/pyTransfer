
# Funcoes

import hashlib
from random import choice, getrandbits


def genBalanceRandom():
    return getrandbits(16)


def randomchar(tamanho):
    # funcao para dandomizar um char de tamanho definido
    caracteres  = '123456-78ABCDEFGHJK-MNPQRSTXabcdefghjkmnpqrstxz-'
    return ''.join(choice(caracteres) for _ in range(tamanho))

def getnewtoken():
    return hashlib.sha1(
        (randomchar(5) + randomchar(5)).encode('utf-8')
    ).hexdigest()

