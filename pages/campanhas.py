import pandas as pd
import plotly.express as px
import streamlit as st
from Isaloka import GraphAPI

st.header("Campaign status")
fb_api = open("tokens/token").read()
ad_acc = "956757482423549"
fb_graph_api = GraphAPI(ad_acc, fb_api)

insights = pd.DataFrame(fb_graph_api.get_insights()['data'])
campaign_status = pd.DataFrame(fb_graph_api.get_campaigns_status()['data'])
adset_status = pd.DataFrame(fb_graph_api.get_adset_status()['data'])
media_cpc = insights['cpc'].astype(float).mean()
media_cpm = insights['cpm'].astype(float).mean()
media_freq = insights['frequency'].astype(float).mean()
total_adsets = adset_status.shape[0]
adsets_ativos = adset_status[adset_status['status'] == 'ACTIVE'].shape[0]
adsets_inativos = adset_status[adset_status['status'] == 'PAUSED'].shape[0]

aba1, aba2 = st.tabs(["Campanhas", "Conjuntos de Anúncios"])

with aba1:
    st.header("Status das Campanhas")
    coluna1, coluna2, coluna3 = st.columns(3)
    with coluna1:
        st.metric("Total de Campanhas:", campaign_status.shape[0])
        st.metric("Campanhas Ativas:", campaign_status[campaign_status['status'] == 'ACTIVE'].shape[0])
        st.metric("Campanhas Inativas:", campaign_status[campaign_status['status'] == 'PAUSED'].shape[0])
    with coluna2:
        st.metric("CPC Médio:", f"{media_cpc:.2f}")
        st.metric("CPC Mínimo:", insights['cpc'].astype(float).min())
        st.metric("CPC Máximo:", insights['cpc'].astype(float).max())
    with coluna3:
        st.metric("CPM Médio:", f"{media_cpm:.2f}")
        st.metric("CPM Mínimo:", f"{insights['cpm'].astype(float).min():.2f}")
        st.metric("CPM Máximo:", f"{insights['cpm'].astype(float).max():.2f}")

with aba2:
    st.header("Status dos Conjuntos de Anúncios")
    coluna1, coluna2 = st.columns(2)
    with coluna1:
        st.metric("Total de conjuntos de anúncios:", total_adsets)
        st.metric("Conjuntos de anúncios Ativos:", adsets_ativos)
        st.metric("Conjuntos de anúncios Inativos:", adsets_inativos)
    with coluna2:
        st.metric("Frequência Média:", f"{media_freq:.2f}")
        st.metric("Frequência Mínima:", f"{insights['frequency'].astype(float).min():.2f}")
        st.metric("Frequência Máxima:", f"{insights['frequency'].astype(float).max():.2f}")
