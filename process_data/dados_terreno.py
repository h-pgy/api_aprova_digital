from utilities.my_tools import b_resp, FlexKeyDict
from utilities.proj_decorators import json_resp, mascara_sql_decor, mascara_codlog_decor
from pprint import pprint

def __aux_end_flat(last_version):

    if 'endereco_obra' in last_version:
        #com hack para nao quebrar caso valor esteja nulo
        dados_end = [
            last_version['endereco_obra'][0].get('logradouro_rua'),
                      str(last_version['endereco_obra'][0].get('testada_rua', ''))]

        return ', '.join(dados_end)
    elif 'logradouro_rua' in last_version:

        dados_end = [
                    last_version.get('logradouro_rua'),
                    last_version.get('numero-predial'),
                    last_version.get('id-bairro')
                    ]

        return ', '.join([item for item in dados_end if item])

def __dados_terreno_flat(last_version):
    '''Neste modelo há apenas um SQL por solicitacao e os dados
    estão flat'''

    dados_terr = [
    b_resp('tipo_identificacao',
           'Tipo de identificação do imóvel - SQL ou Incra',
           last_version.get_m(['identificacao_imovel'])),
    b_resp('identificacao_terreno',
           'Código de identificação do terreno (SQL ou INCRA)',
           last_version.get_m(['campo_sql', 'cadastro_rural'])),
    b_resp('codlog',
          'Código do logradouro em que se situa a fachada do terreno',
          last_version.get_m(['codlog'])),
    b_resp('area_terreno_real',
           'Área real do terreno',
           last_version.get_m(['area_terreno_real'], None)),
    b_resp('area_escritura',
           'Área registrada em escritura',
           last_version.get_m(['escrituradoterreno'], None)),
    b_resp('cep',
           'CEP do terreno',
           last_version.get_m(['endereco-cep'])),
    b_resp('end_testada_principal',
           'Endereço da testada principal',
           __aux_end_flat(last_version)),
    b_resp('distrito',
           'Distrito em que se situa o imóvel',
           last_version.get_m(['id-bairro']))
    ]

    return dados_terr

def __aux_dados_area_escritura(last_version):

    return [b_resp('area_terreno_real',
               'Área real do terreno',
               last_version.get_m(['escrituradoterreno'], None)),
        b_resp('area_escritura',
               'Área registrada em escritura',
               last_version.get_m(['area_terreno_real'], None)),]

def __dados_terreno(terreno):

    aux_endereco = lambda x:', '.join([item for item in [
                                                    x['nome_logradouro'],
                                                    x['numero-predial'],
                                                    x.get('complemento_imovel'),
                                                    x.get('id-bairro')]
                                        if item])

    dados_terr = [
        b_resp('tipo_identificacao',
               'Tipo de identificação do imóvel - SQL ou Incra',
               terreno.get_m(['tipo_identificacao'])),
        b_resp('identificacao_terreno',
               'Código de identificação do terreno (SQL ou INCRA)',
               terreno.get_m(['campo_sql', 'cadastro_rural'])),
        b_resp('codlog',
               'Código do logradouro em que se situa a fachada do terreno',
               terreno.get_m(['codlog'])),
        b_resp('cep',
               'CEP do terreno',
               terreno.get_m(['endereco-cep'])),
        b_resp('end_testada_principal',
               'Endereço da testada principal',
               aux_endereco(terreno)),
        b_resp('distrito',
               'Distrito em que se situa o imóvel',
               terreno.get_m(['id-bairro']))
    ]

    return dados_terr

def __dados_terreno_declaratorio(terreno):

        aux_endereco = lambda x: ', '.join([
                                item for item in
                                [x.get('nome_logradouro'),
                                 str(x.get('iptu_numeracao')),
                                 x.get('complemento_imovel'),
                                 x.get('iptu_bairro')]
                                if item
                            ])

        dados_terr = [
        b_resp('tipo_identificacao',
               'Tipo de identificação do imóvel - SQL ou Incra',
               'sql'),
        b_resp('identificacao_terreno',
               'Código de identificação do terreno (SQL ou INCRA)',
               terreno.get_m(['sql']).get_m(['input'])),
        b_resp('codlog',
               'Código do logradouro em que se situa a fachada do terreno',
               terreno.get_m(['codlog'])),
        b_resp('cep',
               'CEP do terreno',
               terreno.get_m(['iptu_cep'])),
        b_resp('end_testada_principal',
               'Endereço da testada principal',
               aux_endereco(terreno)),
        b_resp('distrito',
               'Distrito em que se situa o imóvel',
               terreno.get_m(['subprefeitura'])),
        b_resp('area_terreno_real',
                'Área real do terreno',
                terreno.get_m(['area_terreno_real'], None)),
        b_resp('area_escritura',
                'Área registrada em escritura',
                terreno.get_m(['escrituradoterreno'], None))
        ]

        return dados_terr


@json_resp(list = True)
@mascara_sql_decor
@mascara_codlog_decor
def get_dados_terrenos(proc, *args, json_alike = True):
    '''Gets process-related data'''

    last_version = proc.get_m(['last_version'])

    if 'identificacao_terreno' in last_version or 'identificacao_imovel' in last_version:
        #MODELO ANTIGO - MAIS SIMPLES

        dados = __dados_terreno_flat(last_version)

        #ainda que nesse caso haja apenas um terreno, nos outros casos podem ser vários, por isso lista
        print(proc['config_metadata']['title'])
        return [dados]

    elif 'dadosterreno' in last_version and\
            type(last_version['dadosterreno']) is list:
        #MODELO MAIS RECENTE - COM VARIOS LOTES
        dados = []
        terrenos = proc.get_m(['last_version']).get_m(['dadosterreno', 'identificacao_imovel'])

        for terreno in terrenos:
            dados_terreno = __dados_terreno(terreno)
            dados_terreno.extend(__aux_dados_area_escritura(last_version))
            dados.append(dados_terreno)
        print(proc['config_metadata']['title'])
        return dados

    elif 'terreno' in last_version and\
        type(last_version['terreno']) is list:
        #MODELO DO PROCESSO DECLARATORIO HIS
        dados = []
        for terreno in last_version['terreno']:
            dados.append(__dados_terreno_declaratorio(FlexKeyDict(terreno)))
        print(proc['config_metadata']['title'])
        return dados

    else:
        #NAO PARSEOU: PRINTA LOG E LEVANTA ERRO
        pprint(last_version)
        print(proc['config_metadata']['title'])
        raise RuntimeError(f'Formato inesperado')