import streamlit as st
import streamlit.components.v1 as components
import json

def render_risk_classification(data):
    """
    Renders the Risk Classification tab.
    - Minimized Donut Chart size.
    - Corrected Live-Value filtering logic.
    - Professional High-End UI.
    """

    if not data:
        st.warning("⚠️ No data available. Please refresh the API on the Data Acquisition tab.")
        return

    # ── Sanitise: ensuring data types are correct for the JS engine ───────────
    clean = []
    for c in data:
        clean.append({
            "name": c.get("name", "Unknown"),
            "symbol": (c.get("symbol") or "").upper(),
            "market_cap_rank": c.get("market_cap_rank") or 0,
            "current_price": c.get("current_price") or 0,
            "high_24h": c.get("high_24h") or 0,
            "low_24h": c.get("low_24h") or 0,
            "price_change_percentage_24h": float(c.get("price_change_percentage_24h") or 0),
        })

    coins_json = json.dumps(clean)

    # ── Full HTML — Minimized Chart & Proper Asset Display ───────────────────
    html = f"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8"/>
<link href="https://fonts.googleapis.com/css2?family=Space+Grotesk:wght@400;600;700;800;900&display=swap" rel="stylesheet"/>
<script src="https://cdnjs.cloudflare.com/ajax/libs/Chart.js/4.4.0/chart.umd.min.js"></script>
<style>
*{{box-sizing:border-box;margin:0;padding:0;}}
body{{font-family:'Space Grotesk',sans-serif;background:#0d1b2a;color:#fff;padding:10px;overflow-x:hidden;}}
:root{{
  --red:#ef476f; --yellow:#ffd166; --green:#06d6a0; --blue:#4cc9f0;
  --mid:#1b263b; --light:#415a77; --muted:#778da9;
}}
h1{{color:var(--blue);text-align:center;font-size:24px;font-weight:900;margin-bottom:2px;}}
.subtitle{{text-align:center;color:var(--muted);font-size:10px;letter-spacing:2px;margin-bottom:15px;}}

/* TOP ROW: MINIMIZED CHART BOX */
.top-row{{display:grid;grid-template-columns:1fr 1fr;gap:15px;margin-bottom:20px;align-items:stretch;}}
.chart-box{{background:var(--mid);border:1px solid var(--light);border-radius:16px;padding:12px;display:flex;flex-direction:column;align-items:center;}}
.chart-container{{position:relative;height:140px;width:100%;display:flex;justify-content:center;}}
.verdict-container{{background:var(--mid);border:1px solid var(--light);border-radius:16px;padding:15px;text-align:center;display:flex;flex-direction:column;justify-content:center;}}

/* CLUSTERS: PROPER ASSET SPACING */
.clusters{{display:grid;grid-template-columns:repeat(3,1fr);gap:12px;margin-bottom:20px;}}
.cluster-head{{font-size:12px;font-weight:800;margin-bottom:8px;text-transform:uppercase;}}
.risk-card{{padding:12px;border-radius:10px;margin-bottom:8px;color:#fff;border:1px solid rgba(255,255,255,0.05);backdrop-filter:blur(4px);}}
.high-risk-block{{background:linear-gradient(135deg,rgba(208,49,45,.85),rgba(153,15,2,.85));border-left:3px solid var(--red);}}
.med-risk-block{{background:linear-gradient(135deg,rgba(240,165,0,.85),rgba(207,117,0,.85));border-left:3px solid var(--yellow);}}
.low-risk-block{{background:linear-gradient(135deg,rgba(11,132,87,.85),rgba(5,94,61,.85));border-left:3px solid var(--green);}}

.card-name{{font-size:14px;font-weight:800;white-space:nowrap;overflow:hidden;text-overflow:ellipsis;}}
.card-val{{font-size:12px;font-weight:600;opacity:0.9;}}

/* HEATMAP & ADVISOR */
.heatmap-grid{{display:grid;grid-template-columns:repeat(5,1fr);gap:6px;}}
.heatmap-cell{{background:rgba(255,255,255,0.03);border-radius:8px;padding:8px;text-align:center;border:1px solid var(--light);}}
.advisor-wrap{{background:rgba(27,38,59,.9);border-radius:18px;padding:20px;border-top:3px solid var(--blue);margin-top:15px;}}
select{{background:var(--mid);border:1px solid var(--light);color:#fff;padding:10px;border-radius:10px;width:100%;margin-bottom:12px;outline:none;}}
</style>
</head>
<body>

<h1>📊 RISK SEGMENTATION</h1>
<div class="subtitle">LIVE DATA ANALYTICS · MILESTONE 4</div>

<div class="top-row">
  <div class="chart-box">
    <div style="font-size:11px;color:var(--muted);margin-bottom:8px;font-weight:700;">RISK DISTRIBUTION</div>
    <div class="chart-container"><canvas id="donutChart"></canvas></div>
  </div>
  <div class="verdict-container">
    <div style="font-size:10px;color:var(--muted);font-weight:700;">MARKET STATUS</div>
    <div id="vStatus" style="font-size:28px;font-weight:900;">—</div>
    <div id="vAvg" style="font-size:20px;font-weight:800;color:var(--blue);">—</div>
  </div>
</div>

<div class="clusters">
  <div><div id="hHead" style="color:var(--red);" class="cluster-head">🔴 CRITICAL</div><div id="hCards"></div></div>
  <div><div id="mHead" style="color:var(--yellow);" class="cluster-head">🟡 WARNING</div><div id="mCards"></div></div>
  <div><div id="lHead" style="color:var(--green);" class="cluster-head">🟢 SECURE</div><div id="lCards"></div></div>
</div>

<div style="font-size:14px;font-weight:800;margin-bottom:8px;color:var(--blue);">🔥 LIVE VOLATILITY INDEX</div>
<div class="heatmap-grid" id="hmGrid"></div>

<div class="advisor-wrap">
  <div style="font-size:13px;font-weight:800;margin-bottom:10px;color:var(--blue);">🤖 AI STRATEGIC VERDICT</div>
  <select id="coinSelect" onchange="renderAdvisor()"></select>
  <div id="advisorCard"></div>
</div>

<script>
const COINS = {coins_json};
const highCut = 5.0, medCut = 2.5; // FIXED LIVE LOGIC THRESHOLDS
let donut = null;

function renderAll() {{
  const hArr = COINS.filter(c => Math.abs(c.price_change_percentage_24h) >= highCut);
  const mArr = COINS.filter(c => Math.abs(c.price_change_percentage_24h) >= medCut && Math.abs(c.price_change_percentage_24h) < highCut);
  const lArr = COINS.filter(c => Math.abs(c.price_change_percentage_24h) < medCut);

  // Set Headers
  document.getElementById('hHead').textContent = `🔴 CRITICAL (${{hArr.length}})`;
  document.getElementById('mHead').textContent = `🟡 WARNING (${{mArr.length}})`;
  document.getElementById('lHead').textContent = `🟢 SECURE (${{lArr.length}})`;

  // Render Cluster Cards
  const gen = (arr, cls) => arr.slice(0,5).map(c => `
    <div class="risk-card ${{cls}}">
      <div style="font-size:9px;opacity:0.7;">RANK #\${{c.market_cap_rank}}</div>
      <div class="card-name">\${{c.name}}</div>
      <div class="card-val">\${{Math.abs(c.price_change_percentage_24h).toFixed(2)}}%</div>
    </div>`).join('');
  
  document.getElementById('hCards').innerHTML = gen(hArr, 'high-risk-block');
  document.getElementById('mCards').innerHTML = gen(mArr, 'med-risk-block');
  document.getElementById('lCards').innerHTML = gen(lArr, 'low-risk-block');

  // Heatmap
  document.getElementById('hmGrid').innerHTML = COINS.slice(0,10).map(c => {{
    const v = Math.abs(c.price_change_percentage_24h);
    const col = v >= highCut ? '#ef476f' : v >= medCut ? '#ffd166' : '#06d6a0';
    return `<div class="heatmap-cell" style="border-bottom: 2px solid \${{col}};">
      <div style="color:\${{col}};font-weight:800;font-size:11px;">\${{c.symbol}}</div>
      <div style="font-size:12px;font-weight:700;">\${{v.toFixed(1)}}%</div>
    </div>`;
  }}).join('');

  // Minimized Donut Chart
  const ctx = document.getElementById('donutChart').getContext('2d');
  if(donut) donut.destroy();
  donut = new Chart(ctx, {{
    type:'doughnut',
    data:{{ 
        labels:['High','Med','Low'], 
        datasets:[{{data:[hArr.length, mArr.length, lArr.length], backgroundColor:['#ef476f','#ffd166','#06d6a0'], borderWidth:0}}] 
    }},
    options:{{ cutout:'75%', maintainAspectRatio: false, plugins:{{legend:{{display:false}}}} }}
  }});

  // Market Health
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
    <div style="display:flex;justify-content:space-between;align-items:center;margin-bottom:8px;">
      <b style="font-size:18px;">\${{asset.name}}</b>
      <span style="background:\${{col}};color:#000;padding:3px 10px;border-radius:15px;font-weight:900;font-size:10px;">
        \${{v >= highCut ? 'CRITICAL' : v >= medCut ? 'MODERATE' : 'SECURE'}}
      </span>
    </div>
    <div style="display:grid;grid-template-columns:1fr 1fr;gap:10px;font-size:13px;">
      <div>Price: <b>$\${{asset.current_price.toLocaleString()}}</b></div>
      <div style="text-align:right;">24h Low: <b style="color:var(--red);">$\${{asset.low_24h.toLocaleString()}}</b></div>
    </div>`;
}}

document.getElementById('coinSelect').innerHTML = COINS.map(c => `<option value="\${{c.name}}">\${{c.name}}</option>`).join('');
renderAll();
</script>
</body>
</html>"""

    components.html(html, height=1200, scrolling=True)
