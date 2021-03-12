import functools
from fastapi import HTTPException
from utilities.proj_exceptions import ProcessoForadoPadrao, ProcessNotFound
from utilities.my_tools import dict_resp, dict_resp_list, hack_get_default_param

def treat_proc_num_out_of_pattern(func):

    @functools.wraps(func)
    def wraped(*args, **kwargs):
        try:
            resp = func(*args, **kwargs)
            return resp
        except ProcessoForadoPadrao as e:
            raise HTTPException(400, detail = str(e))
    return wraped

def treat_proc_not_found(func):

    @functools.wraps(func)
    def wraped(*args, **kwargs):
        try:
            resp = func(*args, **kwargs)
            return resp
        except ProcessNotFound as e:
            raise HTTPException(404, detail = str(e))
    return wraped

def json_resp(list = False):
    def decorator(func):
        @functools.wraps(func)
        def wraped(*args, **kwargs):

            json_alike = kwargs.get('json_alike')
            if json_alike is None:
                json_alike = hack_get_default_param(func, 'json_alike')
            resp = func(*args, **kwargs)
            if json_alike:
                if list:
                    resp = dict_resp_list(resp)
                else:
                    resp = dict_resp(resp)
            return resp
        return wraped
    return decorator

def encapsulate_response(func):

    @functools.wraps(func)
    def wraped(*args, **kwargs):
        try:
            resp = func(*args, **kwargs)
            return {'sucess' : True, 'data' : resp}
        except HTTPException as e:
            raise e
    return wraped

### mascaras dados

def mascara_sql(sql):
    sql = str(sql)
    if '.' not in sql:
        sql = '.'.join([sql[:3], sql[3:6], sql[6:10]]) + f'-{sql[-1]}'

    return sql
def apply_mascara_sql(dados):

    for terreno in dados:
        for i, campo in enumerate(terreno):
            if campo['label'] == 'tipo_identificacao' and 'sql' in str(campo['value']).lower():
                campo['value'] = 'SQL' #aproveitando para padronizar para SQL
                campo_sql = terreno[i+1]
                assert campo_sql['label'] == 'identificacao_terreno'
                sql_origi = campo_sql['value']
                campo_sql['value'] = mascara_sql(sql_origi)

def mascara_sql_decor(func):

    @functools.wraps(func)
    def wraped(*args, **kwargs):

        dados = func(*args, **kwargs)
        apply_mascara_sql(dados)

        return dados

    return wraped

def mascara_codlog(codlog):
    codlog = str(codlog)
    if '-' not in codlog:
        codlog = codlog[:-1] + f'-{codlog[-1]}'

    return codlog

def apply_mascara_codlog(dados):

    for terreno in dados:
        for campo in terreno:
            if campo['label'] == 'codlog':
                campo['value'] = mascara_codlog(campo['value'])

def mascara_codlog_decor(func):

    @functools.wraps(func)
    def wraped(*args, **kwargs):

        dados = func(*args, **kwargs)
        apply_mascara_codlog(dados)

        return dados

    return wraped
