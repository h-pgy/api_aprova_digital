from utilities.my_tools import b_resp, timestamp_to_txt
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

def __aux_public_deferido(dados, proc):

        docs_publicados = get_docs_published(proc, json_alike=True)
        print(docs_publicados)
        for doc in docs_publicados:
            if doc.get('tipo_documento') == 'Despacho deferido':
                dados.append(b_resp('data_publicacao',
                                    'Data de publicação no Diário Oficial',
                                    doc.get('data_publicacao')))
                break
        #nao publicou ainda
        else:
            dados.append(b_resp('data_publicacao',
                            'Data de publicação no Diário Oficial',
                            None))

def __aux_public_indeferido(dados, proc):

        docs_publicados = get_docs_published(proc, json_alike=True)
        for doc in docs_publicados:
            if doc.get('tipo_documento') == 'Despacho indeferido':
                dados.append(b_resp('data_publicacao',
                                    'Data de publicação no Diário Oficial',
                                    doc.get('data_publicacao')))
                break
        #nao publicou ainda
        else:
            dados.append(b_resp('data_publicacao',
                                'Data de publicação no Diário Oficial',
                                None))

def __aux_dt_public(status, dados, proc):

    if status == 'deferido':
        __aux_public_deferido(dados, proc)

    elif status == 'indeferido' or status == 'indeferido e finalizado':
        __aux_public_indeferido(dados, proc)

    #nao tem nada para publicar
    else:
        dados.append(b_resp('data_publicacao',
                            'Data de publicação no Diário Oficial',
                            None))


@json_resp(list = True)
def get_docs_published(proc, *args, json_alike = True):
    '''Gets list of process's published documents'''

    docs = proc.get('sei', {}).get('dispatchedDocuments', [])
    dados = []
    for doc in docs:
        dados_doc = [
            b_resp(
                'data_publicacao',
                'Data de publicação do documento no Diário Oficial',
                timestamp_to_txt(doc.get('datPublicacao'))
            ),
            b_resp(
                'prazo_resposta',
                'Prazo em dias para resposta à publicação (p. ex. resposta Comunique-se)',
                doc.get('numPrazoComuniquese', None)
            ),
            b_resp('tipo_documento',
                   'Tipo de documento publicado',
                   doc.get('txtTipoDocumento')),
            b_resp(
                'num_id_doc',
                'Número identificador do documento no SEI',
                doc.get('numDocumento')
            )
        ]

        dados.append(dados_doc)
    if dados:
        return dados
    else:
        return [b_resp(
            'no_doc_found',
            'Nenhum documento foi encontrado',
            None
        )]

@json_resp(list = False)
def get_proc_mdata(proc, *args, json_alike = True):
    '''Gets process-related data'''

    # em alguns casos podemos chamar a chave direto
    # porque tem padrão nos dados

    status = status_processo(proc)
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
               status)
    ]

    #chama funcao auxiliar para devolver data de publicacao
    __aux_dt_public(status, dados, proc)

    return dados