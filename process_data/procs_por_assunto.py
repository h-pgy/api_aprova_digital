import re
from utilities.my_tools import b_resp
from utilities.proj_decorators import json_resp
from utilities.connect import gen_db

@json_resp(list=True)
def list_assuntos(*args, include_disabled = False, json_alike = True):

    db = gen_db()
    cidade = db.city.find_one()
    dados = []
    for proc in cidade['processos']:
        if not include_disabled and proc.get('disabled'):
            continue
        dados.append(
            [
            b_resp(
            'assunto',
            'Título do assunto',
            proc['title']
            ),
            b_resp(
                'desc',
                'Descrição do assunto',
                proc['descricao']
            ),
            b_resp(
                'disabled',
                'Indica se o processo está desabilitado',
                proc['disabled']
            ),
            b_resp(
                'categoria',
                'Tipo de assunto ou Coordenadoria responsável pela análise',
                proc.get('categoria')
            )
            ]
        )

    return dados

@json_resp(list = True)
def list_procs_by_assunto(assunto, *args, json_alike = True):

    assunto = re.sub(r'^\d\. ', '', assunto)
    assunto = assunto.strip()

    db = gen_db()
    procs = db.process.find({'config_metadata.title': assunto}, {'nP': 1})

    dados = [
        b_resp('num_protocolo',
               'Número de protocolo do processo no Aprova Digital',
               proc['nP'])
        for proc in procs
        ]

    return dados