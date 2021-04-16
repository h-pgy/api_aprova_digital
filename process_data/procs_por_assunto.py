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