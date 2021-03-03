from utilities.my_tools import b_resp
from utilities.proj_decorators import json_resp

@json_resp(list = False)
def get_proc_mdata(proc, *args, json_alike = True):
    '''Gets process-related data'''

    # em alguns casos podemos chamar a chave direto
    # porque tem padrão nos dados
    dados = [
        b_resp('num_protocolo',
               'Número de protocolo no Aprova Digital',
               proc['nP']),
        b_resp('num_proc_sei',
               'Número de processo SEII',
               proc.get_m(['sei']) \
               .get_m(['txtCodigoProcedimentoFormatado'], None)),
        b_resp('assunto',
               'Assunto da solicitação',
               proc['config_metadata']['title'],
               )
    ]

    return dados