from utilities.my_tools import find_apostilamentos, b_resp
from utilities.proj_decorators import json_resp
from process_data.metadados_processo import get_proc_mdata

@json_resp(list = True)
def apostilamentos_andamento(num_proc, *args, json_alike = True):

    apostilamentos = find_apostilamentos(num_proc)
    dados = []
    for apostila in apostilamentos:

        metadados = get_proc_mdata(apostila, json_alike = True)

        if metadados['status'] == 'em analise' or 'indeferido':

            dados.append(
                    get_proc_mdata(apostila, json_alike = False)
                   )

    return dados