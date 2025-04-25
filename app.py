import pandas as pd
import numpy as np
from matplotlib import pyplot as plt
import plotly.express as px
import streamlit as st

st.set_page_config(
    page_title="Extrair_imposto_nf_XML",
    page_icon="🧊",
    layout="wide",
    initial_sidebar_state="expanded")

lista_aux=[]
todas_nf=[]
lista_aux_icms=[]
lista_nota =[]
notas = []
lista_icms=[]
todos_icms=[]
lista_aux_pis=[]
lista_pis=[]
todos_pis=[]
lista_aux_cofin=[]
lista_cofin=[]
todos_cofin=[]

with st.sidebar:
    st.title('APP CIBREL: Carregue Nf_XML')
    notas_xml = st.file_uploader('Coloque aqui seus arquivos',accept_multiple_files=True,type=["xml"])
    st.write("F5, *Para recarregar!* :rocket:")

    for i in notas_xml: # Extrair lista com numeros das notas fiscais "nNF"
        if i is not None:
            nota = i.read().decode("utf-8")
            lista_nota = nota.split('<')
            for lista_tag in lista_nota: 
                if "nNF" in lista_tag:
                    lista_aux.append(lista_tag)
            
            for lista_tag in lista_nota: # Extrair lista com impostos das notas fiscais "vICMS"
                if "vICMS>" in lista_tag:
                    lista_aux_icms.append(lista_tag)
                icms=str(lista_aux_icms[-4:-3])
            lista_icms.append(icms)

            for lista_tag in lista_nota: # Extrair lista com impostos das notas fiscais "vPIS"
                if "vPIS" in lista_tag:
                    lista_aux_pis.append(lista_tag)
                pis=str(lista_aux_pis[-2:-1])
            lista_pis.append(pis)

            for lista_tag in lista_nota: # Extrair lista com impostos das notas fiscais "vCOFINS"
                if "vCOFINS" in lista_tag:
                    lista_aux_cofin.append(lista_tag)
                cofin=str(lista_aux_cofin[-2:-1])
            lista_cofin.append(cofin)

    for index in range(0,len(lista_aux),4): # Extrair lista com valores depurados das notas fiscais "nNF"
        valor = lista_aux[index]
        valor = valor[4:]
        todas_nf.append(valor)

    for imp_icms in lista_icms: # Extrair lista com valores depurados dos imposto notas fiscais "vICMS"
        icms_valor = imp_icms[8:-2]
        todos_icms.append(icms_valor)

    for imp_pis in lista_pis: # Extrair lista com valores depurados dos imposto notas fiscais "vPIS"
        pis_valor = imp_pis[7:-2]
        todos_pis.append(pis_valor)

    for imp_cofin in lista_cofin: # Extrair lista com valores depurados dos imposto notas fiscais "vPIS"
        cofin_valor = imp_cofin[10:-2]
        todos_cofin.append(cofin_valor)

imposto_ml_cibrel = {'N° de Nota':todas_nf,
                     'ICMS':todos_icms,
                     'PIS':todos_pis,
                     'COFIN':todos_cofin}

st.title(":red[Tabela de imposto Mercado Livre <FULL>]")
df_imposto = pd.DataFrame(imposto_ml_cibrel)
st.dataframe(df_imposto)
