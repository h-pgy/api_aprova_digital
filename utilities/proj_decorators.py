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