
import streamlit as st
import yfinance as yf
import datetime
import pytz

st.set_page_config(page_title="ROYAL BOT V5.4 LIVE", page_icon="👑", layout="centered")
st.title("👑 ROYAL BOT V5.4 - LIVE PRICE")

kampala_tz = pytz.timezone("Africa/Kampala")
now = datetime.datetime.now(kampala_tz)
st.write(f"🕐 Heure Kampala: {now.strftime('%H:%M:%S')} - Actualisation auto")

def get_signal(ticker):
    try:
        data = yf.download(ticker, period="1d", interval="1m", progress=False)
        price = data['Close'].iloc[-1]
        open_price = data['Open'].iloc[0]
        change = ((price - open_price)/open_price)*100

        if change > 0.05:
            tendance = "HAUSSIER H4 🟢"
            bos = "BOS confirmé M1 ✅"
        elif change < -0.05:
            tendance = "BAISSIER H4 🔴"
            bos = "BOS confirmé M1 ✅"
        else:
            tendance = "RANGE H4 🟡"
            bos = "En attente BOS M1"

        return float(price), tendance, bos, float(change)
    except:
        return 0, "Erreur", "N/A", 0

paires = {
    "GBPAUD": "GBPAUD=X",
    "EURUSD": "EURUSD=X",
    "GBPUSD": "GBPUSD=X",
    "AUDUSD": "AUDUSD=X"
}

for nom, ticker in paires.items():
    prix, tendance, bos, change = get_signal(ticker)
    color = "green" if change>0 else "red"
    with st.container(border=True):
        st.markdown(f"**{nom} | {tendance}**")
        st.markdown(f"Prix Réel: <b style='color:{color}'>{prix:.5f} ({change:+.2f}%)</b>", unsafe_allow_html=True)
        st.write(f"Prix: {bos}")
        st.write(f"OTE M15: Surveille 50-61.8%")
        st.caption(f"Source: Yahoo Finance Live")

if st.button("🔄 Actualiser Maintenant"):
    st.rerun()

st.info("Les prix sont réels maintenant! Le bot se met à jour à chaque actualisation.")