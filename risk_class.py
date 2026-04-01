import streamlit as st
import streamlit.components.v1 as components
import json

def render_risk_classification(data):
    """
    Renders the Risk Classification tab with the exact UI from the uploaded image.
    Corrected logic to ensure Real-Time filtering based on API values.
    """

    if not data:
        st.warning("⚠️ No data available. Please refresh the API on the Data Acquisition tab.")
        return

    # ── Sanitise: replace None with 0 so JS logic functions correctly ────────
    clean = []
    for c in data:
        clean.append({
            "name": c.get("name", "Unknown"),
            "symbol": (c.get("symbol") or "").upper(),
            "market_cap_rank": c.get("market_cap_rank") or 0,
            "current_price": c.get("current_price") or 0,
            "high_24h": c.get("high_24h") or 0,
            "low_24h": c.get("low_24h") or 0,
            "price_change_percentage_24h": c.get("price_change_percentage_24h") or 0,
        })

    coins_json = json.dumps(clean)

    # ── Full HTML — EXACT replica with corrected Real-Time Logic ──────────────
    html = f"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8"/>
<link href="https://fonts.googleapis.com/css2?family=Space+Grotesk:wght@400;600;700;800;900&family=JetBrains+Mono:wght@400;700&display=swap" rel="stylesheet"/>
<script src="https://cdnjs.cloudflare.com/ajax/libs/Chart.js/4.4.0/chart.umd.min.js"></script>
<style>
*{{box-sizing:border-box;margin:0;padding:0;}}
body{{font-family:'Space Grotesk',sans-serif;background:#0d1b2a;color:#fff;min-height:100vh;padding:20px;}}
:root{{
  --red:#ef476f; --yellow:#ffd166; --green:#06d6a0; --blue:#4cc9f0;
  --mid:#1b263b; --light:#415a77; --muted:#778da9;
}}
h1{{color:var(--blue);text-align:center;font-size:28px;font-weight:900;letter-spacing:2px;margin-bottom:4px;}}
.subtitle{{text-align:center;color:var(--muted);font-size:11px;letter-spacing:3px;margin-bottom:20px;}}
hr{{border:none;border-top:1px solid var(--light);margin:16px 0;opacity:0.3;}}

/* CONFIG BOX */
.expander{{background:var(--mid);border:1px solid var(--light);border-radius:12px;margin-bottom:18px;overflow:hidden;}}
.expander-header{{padding:12px 18px;cursor:pointer;display:flex;justify-content:space-between;align-items:center;font-size:13px;font-weight:700;color:var(--blue);}}
.expander-body{{padding:0 18px;max-height:0;overflow:hidden;transition:max-height .3s ease;}}
.expander-body.open{{max-height:300px;padding:14px 18px;}}
.slider-label{{font-size:12px;color:var(--muted);margin-bottom:6px;}}
input[type=range]{{width:100%;accent-color:var(--blue);margin-bottom:10px;}}

/* DASHBOARD LAYOUT */
.top-row{{display:grid;grid-template-columns:2fr 1fr;gap:16px;margin-bottom:18px;}}
.chart-box{{background:var(--mid);border:1px solid var(--light);border-radius:16px;padding:16px;}}
.verdict-container{{background:var(--mid);border:1px solid var(--light);border-radius:16px;padding:20px;text-align:center;}}
.clusters{{display:grid;grid-template-columns:repeat(3,1fr);gap:14px;margin-bottom:18px;}}
.risk-card{{padding:14px;border-radius:12px;margin-bottom:10px;color:#fff;border:1px solid rgba(255,255,255,0.08);}}
.high-risk-block{{background:linear-gradient(135deg,rgba(208,49,45,.9),rgba(153,15,2,.9));border-left:4px solid #ff4b2b;}}
.med-risk-block{{background:linear-gradient(135deg,rgba(240,165,0,.9),rgba(207,117,0,.9));border-left:4px solid #ffd166;}}
.low-risk-block{{background:linear-gradient(135deg,rgba(11,132,87,.9),rgba(5,94,61,.9));border-left:4px solid #06d6a0;}}

/* HEATMAP */
.heatmap-grid{{display:grid;grid-template-columns:repeat(5,1fr);gap:8px;margin-top:10px;}}
.heatmap-cell{{background:rgba(255,255,255,0.05);border-radius:8px;padding:10px;text-align:center;border:1px solid var(--light);}}

/* ADVISOR */
.advisor-wrap{{background:rgba(27,38,59,.8);border-radius:20px;padding:25px;margin-top:20px;}}
select{{background:var(--mid);border:1px solid var(--light);color:#fff;padding:10px;border-radius:10px;width:100%;margin-bottom:15px;}}
</style>
</head>
<body>

<h1>📊 RISK CLASSIFICATION</h1>
<div class="subtitle">LIVE ASSET MONITORING · PORTFOLIO INTELLIGENCE</div>

<div class="expander">
  <div class="expander-header" onclick="toggleExp()">🛠️ CONFIGURE RISK THRESHOLDS <span id="expArrow">▼</span></div>
  <div class="expander-body" id="expBody">
      <div class="slider-label">High Risk Threshold: <b id="highVal">5.0</b>%</div>
      <input type="range" id="highSlider" min="3" max="10" step="0.5" value="5" oninput="onUpdate()"/>
      <div class="slider-label">Medium Risk Threshold: <b id="medVal">2.5</b>%</div>
      <input type="range" id="medSlider" min="1" max="5" step="0.5" value="2.5" oninput="onUpdate()"/>
  </div>
</div>

<div class="top-row">
  <div class="chart-box"><canvas id="donutChart"></canvas></div>
  <div class="verdict-container">
    <div style="font-size:11px;color:var(--muted);">MARKET HEALTH</div>
    <div id="vStatus" style="font-size:30px;font-weight:900;">—</div>
    <div id="vAvg" style="font-size:22px;font-weight:800;">—</div>
  </div>
</div>

<div class="clusters">
  <div><div id="hHead" style="color:var(--red);font-weight:800;margin-bottom:10px;">🔴 CRITICAL</div><div id="hCards"></div></div>
  <div><div id="mHead" style="color:var(--yellow);font-weight:800;margin-bottom:10px;">🟡 WARNING</div><div id="mCards"></div></div>
  <div><div id="lHead" style="color:var(--green);font-weight:800;margin-bottom:10px;">🟢 SECURE</div><div id="lCards"></div></div>
</div>

<div style="font-weight:800;margin:20px 0 10px 0;">🔥 Volatility Heatmap</div>
<div class="heatmap-grid" id="hmGrid"></div>

<div style="font-weight:800;margin:20px 0 10px 0;">🤖 AI Strategic Portfolio Advisor</div>
<select id="coinSelect" onchange="renderAdvisor()"></select>
<div id="advisorCard"></div>

<script>
const COINS = {coins_json};
let highCut = 5.0, medCut = 2.5, donut = null;

function toggleExp() {{
  const b = document.getElementById('expBody');
  b.classList.toggle('open');
  document.getElementById('expArrow').textContent = b.classList.contains('open') ? '▲' : '▼';
}}

function onUpdate() {{
  highCut = parseFloat(document.getElementById('highSlider').value);
  medCut = parseFloat(document.getElementById('medSlider').value);
  document.getElementById('highVal').textContent = highCut.toFixed(1);
  document.getElementById('medVal').textContent = medCut.toFixed(1);
  renderAll();
}}

function renderAll() {{
  // REAL-TIME FILTERING LOGIC
  const hArr = COINS.filter(c => Math.abs(c.price_change_percentage_24h) >= highCut);
  const mArr = COINS.filter(c => Math.abs(c.price_change_percentage_24h) >= medCut && Math.abs(c.price_change_percentage_24h) < highCut);
  const lArr = COINS.filter(c => Math.abs(c.price_change_percentage_24h) < medCut);

  // Update Headers
  document.getElementById('hHead').textContent = `🔴 CRITICAL (${{hArr.length}})`;
  document.getElementById('mHead').textContent = `🟡 WARNING (${{mArr.length}})`;
  document.getElementById('lHead').textContent = `🟢 SECURE (${{lArr.length}})`;

  // Update Cards
  const gen = (arr, cls) => arr.slice(0,4).map(c => `
    <div class="risk-card ${{cls}}">
      <div style="font-size:10px;opacity:0.7;">Rank #${{c.market_cap_rank}}</div>
      <div style="font-size:16px;font-weight:900;">${{c.name}}</div>
      <div style="font-size:13px;">${{Math.abs(c.price_change_percentage_24h).toFixed(2)}}% Vol</div>
    </div>`).join('');
  
  document.getElementById('hCards').innerHTML = gen(hArr, 'high-risk-block');
  document.getElementById('mCards').innerHTML = gen(mArr, 'med-risk-block');
  document.getElementById('lCards').innerHTML = gen(lArr, 'low-risk-block');

  // Update Heatmap
  document.getElementById('hmGrid').innerHTML = COINS.slice(0,15).map(c => {{
    const v = Math.abs(c.price_change_percentage_24h);
    const border = v >= highCut ? '#ef476f' : v >= medCut ? '#ffd166' : '#06d6a0';
    return `<div class="heatmap-cell" style="border-color:${{border}};">
      <div style="color:${{border}};font-weight:800;font-size:12px;">${{c.symbol}}</div>
      <div style="font-weight:900;">${{v.toFixed(1)}}%</div>
    </div>`;
  }}).join('');

  // Update Donut
  const ctx = document.getElementById('donutChart').getContext('2d');
  if(donut) donut.destroy();
  donut = new Chart(ctx, {{
    type:'doughnut',
    data:{{ labels:['High','Med','Low'], datasets:[{{data:[hArr.length, mArr.length, lArr.length], backgroundColor:['#ef476f','#ffd166','#06d6a0'], borderWidth:0}}] }},
    options:{{ cutout:'70%', plugins:{{legend:{{display:false}}}} }}
  }});

  // Update Market Health
  const avg = COINS.reduce((a,b)=>a+Math.abs(b.price_change_percentage_24h),0)/COINS.length;
  document.getElementById('vStatus').textContent = avg > 4 ? 'VOLATILE' : 'STABLE';
  document.getElementById('vStatus').style.color = avg > 4 ? '#ef476f' : '#06d6a0';
  document.getElementById('vAvg').textContent = avg.toFixed(2) + '%';
  
  renderAdvisor();
}}

function renderAdvisor() {{
  const asset = COINS.find(c => c.name === document.getElementById('coinSelect').value) || COINS[0];
  const v = Math.abs(asset.price_change_percentage_24h);
  let col = v >= highCut ? '#ef476f' : v >= medCut ? '#ffd166' : '#06d6a0';
  document.getElementById('advisorCard').innerHTML = `
    <div class="advisor-wrap" style="border:2px solid ${{col}};">
      <div style="display:flex;justify-content:space-between;align-items:center;">
        <div style="font-size:22px;font-weight:900;">${{asset.name}}</div>
        <div style="background:${{col}};color:#000;padding:5px 15px;border-radius:20px;font-weight:800;">${{v >= highCut ? 'CRITICAL' : v >= medCut ? 'MODERATE' : 'SECURE'}}</div>
      </div>
      <p style="margin-top:10px;">Current Price: <b>$${{asset.current_price.toLocaleString()}}</b></p>
      <div style="margin-top:10px;font-size:14px;opacity:0.8;">24h High: ${{asset.high_24h}} | 24h Low: ${{asset.low_24h}}</div>
    </div>`;
}}

document.getElementById('coinSelect').innerHTML = COINS.map(c => `<option value="${{c.name}}">${{c.name}}</option>`).join('');
renderAll();
</script>
</body>
</html>"""

    components.html(html, height=1800, scrolling=True)
