import pandas as pd
import streamlit as st
from Isaloka import *

#-----------------------------------------------------------------------------------------------------

# Load API token and ad account ID
fb_api = open("tokens/token").read()
ad_acc = "956757482423549"
fb_graph_api = GraphAPI(ad_acc, fb_api)

st.set_page_config(layout='wide')
st.title('Dashboard Isa')
#-----------------------------------------------------------------------------------------------------------
# Sidebar and header
st.header("Status de Campanha")
campaign_status = pd.DataFrame(fb_graph_api.get_campaigns_status(ad_acc)['data'])
st.write(campaign_status)


st.header("Status de Conjuntos de Anuncios")
adset_status = pd.DataFrame(fb_graph_api.get_adset_status(ad_acc)['data'])
st.write(adset_status)

st.header("Insights")
insights = pd.DataFrame(fb_graph_api.get_insights(ad_acc)['data'])
insights['date_start'] = pd.to_datetime(insights['date_start'], format='%Y-%m-%d')
insights['date_start'] = insights['date_start'].dt.strftime('%d/%m/%Y')
insights['date_stop'] = pd.to_datetime(insights['date_stop'], format='%Y-%m-%d')
insights['date_stop'] = insights['date_stop'].dt.strftime('%d/%m/%Y')

st.write(insights)

st.header("Dados Por Tempo de Campanha")
campaign_id = "120208363974670077"
data_over_time_data = fb_graph_api.get_data_over_time(campaign_id)
if 'data' in data_over_time_data:
    data_over_time = pd.DataFrame(data_over_time_data['data'])
    data_over_time['date_start'] = pd.to_datetime(data_over_time['date_start'], format='%Y-%m-%d')
    data_over_time['date_start'] = data_over_time['date_start'].dt.strftime('%d/%m/%Y')
    data_over_time['date_stop'] = pd.to_datetime(data_over_time['date_stop'], format='%Y-%m-%d')
    data_over_time['date_stop'] = data_over_time['date_stop'].dt.strftime('%d/%m/%Y')
else:
    st.error("No data over time available.")
    data_over_time = pd.DataFrame()

st.write(data_over_time)

#-----------------------------------------------------------------------------------------------------------


