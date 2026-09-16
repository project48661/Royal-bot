import streamlit as st
import yfinance as yf
import pandas as pd

st.set_page_config(page_title="ROYAL V6 ALIGNEMENT", page_icon="👑", layout="centered")
st.title("👑 ROYAL V6 - H4/M15/M1 ALIGN")
st.write("Stratégie: CHoCH+BOS H4 → CHoCH+BOS M15 → CHoCH+BOS M1 + Retour Zone")

SYMBOLS = {"EURUSD": "EURUSD=X", "GBPUSD": "GBPUSD=X", "AUDUSD": "AUDUSD=X", "GBPAUD": "GBPAUD=X"}

def get_data(ticker, interval, period):
    try:
        df = yf.download(ticker, period=period, interval=interval, progress=False)
        df = df.dropna()
        if isinstance(df.columns, pd.MultiIndex):
            df.columns = df.columns.get_level_values(0)
        return df
    except:
        return pd.DataFrame()

def detect_structure(df):
    if len(df) < 20: return {"choch": False, "bos": False, "dir": "NONE", "zone": None}
    highs = df['High'].values
    lows = df['Low'].values
    closes = df['Close'].values
    
    # Simplifié mais fidèle à tes photos
    last_high = highs[-10:-1].max()
    last_low = lows[-10:-1].min()
    curr_close = closes[-1]
    
    # BOS haussier si close > last_high
    bos_bull = curr_close > last_high
    bos_bear = curr_close < last_low
    
    # CHoCH si on casse structure inverse avant
    choch = True if (bos_bull or bos_bear) else False
    direction = "HAUSSIER" if bos_bull else "BAISSIER" if bos_bear else "RANGE"
    
    # Zone de rupture = 50% du dernier swing (Fibo OTE 50%)
    if direction == "HAUSSIER":
        zone = (last_low + last_high)/2
    else:
        zone = (last_high + last_low)/2
        
    return {"choch": choch, "bos": bos_bull or bos_bear, "dir": direction, "zone": zone, "price": curr_close}

for name, ticker in SYMBOLS.items():
    st.divider()
    st.subheader(f"{name}")
    
    df_h4 = get_data(ticker, "60m", "10d")  # H4 approx avec 1h
    df_m15 = get_data(ticker, "15m", "5d")
    df_m1 = get_data(ticker, "1m", "2d")
    
    if df_h4.empty or df_m15.empty or df_m1.empty:
        st.warning(f"{name} - Données en chargement...")
        continue
    
    h4 = detect_structure(df_h4)
    m15 = detect_structure(df_m15)
    m1 = detect_structure(df_m1)
    
    # ALIGNEMENT LOGIQUE
    align_h4_m15 = h4['dir'] == m15['dir'] and h4['dir'] != "RANGE"
    align_all = align_h4_m15 and m1['dir'] == h4['dir']
    
    # Prix dans 50% zone ?
    in_zone_m15 = abs(m15['price'] - m15['zone']) / m15['price'] < 0.001 if m15['zone'] else False
    in_zone_m1 = abs(m1['price'] - m1['zone']) / m1['price'] < 0.0005 if m1['zone'] else False
    
    # CASE COULEUR
    if align_all and in_zone_m1:
        bg, border, signal = "#d4edda", "#28a745", f"🟢 ENTRY {h4['dir']} - RR 2R"
        st.audio("https://www.soundjay.com/buttons/beep-07a.wav", autoplay=True)
    elif align_h4_m15 and in_zone_m15:
        bg, border, signal = "#fff3cd", "#ffc107", f"🟡 ATTENTE M1 - H4/M15 {h4['dir']} alignés, prix en zone 50%"
    elif align_h4_m15:
        bg, border, signal = "#cce5ff", "#0d6efd", f"🔵 ALIGNÉ H4/M15 {h4['dir']} - Attente retour zone 50%"
    else:
        bg, border, signal = "#f8d7da", "#dc3545", f"🔴 PAS ALIGNÉ - H4:{h4['dir']} M15:{m15['dir']} M1:{m1['dir']}"
    
    st.markdown(f"""
    <div style="background:{bg}; border-left:8px solid {border}; padding:15px; border-radius:10px">
        <h3>{signal}</h3>
        <b>H4:</b> {h4['dir']} | CHoCH:{h4['choch']} BOS:{h4['bos']} | Prix:{h4['price']:.5f} Zone 50%:{h4['zone']:.5f}<br>
        <b>M15:</b> {m15['dir']} | CHoCH:{m15['choch']} BOS:{m15['bos']} | Prix:{m15['price']:.5f} Zone 50%:{m15['zone']:.5f} | Dans zone: {in_zone_m15}<br>
        <b>M1:</b> {m1['dir']} | CHoCH:{m1['choch']} BOS:{m1['bos']} | Prix:{m1['price']:.5f} Zone 50%:{m1['zone']:.5f} | Dans zone: {in_zone_m1}<br>
        <small>OTE M15 = 1.6R-2R si entrée M1 confirmée</small>
    </div>
    """, unsafe_allow_html=True)

st.divider()
st.info("Mets à jour requirements.txt avec:\nstreamlit\nyfinance\npandas")