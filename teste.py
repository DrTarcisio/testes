import yaml
from yaml.loader import SafeLoader
import streamlit_authenticator as stauth

import pyodbc
import pandas as pd
from datetime import datetime
from datetime import date
import streamlit as st
import streamlit_pandas as sp
from sqlalchemy import create_engine, text

# +
## Load Hash_pw

st.set_page_config(layout = "wide")

with open('config.yml') as file:
    config = yaml.load(file, Loader=SafeLoader)
# -

authenticator = stauth.Authenticate(
    config['credentials'],
    config['cookie']['name'],
    config['cookie']['key'],
    config['cookie']['expiry_days']
)

# +
st.header(f"Clínica de Anestesia de Muriaé - MG", divider="gray")

authenticator.login()

# +
# CARREGA MAIN, se senha correta

if st.session_state["authentication_status"] is False:
    st.error("Usuário/Senha inválido(a)")
elif st.session_state["authentication_status"] is None:
    st.warning("Digite usuário e senha")
elif st.session_state["authentication_status"]:
    
    

    st.write(f'Bem Vindo *{st.session_state["name"]}*')
    st.title(f'Clínica de Anestesia de Muriaé - MG')

    # DB Connection
    DRIVER = "ODBC Driver 17 for SQL Server"
    DATABASE_CONNECTION = f"mssql+pyodbc://11382CLIANEST:A4Q/JW_5U6f@customerdb001.gvinci.com.br/11382CLIANEST?driver={DRIVER}"

    engine = create_engine(DATABASE_CONNECTION)
    connection = engine.connect()
    # -

    connection.execute(text("""SELECT [NUMERO_DA_FICHA]
          ,[HOSPITAL]
          ,[DATA_INTERNACAO]
          ,[NOME_DO_PACIENTE]
          ,[DATA_DE_NASCIMENTO]
          ,[SEXO]
          ,[ASA]
          ,[COR]
          ,[CATEGORIA]
          ,[NOME_CONVENIO]
          ,[DIAGNOSTICO]
          ,[ESTADO_FISICO]
          ,[PRE_ANESTESICO]
          ,[ANESTESISTA]
          ,[AGENTES]
          ,[ANESTESIA]
          ,[CIRURGIA]
          ,[CIRURGIA_COMPL]
          ,[CIRURGIA_COMPL2]
          ,[CIRURGIAO1]
          ,[CIRURGIAO2]
          ,[CIRURGIAO3]
          ,[CIRURGIAO4]
          ,[OBSERVACAO]
          ,[OBSERVACAO2]
          ,[APTO]
          ,[SITUACAO]
          ,[VALOR]
          ,[IDADE]
          ,[DATAPAGAMENTO]
          ,[EMPRESA]

      FROM [dbo].[FICHA]"""))


    # Filtrando por Datas
    def data_inicial():
        data_inicio = '2023-01-01'
        data_fim = datetime.today().strftime('%Y-%m-%d')
        global a
        a = f"""SELECT [NUMERO_DA_FICHA]
              ,[HOSPITAL]
              ,[DATA_INTERNACAO]
              ,[NOME_DO_PACIENTE]
              ,[IDADE]
              ,[NOME_CONVENIO]
              ,[ANESTESISTA]
              ,[CIRURGIAO1]
              ,[OBSERVACAO]
              ,[SITUACAO]
              ,[VALOR]

          FROM [dbo].[FICHA]

          WHERE DATA_INTERNACAO BETWEEN '{data_inicio}' AND '{data_fim}'"""


    # +
    # df_filtrada['DATA_INTERNACAO'] = pd.to_datetime(df_filtrada['DATA_INTERNACAO']).dt.strftime('%Y/%m/%d')
    # -

    def load_data():
        data_inicial()
        global df
        global df_filtrada
        try:
            df = pd.read_sql(a, engine)
            df_filtrada = df.sort_values(['DATA_INTERNACAO'])
            df_filtrada['HOSPITAL'] = [(str(i).upper().strip()) for i in df_filtrada['HOSPITAL']]
            df_filtrada['IDADE'] = pd.to_numeric(df_filtrada['IDADE'], errors='coerce')
            df_filtrada['IDADE'] = df_filtrada['IDADE'].fillna(df_filtrada['IDADE'].mean())
        except:
            df = pd.read_sql(a, engine)
            df_filtrada = df.sort_values(['DATA_INTERNACAO'])
            df_filtrada['HOSPITAL'] = [(str(i).upper().strip()) for i in df_filtrada['HOSPITAL']]
            df_filtrada['IDADE'] = pd.to_numeric(df_filtrada['IDADE'], errors='coerce')
            df_filtrada['IDADE'] = df_filtrada['IDADE'].fillna(df_filtrada['IDADE'].mean())
        return df
    
    load_data()

    with st.sidebar:
        authenticator.logout()
        st.title("Particulares")

    create_data = {
        "SITUACAO" : "select",
        "NOME_CONVENIO" : "multiselect",
        "HOSPITAL": "multiselect",
        "CIRURGIAO1": "multiselect",
        "ANESTESISTA": "multiselect",
    }

    all_widgets = sp.create_widgets(df, create_data, ignore_columns=["VALOR","IDADE","NUMERO_DA_FICHA","NOME_DO_PACIENTE", "OBSERVACAO"])
    res = sp.filter_df(df, all_widgets)
    st.write(res)

# -




    # !streamlit run clianest.py
