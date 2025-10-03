import streamlit as st
import pandas as pd
from datetime import datetime
from st_aggrid import AgGrid, GridOptionsBuilder

st.set_page_config(layout="wide")

uploaded_files = st.file_uploader("Choose a file", accept_multiple_files=True)
xls = []
sheet = []
sheet_names = []

for i, uploaded_file in enumerate(uploaded_files):
    if uploaded_file is not None:
        st.write(f"### Arquivo: {uploaded_file.name}")

        if uploaded_file.name.endswith("csv"):
            dataframe = pd.read_csv(uploaded_file, sep=None, engine='python', dtype=str)
            # Usando AgGrid no lugar de st.write
            gb = GridOptionsBuilder.from_dataframe(dataframe)
            gb.configure_pagination(paginationAutoPageSize=True)  # paginação automática
            gb.configure_side_bar()  # barra lateral com filtros
            gridOptions = gb.build()
            AgGrid(dataframe, gridOptions=gridOptions, height=500, fit_columns_on_grid_load=True)

        elif uploaded_file.name.endswith("parquet"):
            dataframe = pd.read_parquet(uploaded_file)
            gb = GridOptionsBuilder.from_dataframe(dataframe)
            gb.configure_pagination(paginationAutoPageSize=True)
            gb.configure_side_bar()
            gridOptions = gb.build()
            AgGrid(dataframe, gridOptions=gridOptions, height=500, fit_columns_on_grid_load=True)

        elif uploaded_file.name.endswith("xlsx"):
            xls.append(pd.ExcelFile(uploaded_file))
            sheet_names.append(xls[i].sheet_names)
            sheet.append(st.selectbox(f"Escolha uma aba para o arquivo {uploaded_file.name}", sheet_names[i]))
            df = pd.read_excel(uploaded_file, sheet_name=sheet[i])

            st.write(f"Dados da aba {sheet[i]}:")
            gb = GridOptionsBuilder.from_dataframe(df)
            gb.configure_pagination(paginationAutoPageSize=True)
            gb.configure_side_bar()
            gridOptions = gb.build()
            AgGrid(df, gridOptions=gridOptions, height=500, fit_columns_on_grid_load=True)
