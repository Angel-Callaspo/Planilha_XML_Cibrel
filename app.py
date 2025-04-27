import pandas as pd
import numpy as np
from pathlib import Path
from matplotlib import pyplot as plt
import plotly.express as px
import streamlit as st
import io
from PIL import Image

st.set_page_config(
    page_title="Extrair_imposto_nf_XML",
    page_icon="🧊",
    layout="wide",
    initial_sidebar_state="expanded")

lista_aux=[]
todas_nf=[]
lista_aux_icms=[]
lista_nota =[]
lista_iten = []
todos_icms=[]
lista_aux_pis=[]
todos_pis=[]
lista_aux_cofin=[]
todos_cofin=[]
lista_valor_notas = []
todos_valor_nota=[]

path= Path("LOGO.png")
imagem = Image.open(path) 
st.logo(image=imagem, size="large")

with st.sidebar:
    st.title('APP CIBREL: Carregue Nf_XML')
    notas_xml = st.file_uploader('Coloque aqui seus arquivos',accept_multiple_files=True,type=["xml"])
    st.write("F5, *Para recarregar!* :rocket:")

    for i in notas_xml: # Extrair lista com numeros das notas fiscais "nNF"
        if i is not None:
            nota = i.read().decode("utf-8")
            nota_separada = nota.split("<")
            
            lista_nota = nota.split('total')
            imposto_notas = str(lista_nota[1:2])
            separa_imposto = imposto_notas.split("<")
            
            num_iten = nota.count("det nItem")

            for lista_tag in nota_separada: 
              if "nNF" in lista_tag:
                lista_aux.append(lista_tag)
            
            for imposto in separa_imposto:
                if "vICMS>" in imposto:
                    lista_aux_icms.append(imposto)

            for imposto in separa_imposto:
                if "vPIS>" in imposto:
                    lista_aux_pis.append(imposto)

            for imposto in separa_imposto:
                if "vCOFINS>" in imposto:
                    lista_aux_cofin.append(imposto)
            
            for imposto in separa_imposto:
                if "vNF>" in imposto:
                    lista_valor_notas.append(imposto)

        lista_iten.append(num_iten)
        
    for index in range(0,len(lista_aux),4): # Extrair lista com valores depurados das notas fiscais "nNF"
        valor = lista_aux[index]
        valor = valor[4:]
        todas_nf.append(valor)

    for imp_icms in lista_aux_icms:
        if "/vICMS>" not in imp_icms:
            icms_valor = imp_icms[6:]
            todos_icms.append(icms_valor)

    for imp_pis in lista_aux_pis:
        if "/vPIS>" not in imp_pis:
            pis_valor = imp_pis[5:]
            todos_pis.append(pis_valor)

    for imp_cofin in lista_aux_cofin:
        if "/vCOFINS>" not in imp_cofin:
            cofin_valor = imp_cofin[8:]
            todos_cofin.append(cofin_valor)

    for valor_nota in lista_valor_notas:
        if "/vNF>" not in valor_nota:
            valor_nf = valor_nota[4:]
            todos_valor_nota.append(valor_nf)


imposto_ml_cibrel = {'N° Nfe':todas_nf,
                     'N° item\n(und)':lista_iten,
                     'ICMS\n(R$)':todos_icms,
                     'PIS\n(R$)':todos_pis,
                     'COFIN\n(R$)':todos_cofin,
                     'Valor Nfe\n(R$)':todos_valor_nota}

st.title(":blue[CIBREL:] :red[Tabela de Impostos]") 
df_imposto = pd.DataFrame(imposto_ml_cibrel)
st.dataframe(df_imposto)

st.write(f'Quantidade de Notas carregadas: <:green[{len(df_imposto)} Nfe]>')


def convert_for_download(df):
    output = io.BytesIO()
    with pd.ExcelWriter(output, engine='xlsxwriter') as writer:
        df.to_excel(writer, index=False)
    processed_data = output.getvalue()
    return processed_data


st.download_button(label="Baixar Excel",
                   data=convert_for_download(df_imposto),
                   file_name="imposto_cibrel.xlsx",
                   mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
                   type="primary")

