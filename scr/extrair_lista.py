def extrair_lista(notas):
    '''Extrair lista com todos parametros das notas fiscais'''
    lista_xml=[]
    for i in notas:
        if i is not None:
            nota = i.read().decode("utf-8")
            lista_xml = nota.split('<')
    return lista_xml

def extrair_parametro(lista,parametro):
    for lista_tag in lista: 
        if parametro in lista_tag:
            lista_aux.append(lista_tag)
    parametros_nf=[]
    for index in range(0,len(lista_aux),len(parametro)): # Extrair lista com valores depurados das notas fiscais
        valor = lista_aux[index]
        valor = valor[len(parametro):]
        parametros_nf.append(valor)
    return parametros_nf