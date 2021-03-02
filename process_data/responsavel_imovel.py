from utilities.my_tools import b_resp
from utilities.proj_decorators import json_resp

def _build_address_respo(respo):
    '''Build address info by parsing address related keys'''

    endereco = [respo.get_m(['rua_proprietario'], None),
                respo.get_m(['numero_proprietario'], None),
                respo.get_m(['complemento_prop'], None),
                respo.get_m(['bairro_proprietario'], None),
                respo.get_m(['cidade_proprietario'], None),
                respo.get_m(['uf-proprietario'], None)
                ]
    endereco = [item for item in endereco if item is not None]

    if not endereco:
        return None

    endereco = ', '.join(endereco)

    return endereco

def __treat_cep(respo):

    cep = respo.get_m(['cep_proprietario', 'cep'], None)

    #trata para os casos de cep com consultade webservice
    if 'input' in cep:
        cep = cep.get_m(['input'])

    return cep

def __doc_respo_complex(respo, dados):

    doc = respo.get_m(['cpfcnpj_proprietario'])

    dados_doc = [b_resp(
        'doc',
        'Número do documento do responsável pelo imóvel',
        doc.get_m(['cpfCnpj'])
    ),
        b_resp(
            'tipo_doc',
            'Tipo de documento do responsável pelo imóvel',
            doc.get_m(['type'], None))
    ]

    dados.extend(dados_doc)

    if doc.get_m(['type']) == 'cnpj':
        dados_responsavel_empresa = [
            b_resp('nome_resp_empresa',
                   'Nome do responsável pela empresa',
                   respo.get_m(['cpfcnpj_proprietario']).get_m(['nomeResp'])),

            b_resp('cpf_resp_empresa',
                   'CPF do responsável pela empresa',
                   respo.get_m(['cpfcnpj_proprietario', 'cnpj_proprietario']).get_m(['cpfResp']))
        ]
        dados.extend(dados_responsavel_empresa)

def __doc_respo_flat_cnpj(respo, dados):

    dados_doc = [b_resp(
        'doc',
        'Número do documento do responsável pelo imóvel',
        respo.get_m(['cnpj_proprietario'])
    ),
        b_resp(
            'tipo_doc',
            'Tipo de documento do responsável pelo imóvel',
            'cnpj')
    ]

    dados_responsavel_empresa = [
        b_resp('nome_resp_empresa',
               'Nome do responsável pela empresa',
               respo.get_m(['representante_proprietario'])),

        b_resp('cpf_resp_empresa',
               'CPF do responsável pela empresa',
               respo.get_m(['cpf_proprietario']))
    ]

    dados.extend(dados_doc)
    dados.extend(dados_responsavel_empresa)

def __doc_respo_flat_cpf(respo, dados):
    dados_doc = [b_resp(
        'doc',
        'Número do documento do responsável pelo imóvel',
        respo.get_m(['cpf_proprietario'])
    ),
        b_resp(
            'tipo_doc',
            'Tipo de documento do responsável pelo imóvel',
            'cpf')
    ]

    dados.extend(dados_doc)
    dados.extend(dados_responsavel_empresa)

def __treat_doc_respo(respo):

    dados = []

    if 'cpfcnpj_proprietario' in respo:

        __doc_respo_complex(respo, dados)

    elif 'cnpj_proprietario' in respo:

        __doc_respo_flat_cnpj(respo, dados)

    elif 'cpf_proprietario' in respo:

        __doc_respo_flat_cpf(respo, dados)

    else:
        raise RuntimeError(f'Resposta não esperada: {respo}')

    return dados


def _dados_um_resp(respo):
    '''Parse all the data for one of the owner's info'''

    dados = [
        b_resp(
            'nome',
            'Nome do responsável pelo imóvel',
            respo.get_m(['nome-proprietario'], None)),
        b_resp(
            'tipo_vinculo',
            'Tipo de vínculo do responsável pelo imóvel',
            respo.get_m(['tipo_vinculo_proprietario',
                         'tipo_vinculo'], None)),
        b_resp(
            'email',
            'E-mail do responsável pelo imóvel',
            respo.get_m(['email_proprietario'], None)),

        b_resp(
            'endereco',
            'Endereço do responsável pelo imóvel',
            _build_address_respo(respo)),

        b_resp('cep',
               'CEP do responsável pelo imóvel',
               __treat_cep(respo)),

        #NÃO CONSEGUI IDENTIFICAR NENHUM PROCESSO COM INFORMAÇÃO DE TELEFONE DO RESP
        b_resp('telefone',
               'Telefone do responsável pelo imóvel',
               'Informação Não Disponível')
    ]

    dados.extend(__treat_doc_respo(respo))

    return dados

@json_resp(list = True)
def dados_resps_imovel(proc, *args, json_alike = True):
    '''Get's info for all building owners'''

    resps_imovel = proc.get_m(['last_version']) \
        .get_m(['proprietario'], [])

    dados_resps = []
    for respo in resps_imovel:
        dados_resps.append(_dados_um_resp(respo))

    return dados_resps