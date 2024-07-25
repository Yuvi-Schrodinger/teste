import pandas as pd
import plotly.graph_objects as go
import plotly.express as px
import streamlit as st
from Isaloka import *


fb_api = st.secrets['db_token']
ad_acc = "956757482423549"
fb_graph_api = GraphAPI(ad_acc, fb_api)

st.header("Gráficos e Visualizações")
campaign_status = pd.DataFrame(fb_graph_api.get_campaigns_status(ad_acc)['data'])
campaign_status_count = campaign_status['status'].value_counts().reset_index()
campaign_status_count.columns = ['status', 'count']
campaign_id = "120208363974670077"
data_over_time_data = fb_graph_api.get_data_over_time(campaign_id)
data_over_time = pd.DataFrame(data_over_time_data['data'])
data_over_time['date_start'] = pd.to_datetime(data_over_time['date_start'])
data_over_time_sorted_cpm = data_over_time.sort_values(by='cpm',ascending=False)
data_over_time_sorted_cpc = data_over_time.sort_values(by='cpc',ascending=False)

# CPC e CPM ao longo do tempo
st.header("CPC e CPM ao Longo do Tempo")
  
fig = go.Figure(go.Bar(x=data_over_time_sorted_cpc['date_start'], y=data_over_time_sorted_cpc['cpc'], name='CPC'))


# Atualizar layout do gráfico
fig.update_layout(
    title="CPC ao Longo do Tempo com Linhas",
    xaxis_title="Data",
    yaxis_title="CPC",
    template='plotly_white'
)

# Exibir gráfico
st.plotly_chart(fig)
fig = go.Figure(go.Bar(x=data_over_time_sorted_cpm['date_start'], y=data_over_time_sorted_cpm['cpm'], name='CPM'))
st.plotly_chart(fig)

#_______________________________________________________________________________________________________________________________________________________________________________


#_______________________________________________________________________________________________________________________________________________________________________________
# Status dos Conjuntos de Anúncios
st.header("Status dos Conjuntos de Anúncios")
# Agrupar e contar o status dos conjuntos de anúncios
adset_status = pd.DataFrame(fb_graph_api.get_adset_status(ad_acc)['data'])
adset_status_count = adset_status['status'].value_counts().reset_index()
adset_status_count.columns = ['status', 'count']

fig_adset_status = px.pie(
    adset_status_count,
    names='status',
    values='count',
    title='Distribuição do Status dos Conjuntos de Anúncios',
    template='plotly_white'
)
st.plotly_chart(fig_adset_status)


