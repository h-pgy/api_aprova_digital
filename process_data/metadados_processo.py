from utilities.my_tools import b_resp
from utilities.proj_decorators import json_resp


def status_processo(proc):
    deferimento = 'Processo Deferido'
    desistencia = 'Usuário desistiu da análise do processo'
    indeferido = 'Processo Indeferido'
    finalizado = 'Processo Finalizado'

    eventos = proc['timeline']

    for ev in eventos:
        tipo = ev['data']['action']
        if tipo == deferimento:
            return 'deferido'
        elif tipo == desistencia:
            return 'desistencia'
        elif tipo == finalizado:
            return 'indeferido e finalizado'
        elif tipo == indeferido:
            return 'indeferido'
    # else aqui é do for-else
    else:
        print(tipo)
        return 'em analise'

@json_resp(list = False)
def get_proc_mdata(proc, *args, json_alike = True):
    '''Gets process-related data'''

    # em alguns casos podemos chamar a chave direto
    # porque tem padrão nos dados
    dados = [
        b_resp('num_protocolo',
               'Número de protocolo no Aprova Digital',
               proc['nP']),
        b_resp('dt_protocolo',
               'Data de protocolo',
               proc['created_at']),
        b_resp('dt_ultima_atualiz',
               'Última atualização',
               proc['updated_at']),
        b_resp('num_proc_sei',
               'Número de processo SEII',
               proc.get_m(['sei'])\
               .get_m(['txtCodigoProcedimentoFormatado'], None)),
        b_resp('assunto',
               'Assunto da solicitação',
               proc['config_metadata']['title'],
               ),
        b_resp('status',
               'Situação da solicitação',
               status_processo(proc))
    ]

    return dados