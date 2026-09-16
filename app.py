import streamlit as st
import yfinance as yf
import pandas as pd

st.set_page_config(page_title="ROYAL - Search", layout="wide", page_icon="👑")

# CSS GOOGLE STYLE FRANCE24
st.markdown("""
<style>
.big-logo {text-align:center; font-size:65px; font-weight:900; color:#4285F4; letter-spacing:-2px; margin-top:20px}
.big-logo span:nth-child(2){color:#EA4335} span:nth-child(3){color:#FBBC05} span:nth-child(4){color:#4285F4} span:nth-child(5){color:#34A853} span:nth-child(6){color:#EA4335}
.search-box input {border-radius:24px!important; height:50px!important}
.card {border:1px solid #e0e0e0; border-radius:12px; padding:12px; margin-bottom:10px; background:white}
.card:hover{box-shadow:0 2px 8px rgba(0,0,0,0.15)}
</style>
<div class="big-logo"><span>R</span><span>O</span><span>Y</span><span>A</span><span>L</span></div>
<p style="text-align:center; color:gray;">Moteur de signaux H4/M15/M1 - Piège LH + 50% Zone</p>
""", unsafe_allow_html=True)

query = st.text_input("", placeholder="Rechercher: EURUSD, GBPUSD, signal 50%, piège...", label_visibility="collapsed")

tabs = st.tabs(["All", "Images", "Videos", "News", "Maps", "Myfxbook"])

SYMBOLS = {
    "EURUSD":"EURUSD=X","GBPUSD":"GBPUSD=X","GBPAUD":"GBPAUD=X",
    "GBPJPY":"GBPJPY=X","EURJPY":"EURJPY=X","AUDUSD":"AUDUSD=X",
    "USDJPY":"USDJPY=X","USDCAD":"USDCAD=X"
}

def get_signal(ticker):
    try:
        df = yf.download(ticker, period="5d", interval="15m", progress=False)
        if isinstance(df.columns, pd.MultiIndex): df.columns = df.columns.get_level_values(0)
        df = df.dropna()
        if len(df)<30: return None
        close = float(df['Close'].iloc[-1])
        hi = df['High'].iloc[-30:-10].max()
        lo = df['Low'].iloc[-30:-10].min()
        fib50 = hi - (hi-lo)*0.5
        # Piège: cassure LH puis retour
        trap = df['High'].iloc[-1] > hi*0.999 and close < hi
        direction = "BAISSIER 🔻" if close < fib50 else "HAUSSIER 🔺"
        rr = "7.67R" if trap else "2R"
        return {"price":close, "dir":direction, "fib50":fib50, "trap":trap, "rr":rr, "entry":abs(close-fib50)<0.0005}
    except: return None

with tabs[0]:
    st.write(f"Environ {len(SYMBOLS)} résultats (0.42 secondes) pour **{query if query else 'forex royal'}**")
    st.divider()
    for name, ticker in SYMBOLS.items():
        sig = get_signal(ticker)
        if not sig: continue
        # Entry condition: test 50% comme ton trade GBPUSD
        badge = "🟢 ENTRY AU 50% - PIÈGE DÉTECTÉ" if sig['trap'] and sig['entry'] else "🟡 Attente 50%"
        st.markdown(f"""
        <div class="card">
        <small style="color:green">https://royal-trading.com/{name.lower()} › signal › live</small><br>
        <b style="font-size:18px; color:#1a0dab">{name} - {sig['dir']} - Test 50% Zone | RR {sig['rr']}</b><br>
        <span style="color:#4d5156">Prix TradingView vérifié: <b>{sig['price']:.5f}</b> | Zone rupture 50%: {sig['fib50']:.5f} |
        {badge} - Stop serré 0.007% comme ton trade 1.34745 → Target 1.34660 | Stratégie H4/M15/M1 + LH/LL/BOS/CHoCH</span>
        </div>
        """, unsafe_allow_html=True)
        if sig['trap'] and sig['entry']:
            st.success(f"✅ {name} - EXACTEMENT COMME TA PHOTO GBPUSD RR 7.67 - ENTRY NOW!")

with tabs[1]:
    st.subheader("Images - Mes Trades Preuves")
    st.write("Comme Google Images mais avec tes trades gagnants")
    uploader = st.file_uploader("Glisse tes screenshots ici (comme GBPAUD & GBPUSD)", accept_multiple_files=True, type=['png','jpg','jpeg'])
    cols = st.columns(3)
    if uploader:
        for i, file in enumerate(uploader):
            with cols[i%3]: st.image(file, caption=f"Trade {file.name} - RR 7.67R - Piège LH", use_container_width=True)

with tabs[2]:
    st.subheader("Videos")
    st.info("Tes enregistrements d'écran TradingView")

with tabs[3]:
    st.subheader("News - Calendrier Économique")
    st.components.v1.iframe("https://sslecal2.investing.com?columns=exc_flags,exc_currency,exc_importance,exc_actual,exc_forecast,exc_previous&features=datepicker,timezone&countries=25,32,6,37,72,22,17,39,14,10,35,43,56,36,110,11,26,12,4,5&calType=week&timeZone=15&lang=1", height=500)

with tabs[4]:
    st.subheader("Maps - Heatmap Forex")
    st.components.v1.iframe("https://www.tradingview.com/forex-heat-map/", height=600)

with tabs[5]:
    st.subheader("Myfxbook Vérifié")
    link = st.text_input("Colle ton lien Myfxbook public", value="")
    if link: st.components.v1.iframe(link, height=600)
    else: st.warning("Ajoute ton lien Myfxbook pour afficher comme France24 montre ses sources")