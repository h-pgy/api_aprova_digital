from utilities.my_tools import find_estandes, b_resp
from utilities.proj_decorators import json_resp
from process_data.metadados_processo import get_proc_mdata
from process_data.dados_terreno import get_dados_terrenos
from process_data.responsavel_imovel import dados_resps_imovel

@json_resp(list = True)
def dados_estandes_existentes(num_proc, *args, json_alike = True):

    estandes = find_estandes(num_proc)
    dados = []
    for estande in estandes:

        dados_estande = [
            b_resp('metadados_processo',
                   'Dados relacionados ao processo de Estande de Vendas',
                   get_proc_mdata(estande, json_alike = False)),
            b_resp('dados_resps_imovel',
                   'Dados dos responsáveis pelo imóvel em que se situa o Estande de Vendas',
                   dados_resps_imovel(estande, json_alike=False)),
            b_resp('dados_terrenos',
                   'Dados relacionados ao(s) terreno(s) em que se situa o Estande de Vendas',
                   get_dados_terrenos(estande, json_alike=False)),
        ]

        dados.append(dados_estande)

    return dados

@json_resp(list = True)
def estandes_deferidos(num_proc, *args, json_alike = True):

    estandes = find_estandes(num_proc)
    dados = []
    for estande in estandes:

        metadados = get_proc_mdata(estande, json_alike = True)

        if metadados['status'] == 'deferido':

            dados.append(
                    get_proc_mdata(estande, json_alike = False)
                   )

    return dados