
<!DOCTYPE html>
<html>
<head>
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>Royal Bot V5.4</title>
<style>
body{font-family:sans-serif;background:#0e1117;color:white;padding:15px}
.card{background:#1f2937;padding:15px;border-radius:12px;margin:10px 0}
.green{color:#00ff88}.red{color:#ff4444}
.setup{background:#00ff88;color:black;padding:8px;border-radius:8px;font-weight:bold}
</style>
</head>
<body>
<h1>👑 ROYAL BOT V5.4</h1>
<p id="time"></p>
<div id="data">Chargement GBPAUD...</div>
<script>
function refresh(){
document.getElementById('time').innerText = new Date().toLocaleString('fr-FR',{timeZone:'Africa/Kampala'}) + " Kampala";
document.getElementById('data').innerHTML = `
<div class="card"><h3>GBPAUD | <span class="green">🟢 HAUSSIER H4</span></h3>
Prix: en attente BOS M1<br>OTE M15: Surveille 50-61.8%<br><br>
<div class="setup">🔔 Ouvre TradingView pour confirmer BOS</div></div>
<div class="card"><h3>GBPUSD | <span class="green">🟢 HAUSSIER</span></h3>Attente CPI 09h Kampala demain</div>
<div class="card"><h3>GOLD | <span class="red">🔴 BAISSIER</span></h3>Pause jusqu'à FED 21h</div>
<p style="background:orange;color:black;padding:10px;border-radius:8px">⚠️ FED demain 21h Kampala - Pas de trade 19h-22h</p>
`;
}
refresh(); setInterval(refresh,60000);
</script>
</body>
</html>