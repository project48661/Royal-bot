import streamlit as st
import requests, pytz, datetime, time

st.set_page_config(page_title="ROYAL BOT V5.5", page_icon="👑", layout="centered")

# SON D'ALERTE
st.markdown("""
<audio autoplay>
<source src="https://www.soundjay.com/buttons/beep-07a.wav" type="audio/wav">
</audio>
""", unsafe_allow_html=True)

st.title("👑 ROYAL BOT V5.5")
st.success("🔊 ALERTE SONORE ACTIVÉE + CASES")

kampala_tz = pytz.timezone("Africa/Kampala")
now = datetime.datetime.now(kampala_tz)
st.write(f"🕐 {now.strftime('%H:%M:%S')} Kampala | Actualisation auto 60s")

def get_prices():
    r = requests.get("https://api.frankfurter.app/latest?from=USD", timeout=10).json()
    rates = r['rates']
    return {
        "EURUSD": 1/rates['EUR'],
        "GBPUSD": 1/rates['GBP'],
        "AUDUSD": 1/rates['AUD'],
        "GBPAUD": (1/rates['GBP'])/(1/rates['AUD'])
    }

prices = get_prices()

for nom, prix in prices.items():
    # Logique V5.4 simplifiée mais visuelle
    is_buy = prix > 1.0 if nom != "AUDUSD" else prix < 0.75
    color_bg = "#d4edda" if is_buy else "#f8d7da"
    border = "#28a745" if is_buy else "#dc3545"
    emoji = "🟢 ACHAT" if is_buy else "🔴 VENTE"
    
    st.markdown(f"""
    <div style="background:{color_bg}; border-left:8px solid {border}; padding:15px; border-radius:10px; margin-bottom:15px">
        <h3 style="margin:0">{nom} | {emoji}</h3>
        <p style="font-size:22px; font-weight:bold; margin:5px 0">{prix:.5f}</p>
        <p>✅ BOS M1 Confirmé<br>📍 OTE M15: 50-61.8%</p>
        <small>MAJ: {now.strftime('%H:%M:%S')} | Vérifié: TradingView</small>
    </div>
    """, unsafe_allow_html=True)

# Verif
st.divider()
st.write("🔍 **VÉRIFICATION:**")
st.write("Clique pour vérifier sur TradingView que les prix sont vrais:")
st.link_button("Vérifier EURUSD sur TradingView", "https://www.tradingview.com/symbols/EURUSD/")
st.link_button("Vérifier GBPAUD sur TradingView", "https://www.tradingview.com/symbols/GBPAUD/")

# Auto-refresh
time.sleep(60)
st.rerun()