from fastapi import FastAPI
from typing import Optional
from utilities.my_tools import get_proc_aleatorio, get_proc
from utilities.proj_decorators import treat_proc_num_out_of_pattern, treat_proc_not_found
from process_data.responsavel_imovel import dados_resps_imovel
from process_data.metadados_processo import get_proc_mdata
from process_data.dados_terreno import get_dados_terrenos

app = FastAPI()

@app.get("/responsavel_imovel/")
@treat_proc_not_found
@treat_proc_num_out_of_pattern
def dados_responsavel(num_proc: Optional[str] = None, json_alike: Optional[bool] = None):

    print(f'***********{num_proc}************')

    if json_alike is None:
        json_alike = True

    if num_proc:
        p = get_proc(num_proc)
    else:
        p = get_proc_aleatorio()

    return dados_resps_imovel(p, json_alike = json_alike)

@app.get("/metadados_dados_processo/")
@treat_proc_not_found
@treat_proc_num_out_of_pattern
def metadados_processo(num_proc: Optional[str] = None, json_alike: Optional[bool] = None):

    print(f'***********{num_proc}************')

    if json_alike is None:
        json_alike = True

    if num_proc:
        p = get_proc(num_proc)
    else:
        p = get_proc_aleatorio()

    return get_proc_mdata(p, json_alike = json_alike)

@app.get("/dados_terreno/")
@treat_proc_not_found
@treat_proc_num_out_of_pattern
def dados_terrenos(num_proc: Optional[str] = None, json_alike: Optional[bool] = None):

    print(f'***********{num_proc}************')

    if json_alike is None:
        json_alike = True

    if num_proc:
        p = get_proc(num_proc)
    else:
        p = get_proc_aleatorio()

    return get_dados_terrenos(p, json_alike = json_alike)