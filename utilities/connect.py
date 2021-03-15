from pymongo import MongoClient
from config import conn_str_producao, conn_str_homologacao


def gen_db(env = 'homolog'):

    aceitos = {'producao' : {'prod', 'producao', 'produção'},
               'homologacao' : {'homolog', 'homologacao', 'homologação'}}

    if env is None or \
            env.lower() in aceitos['homologacao']:
        conn_str = conn_str_homologacao
        db = MongoClient(conn_str)['next-homologacao-sp']
    elif env.lower() in aceitos['producao']:
        conn_str = conn_str_producao
        db = MongoClient(conn_str)['next-producao']
    else:
        raise ValueError(f'Ambiente {env} nao é válido. Válidos: {aceitos}')

    return db