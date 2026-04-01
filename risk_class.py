import streamlit as st
import streamlit.components.v1 as components
import json

def render_risk_classification(data):
    """
    Renders the Risk Classification tab.
    Removed manual thresholds to focus on direct live-data classification.
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

    # ── Full HTML — Professional Live Data View ──────────────────────────────
    html = f"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8"/>
<link href="https://fonts.googleapis.com/css2?family=Space+Grotesk:wght@400;600;700;800;900&family=JetBrains+Mono:wght@400;700&display=swap" rel="stylesheet"/>
<script src="https://cdnjs.cloudflare.com/ajax/libs/Chart.js/4.4.0/chart.umd.min.js"></script>
<style>
*{{box-sizing:border-box;margin:0;padding:0;}}
body{{font-family:'Space Grotesk',sans-serif;background:#0d1b2a;color:#fff;min-height:100vh;padding:20px;overflow-x:hidden;}}
:root{{
  --red:#ef476f; --yellow:#ffd166; --green:#06d6a0; --blue:#4cc9f0;
  --mid:#1b263b; --light:#415a77; --muted:#778da9;
}}
h1{{color:var(--blue);text-align:center;font-size:28px;font-weight:900;letter-spacing:2px;margin-bottom:4px;}}
.subtitle{{text-align:center;color:var(--muted);font-size:11px;letter-spacing:3px;margin-bottom:20px;text-transform:uppercase;}}
hr{{border:none;border-top:1px solid var(--light);margin:16px 0;opacity:0.3;}}

/* DASHBOARD LAYOUT */
.top-row{{display:grid;grid-template-columns:2fr 1fr;gap:16px;margin-bottom:25px;}}
.chart-box{{background:var(--mid);border:1px solid var(--light);border-radius:16px;padding:16px;}}
.verdict-container{{background:var(--mid);border:1px solid var(--light);border-radius:16px;padding:20px;text-align:center;display:flex;flex-direction:column;justify-content:center;}}

.clusters{{display:grid;grid-template-columns:repeat(3,1fr);gap:14px;margin-bottom:25px;}}
.risk-card{{padding:14px;border-radius:12px;margin-bottom:12px;color:#fff;border:1px solid rgba(255,255,255,0.08);backdrop-filter:blur(5px);}}
.high-risk-block{{background:linear-gradient(135deg,rgba(208,49,45,.9),rgba(153,15,2,.9));border-left:4px solid #ff4b2b;}}
.med-risk-block{{background:linear-gradient(135deg,rgba(240,165,0,.9),rgba(207,117,0,.9));border-left:4px solid #ffd166;}}
.low-risk-block{{background:linear-gradient(135deg,rgba(11,132,87,.9),rgba(5,94,61,.9));border-left:4px solid #06d6a0;}}

/* HEATMAP */
.heatmap-grid{{display:grid;grid-template-columns:repeat(5,1fr);gap:10px;margin-top:10px;}}
.heatmap-cell{{background:rgba(255,255,255,0.05);border-radius:10px;padding:12px;text-align:center;border:1px solid var(--light);transition:0.3s;}}
.heatmap-cell:hover{{transform:scale(1.05); background:rgba(255,255,255,0.1);}}

/* ADVISOR */
.advisor-wrap{{background:rgba(27,38,59,.8);border-radius:20px;padding:25px;margin-top:20px;border-top:4px solid var(--blue);}}
select{{background:var(--mid);border:1px solid var(--light);color:#fff;padding:12px;border-radius:12px;width:100%;margin-bottom:15px;font-family:inherit;cursor:pointer;}}
</style>
</head>
<body>

<h1>📊 RISK SEGMENTATION</h1>
<div class="subtitle">Real-Time Market Volatility Engine · Milestone 4</div>

<div class="top-row">
  <div class="chart-box">
    <h4 style="font-size:13px; margin-bottom:10px; color:var(--muted);">🍩 RISK DISTRIBUTION (LIVE)</h4>
    <canvas id="donutChart"></canvas>
  </div>
  <div class="verdict-container">
    <div style="font-size:11px;color:var(--muted); font-weight:700;">MARKET HEALTH</div>
    <div id="vStatus" style="font-size:32px;font-weight:900; margin:10px 0;">—</div>
    <div id="vAvg" style="font-size:22px;font-weight:800; color:var(--blue);">—</div>
    <div style="font-size:10px; color:var(--muted); margin-top:5px;">AVG 24H MOVEMENT</div>
  </div>
</div>

<div class="clusters">
  <div><div id="hHead" style="color:var(--red);font-weight:800;margin-bottom:12px; font-size:14px;">🔴 CRITICAL ASSETS</div><div id="hCards"></div></div>
  <div><div id="mHead" style="color:var(--yellow);font-weight:800;margin-bottom:12px; font-size:14px;">🟡 WARNING ZONE</div><div id="mCards"></div></div>
  <div><div id="lHead" style="color:var(--green);font-weight:800;margin-bottom:12px; font-size:14px;">🟢 SECURE ASSETS</div><div id="lCards"></div></div>
</div>

<div style="font-weight:800;margin:30px 0 10px 0; font-size:16px; color:var(--blue);">🔥 VOLATILITY HEATMAP</div>
<div class="heatmap-grid" id="hmGrid"></div>

<div style="font-weight:800;margin:40px 0 10px 0; font-size:16px; color:var(--blue);">🤖 AI STRATEGIC ADVISOR</div>
<select id="coinSelect" onchange="renderAdvisor()"></select>
<div id="advisorCard"></div>

<script>
const COINS = {coins_json};
// Fixed Professional Thresholds for Live Value Data
const highCut = 5.0; 
const medCut = 2.5;
let donut = null;

function renderAll() {{
  const hArr = COINS.filter(c => Math.abs(c.price_change_percentage_24h) >= highCut);
  const mArr = COINS.filter(c => Math.abs(c.price_change_percentage_24h) >= medCut && Math.abs(c.price_change_percentage_24h) < highCut);
  const lArr = COINS.filter(c => Math.abs(c.price_change_percentage_24h) < medCut);

  document.getElementById('hHead').textContent = `🔴 CRITICAL ($\{{hArr.length}})`;
  document.getElementById('mHead').textContent = `🟡 WARNING ($\{{mArr.length}})`;
  document.getElementById('lHead').textContent = `🟢 SECURE ($\{{lArr.length}})`;

  const gen = (arr, cls) => arr.slice(0,5).map(c => `
    <div class="risk-card $\{{cls}}">
      <div style="font-size:10px;opacity:0.7; font-weight:bold;">RANK #$\{{c.market_cap_rank}}</div>
      <div style="font-size:16px;font-weight:900; margin:3px 0;">$\{{c.name}}</div>
      <div style="font-size:13px; font-weight:700;">$\{{Math.abs(c.price_change_percentage_24h).toFixed(2)}}% 24H Delta</div>
    </div>`).join('');
  
  document.getElementById('hCards').innerHTML = gen(hArr, 'high-risk-block');
  document.getElementById('mCards').innerHTML = gen(mArr, 'med-risk-block');
  document.getElementById('lCards').innerHTML = gen(lArr, 'low-risk-block');

  document.getElementById('hmGrid').innerHTML = COINS.slice(0,15).map(c => {{
    const v = Math.abs(c.price_change_percentage_24h);
    const border = v >= highCut ? '#ef476f' : v >= medCut ? '#ffd166' : '#06d6a0';
    return `<div class="heatmap-cell" style="border-bottom: 4px solid $\{{border}};">
      <div style="color:$\{{border}};font-weight:800;font-size:12px; margin-bottom:4px;">$\{{c.symbol}}</div>
      <div style="font-weight:900; font-size:15px;">$\{{v.toFixed(1)}}%</div>
    </div>`;
  }}).join('');

  const ctx = document.getElementById('donutChart').getContext('2d');
  if(donut) donut.destroy();
  donut = new Chart(ctx, {{
    type:'doughnut',
    data:{{ 
        labels:['High Risk','Med Risk','Low Risk'], 
        datasets:[{{
            data:[hArr.length, mArr.length, lArr.length], 
            backgroundColor:['#ef476f','#ffd166','#06d6a0'], 
            borderWidth:0,
            hoverOffset: 10
        }}] 
    }},
    options:{{ 
        cutout:'75%', 
        plugins:{{
            legend:{{
                position: 'right',
                labels: {{ color: '#fff', font: {{ family: 'Space Grotesk', size: 11 }} }}
            }}
        }},
        animation: {{ duration: 1000 }}
    }}
  }});

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
  let advice = v >= highCut ? "🚨 High Danger! Use 1x leverage only. Market showing extreme volatility." : 
               v >= medCut ? "⚖️ Moderate Risk. Suitable for swing trades with tight stop-losses." : 
               "🛡️ Secure. Good for long-term holding. Low volatility baseline.";

  document.getElementById('advisorCard').innerHTML = `
    <div class="advisor-wrap" style="border-color: $\{{col}};">
      <div style="display:flex;justify-content:space-between;align-items:center;">
        <div style="font-size:24px;font-weight:900;">$\{{asset.name}} <span style="font-size:12px; color:var(--muted);">($\{{asset.symbol}})</span></div>
        <div style="background:$\{{col}};color:#0d1b2a;padding:6px 16px;border-radius:20px;font-weight:900; font-size:13px;">
            $\{{v >= highCut ? 'CRITICAL' : v >= medCut ? 'MODERATE' : 'SECURE'}}
        </div>
      </div>
      <p style="margin:15px 0; font-size:16px; line-height:1.5;">$\{{advice}}</p>
      <div style="display:grid; grid-template-columns: repeat(3, 1fr); gap:10px; border-top:1px solid var(--light); padding-top:15px;">
        <div><small style="color:var(--muted);">Price</small><br><b>$ $\{{asset.current_price.toLocaleString()}}</b></div>
        <div><small style="color:var(--muted);">24h High</small><br><b style="color:var(--green);">$ $\{{asset.high_24h.toLocaleString()}}</b></div>
        <div><small style="color:var(--muted);">24h Low</small><br><b style="color:var(--red);">$ $\{{asset.low_24h.toLocaleString()}}</b></div>
      </div>
    </div>`;
}}

document.getElementById('coinSelect').innerHTML = COINS.map(c => `<option value="$\{{c.name}}">$\{{c.name}}</option>`).join('');
renderAll();
</script>
</body>
</html>"""

    components.html(html, height=1600, scrolling=True)
