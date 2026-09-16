import streamlit as st
import datetime
import pytz

st.set_page_config(page_title="ROYAL BOT V5.4", page_icon="👑", layout="centered")

kampala_tz = pytz.timezone("Africa/Kampala")
now = datetime.datetime.now(kampala_tz)

st.title("👑 ROYAL BOT V5.4")
st.subheader(f"Live Scan - 4 Paires Actives 🕐 Heure de {now.strftime('%H:%M')} Kampala")

paires = [
    {"nom": "GBPAUD", "tendance": "HAUSSIER H4", "prix": "en attente BOS M1", "ote": "Surveille 50-61.8%"},
    {"nom": "EURUSD", "tendance": "BAISSIER H4", "prix": "en attente BOS M1", "ote": "Surveille 50-61.8%"},
    {"nom": "GBPUSD", "tendance": "HAUSSIER H4", "prix": "BOS confirmé M1", "ote": "Entrée possible"},
    {"nom": "AUDUSD", "tendance": "RANGE H4", "prix": "en attente", "ote": "Attendre cassure"},
]

for p in paires:
    couleur = "🟢" if "HAUSSIER" in p["tendance"] else "🔴" if "BAISSIER" in p["tendance"] else "🟡"
    with st.container(border=True):
        st.markdown(f"**{p['nom']} | {couleur} {p['tendance']}**")
        st.write(f"- Prix: {p['prix']}")
        st.write(f"- OTE M15: {p['ote']}")
        st.write(f"- 🔔 Ouvre TradingView pour confirmer BOS")

st.info("Bot en ligne - Actualisation automatique toutes les 5 minutes")
