import streamlit as st
import pandas as pd
from datetime import datetime

st.set_page_config(layout="wide")

uploaded_files = st.file_uploader("Choose a file", accept_multiple_files=True)
xls = []
sheet = []
sheet_names = []
for i, uploaded_file in enumerate(uploaded_files):
    if uploaded_file is not None:
        st.write(f"""
        # Arquivo: {uploaded_file.name}
        """)
        if uploaded_file.name[-3:] == 'csv':
            dataframe = pd.read_csv(uploaded_file, sep=None, engine='python', dtype=str)
            #dataframe = pd.read_csv(uploaded_file, sep='^', index_col=False, engine='python', dtype=str)
            #dataframe = pd.read_csv(uploaded_file, sep=";")
            st.write(dataframe)

        elif uploaded_file.name[-7:] == 'parquet':
            dataframe = pd.read_parquet(uploaded_file)
            #caminho = '/home/cassio/Downloads/'

            #data = datetime.now().strftime('%Y-%m-%d %H')
            #file_parquet = f"{caminho}/plurix-{data}.xlsx"
            #dataframe.to_excel(file_parquet, index=False)

            st.write(dataframe)

            


        elif uploaded_file.name[-4:] == 'xlsx':

            xls.append(pd.ExcelFile(uploaded_file))  # Usar append para adicionar o ExcelFile
            sheet_names.append(xls[i].sheet_names)  # Adicionar as abas

            # Selecionar uma aba para o arquivo atual
            sheet.append(st.selectbox(f"Escolha uma aba para o arquivo {uploaded_file.name}", sheet_names[i]))

            # Ler os dados da aba selecionada
            df = pd.read_excel(uploaded_file, sheet_name=sheet[i])

            # Mostrar os dados da aba selecionada
            st.write(f"Dados da aba {sheet[i]}:")
            st.write(df)
