import streamlit as st
import streamlit.components.v1 as components
import json


def render_risk_classification(data):
    """
    Renders the Risk Classification tab.
    `data`  — list of dicts from CoinGecko /coins/markets endpoint.
              Required fields: name, symbol, market_cap_rank,
              current_price, high_24h, low_24h, price_change_percentage_24h
    """

    if not data:
        st.warning("⚠️ No data available. Please refresh the API on the Data Acquisition tab.")
        return

    # ── Sanitise: replace None with 0 so JS doesn't break ──────────────────
    clean = []
    for c in data:
        clean.append({
            "name":                        c.get("name", "Unknown"),
            "symbol":                      c.get("symbol", ""),
            "market_cap_rank":             c.get("market_cap_rank") or 0,
            "current_price":               c.get("current_price") or 0,
            "high_24h":                    c.get("high_24h") or 0,
            "low_24h":                     c.get("low_24h") or 0,
            "price_change_percentage_24h": c.get("price_change_percentage_24h") or 0,
        })

    coins_json = json.dumps(clean)

    # ── Full HTML — exact replica of the uploaded dashboard ─────────────────
    html = f"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8"/>
<meta name="viewport" content="width=device-width, initial-scale=1.0"/>
<link href="https://fonts.googleapis.com/css2?family=Space+Grotesk:wght@400;600;700;800;900&family=JetBrains+Mono:wght@400;700&display=swap" rel="stylesheet"/>
<script src="https://cdnjs.cloudflare.com/ajax/libs/Chart.js/4.4.0/chart.umd.min.js"></script>
<style>
*{{box-sizing:border-box;margin:0;padding:0;}}
body{{font-family:'Space Grotesk',sans-serif;background:#0d1b2a;color:#fff;min-height:100vh;padding:20px;}}
:root{{
  --red:#ef476f;--red-bg:rgba(239,71,111,0.18);--red-border:rgba(239,71,111,0.5);
  --yellow:#ffd166;--yellow-bg:rgba(255,209,102,0.18);--yellow-border:rgba(255,209,102,0.5);
  --green:#06d6a0;--green-bg:rgba(6,214,160,0.18);--green-border:rgba(6,214,160,0.5);
  --blue:#4cc9f0;--dark:#0d1b2a;--mid:#1b263b;--light:#415a77;--muted:#778da9;
}}
h1{{color:var(--blue);text-align:center;font-size:28px;font-weight:900;letter-spacing:2px;margin-bottom:4px;}}
.subtitle{{text-align:center;color:var(--muted);font-size:12px;letter-spacing:3px;margin-bottom:20px;}}
hr{{border:none;border-top:1px solid var(--light);margin:16px 0;}}

/* EXPANDER */
.expander{{background:var(--mid);border:1px solid var(--light);border-radius:12px;margin-bottom:18px;overflow:hidden;}}
.expander-header{{padding:12px 18px;cursor:pointer;display:flex;justify-content:space-between;align-items:center;font-size:13px;font-weight:700;color:var(--blue);letter-spacing:1px;user-select:none;}}
.expander-body{{padding:0 18px;max-height:0;overflow:hidden;transition:max-height .3s ease,padding .3s ease;}}
.expander-body.open{{max-height:200px;padding:14px 18px;}}
.slider-row{{display:flex;flex-direction:column;gap:10px;}}
.slider-label{{font-size:12px;color:var(--muted);margin-bottom:4px;}}
input[type=range]{{width:100%;accent-color:var(--blue);cursor:pointer;}}

/* TOP ROW */
.top-row{{display:grid;grid-template-columns:2fr 1fr;gap:16px;margin-bottom:18px;}}
.chart-box{{background:var(--mid);border:1px solid var(--light);border-radius:16px;padding:16px;}}
.chart-box h4{{color:#fff;font-size:14px;margin-bottom:10px;}}
#donutChart{{max-height:230px;}}
.verdict-container{{background:var(--mid);border:1px solid var(--light);border-radius:16px;padding:20px;display:flex;flex-direction:column;align-items:center;justify-content:center;text-align:center;gap:8px;}}
.verdict-label{{color:var(--muted);font-size:11px;font-weight:700;letter-spacing:2px;}}
.verdict-status{{font-size:30px;font-weight:900;}}
.verdict-pct{{font-size:22px;font-weight:800;color:#fff;}}
.verdict-sub{{color:var(--blue);font-size:11px;letter-spacing:2px;}}

/* CLUSTERS */
.cluster-title{{color:#fff;font-size:16px;font-weight:800;margin-bottom:12px;}}
.clusters{{display:grid;grid-template-columns:repeat(3,1fr);gap:14px;margin-bottom:18px;}}
.cluster-head{{font-size:13px;font-weight:800;margin-bottom:8px;}}
.risk-card{{padding:13px 14px;border-radius:12px;margin-bottom:8px;color:#fff;border:1px solid rgba(255,255,255,0.08);transition:transform .25s,box-shadow .25s;backdrop-filter:blur(5px);animation:fadeInUp .35s ease both;}}
.risk-card:hover{{transform:scale(1.025);box-shadow:0 8px 20px rgba(0,0,0,0.45);}}
.high-risk-block{{background:linear-gradient(135deg,rgba(208,49,45,.9),rgba(153,15,2,.9));border-left:4px solid #ff4b2b;}}
.med-risk-block{{background:linear-gradient(135deg,rgba(240,165,0,.9),rgba(207,117,0,.9));border-left:4px solid #ffd166;}}
.low-risk-block{{background:linear-gradient(135deg,rgba(11,132,87,.9),rgba(5,94,61,.9));border-left:4px solid #06d6a0;}}
.card-title{{font-size:11px;font-weight:800;text-transform:uppercase;color:rgba(255,255,255,.6);margin-bottom:2px;}}
.card-name{{font-size:15px;font-weight:900;margin-bottom:4px;}}
.card-val{{font-size:13px;font-weight:700;}}

/* HEATMAP */
.section-title{{color:#fff;font-size:16px;font-weight:800;margin-bottom:12px;}}
.heatmap-wrap{{background:var(--mid);border:1px solid var(--light);border-radius:16px;padding:16px;margin-bottom:18px;}}
.heatmap-grid{{display:grid;grid-template-columns:repeat(5,1fr);gap:6px;}}
.heatmap-cell{{border-radius:10px;padding:10px 8px;text-align:center;cursor:pointer;transition:transform .2s,box-shadow .2s;position:relative;overflow:hidden;}}
.heatmap-cell:hover{{transform:scale(1.06);box-shadow:0 6px 18px rgba(0,0,0,.5);z-index:2;}}
.hm-sym{{font-size:11px;font-weight:800;letter-spacing:.5px;opacity:.8;}}
.hm-val{{font-size:14px;font-weight:900;margin-top:2px;}}
.hm-name{{font-size:9px;opacity:.6;margin-top:2px;white-space:nowrap;overflow:hidden;text-overflow:ellipsis;}}
.heatmap-legend{{display:flex;align-items:center;gap:6px;margin-top:10px;font-size:11px;color:var(--muted);}}
.legend-bar{{height:10px;flex:1;border-radius:5px;background:linear-gradient(90deg,#06d6a0,#ffd166,#ef476f);}}

/* ADVISOR */
.advisor-wrap{{background:rgba(27,38,59,.8);border-radius:20px;padding:24px;margin-bottom:18px;transition:.5s;}}
.advisor-top{{display:flex;justify-content:space-between;align-items:center;margin-bottom:18px;}}
.advisor-badge{{padding:7px 18px;border-radius:50px;font-weight:900;font-size:13px;color:#0d1b2a;}}
.advisor-name{{font-size:20px;font-weight:900;margin:2px 0;}}
.advisor-sym{{font-size:12px;color:var(--muted);}}
.advisor-body{{display:grid;grid-template-columns:2fr 1fr;gap:20px;margin-bottom:18px;}}
.advisor-text{{font-size:15px;line-height:1.7;}}
.signals-box{{background:rgba(0,0,0,.2);border-radius:14px;padding:14px;}}
.signals-title{{font-weight:700;font-size:12px;margin-bottom:8px;}}
.signal-item{{font-size:13px;margin-bottom:5px;}}
.advisor-stats{{display:grid;grid-template-columns:repeat(4,1fr);gap:12px;border-top:1px solid rgba(255,255,255,.08);padding-top:16px;}}
.stat-label{{font-size:11px;color:var(--muted);}}
.stat-val{{font-size:15px;font-weight:800;}}

/* SELECT */
select{{background:var(--mid);border:1px solid var(--light);color:#fff;padding:10px 14px;border-radius:10px;font-family:'Space Grotesk',sans-serif;font-size:14px;width:100%;margin-bottom:14px;cursor:pointer;outline:none;}}
select:focus{{border-color:var(--blue);}}

/* EXPORT BTN */
.export-btn{{display:block;width:100%;padding:14px;background:linear-gradient(135deg,#4cc9f0,#4361ee);border:none;border-radius:12px;color:#fff;font-family:'Space Grotesk',sans-serif;font-size:14px;font-weight:800;letter-spacing:1px;cursor:pointer;text-align:center;transition:opacity .2s;}}
.export-btn:hover{{opacity:.85;}}

@keyframes fadeInUp{{from{{opacity:0;transform:translateY(10px);}}to{{opacity:1;transform:translateY(0);}}}}
</style>
</head>
<body>

<h1>📊 RISK CLASSIFICATION</h1>
<div class="subtitle">LIVE ASSET MONITORING · PORTFOLIO INTELLIGENCE</div>
<hr/>

<!-- CONFIGURE THRESHOLDS -->
<div class="expander" id="exp">
  <div class="expander-header" onclick="toggleExp()">
    🛠️ CONFIGURE RISK THRESHOLDS <span id="expArrow">▼</span>
  </div>
  <div class="expander-body" id="expBody">
    <div class="slider-row">
      <div>
        <div class="slider-label">High Risk Definition: <b id="highVal">5.0</b>%</div>
        <input type="range" id="highSlider" min="3" max="10" step="0.5" value="5" oninput="onSlider()"/>
      </div>
      <div>
        <div class="slider-label">Medium Risk Definition: <b id="medVal">2.5</b>%</div>
        <input type="range" id="medSlider" min="1" max="4.5" step="0.5" value="2.5" oninput="onSlider()"/>
      </div>
    </div>
  </div>
</div>

<!-- TOP ROW -->
<div class="top-row">
  <div class="chart-box">
    <h4>🍩 Asset Risk Distribution</h4>
    <canvas id="donutChart"></canvas>
  </div>
  <div class="verdict-container" id="verdictBox">
    <div class="verdict-label">MARKET HEALTH</div>
    <div class="verdict-status" id="verdictStatus">—</div>
    <div class="verdict-pct" id="verdictPct">—</div>
    <div class="verdict-sub">AVG 24H DELTA</div>
  </div>
</div>

<!-- CLASSIFIED CLUSTERS -->
<div class="cluster-title">🗂️ Classified Asset Clusters</div>
<div class="clusters">
  <div>
    <div class="cluster-head" style="color:var(--red);" id="highHead">🔴 CRITICAL ASSETS (0)</div>
    <div id="highCards"></div>
  </div>
  <div>
    <div class="cluster-head" style="color:var(--yellow);" id="medHead">🟡 WARNING ZONE (0)</div>
    <div id="medCards"></div>
  </div>
  <div>
    <div class="cluster-head" style="color:var(--green);" id="lowHead">🟢 SECURE ASSETS (0)</div>
    <div id="lowCards"></div>
  </div>
</div>

<hr/>

<!-- VOLATILITY HEATMAP -->
<div class="section-title">🔥 Volatility Heatmap</div>
<div class="heatmap-wrap">
  <div class="heatmap-grid" id="heatmapGrid"></div>
  <div class="heatmap-legend">
    <span>Low</span>
    <div class="legend-bar"></div>
    <span>High</span>
  </div>
</div>

<hr/>

<!-- AI ADVISOR -->
<div class="section-title">🤖 AI Strategic Portfolio Advisor</div>
<select id="coinSelect" onchange="renderAdvisor()"></select>
<div id="advisorCard"></div>

<hr/>
<button class="export-btn" onclick="exportCSV()">📥 EXPORT FINAL RISK CLASSIFICATION</button>

<script>
// ── LIVE DATA from CoinGecko via Python ────────────────────────────────────
const COINS = {coins_json};

let highCut = 5.0, medCut = 2.5;
let donutChart = null;

const abs = v => Math.abs(v || 0);

function classify(data){{
  return {{
    high: data.filter(c => abs(c.price_change_percentage_24h) >= highCut),
    med:  data.filter(c => abs(c.price_change_percentage_24h) >= medCut && abs(c.price_change_percentage_24h) < highCut),
    low:  data.filter(c => abs(c.price_change_percentage_24h) < medCut)
  }};
}}

function toggleExp(){{
  const b = document.getElementById('expBody');
  const a = document.getElementById('expArrow');
  b.classList.toggle('open');
  a.textContent = b.classList.contains('open') ? '▲' : '▼';
}}

function onSlider(){{
  highCut = parseFloat(document.getElementById('highSlider').value);
  medCut  = parseFloat(document.getElementById('medSlider').value);
  if (medCut >= highCut) {{ medCut = highCut - 0.5; document.getElementById('medSlider').value = medCut; }}
  document.getElementById('highVal').textContent = highCut.toFixed(1);
  document.getElementById('medVal').textContent  = medCut.toFixed(1);
  renderAll();
}}

function renderDonut(h, m, l){{
  const ctx = document.getElementById('donutChart').getContext('2d');
  if (donutChart) donutChart.destroy();
  donutChart = new Chart(ctx, {{
    type: 'doughnut',
    data: {{
      labels: ['High Risk', 'Medium Risk', 'Low Risk'],
      datasets: [{{ data: [h, m, l], backgroundColor: ['#ef476f', '#ffd166', '#06d6a0'], borderWidth: 0, hoverOffset: 8 }}]
    }},
    options: {{
      cutout: '60%',
      plugins: {{
        legend: {{ labels: {{ color: '#fff', font: {{ family: 'Space Grotesk', weight: '700' }}, padding: 14 }} }},
        tooltip: {{ callbacks: {{ label: ctx => `${{ctx.label}}: ${{ctx.raw}}` }} }}
      }},
      animation: {{ animateRotate: true, duration: 600 }}
    }}
  }});
}}

function renderVerdict(data){{
  const avg = data.reduce((s, c) => s + abs(c.price_change_percentage_24h), 0) / data.length;
  const volatile = avg > 4;
  document.getElementById('verdictStatus').textContent = volatile ? 'VOLATILE' : 'STABLE';
  document.getElementById('verdictStatus').style.color = volatile ? '#ef476f' : '#06d6a0';
  document.getElementById('verdictPct').textContent = avg.toFixed(2) + '%';
}}

function cardHTML(coin, cls){{
  return `<div class="risk-card ${{cls}}">
    <div class="card-title">Rank #${{coin.market_cap_rank}}</div>
    <div class="card-name">${{coin.name}}</div>
    <div class="card-val">${{abs(coin.price_change_percentage_24h).toFixed(2)}}% Volatility</div>
  </div>`;
}}

function renderCards({{high, med, low}}){{
  document.getElementById('highHead').textContent = `🔴 CRITICAL ASSETS (${{high.length}})`;
  document.getElementById('medHead').textContent  = `🟡 WARNING ZONE (${{med.length}})`;
  document.getElementById('lowHead').textContent  = `🟢 SECURE ASSETS (${{low.length}})`;
  document.getElementById('highCards').innerHTML  = high.slice(0, 5).map(c => cardHTML(c, 'high-risk-block')).join('');
  document.getElementById('medCards').innerHTML   = med.slice(0, 5).map(c => cardHTML(c, 'med-risk-block')).join('');
  document.getElementById('lowCards').innerHTML   = low.slice(0, 5).map(c => cardHTML(c, 'low-risk-block')).join('');
}}

function heatColor(vol){{
  const t = Math.min(vol / 10, 1);
  if (t < 0.5) {{
    const u = t * 2;
    const r = Math.round(6   + (255 - 6)   * u);
    const g = Math.round(214 + (209 - 214) * u);
    const b = Math.round(160 + (102 - 160) * u);
    return `rgb(${{r}},${{g}},${{b}})`;
  }} else {{
    const u = (t - 0.5) * 2;
    const r = Math.round(255 + (239 - 255) * u);
    const g = Math.round(209 + (71  - 209) * u);
    const b = Math.round(102 + (111 - 102) * u);
    return `rgb(${{Math.min(255,r)}},${{Math.max(0,g)}},${{Math.max(0,b)}})`;
  }}
}}

function hexToRgb(rgb){{
  const m = rgb.match(/\d+/g);
  return m ? m.join(',') : '255,255,255';
}}

function renderHeatmap(data){{
  const grid = document.getElementById('heatmapGrid');
  grid.innerHTML = data.map(c => {{
    const vol   = abs(c.price_change_percentage_24h);
    const col   = heatColor(vol);
    const dir   = c.price_change_percentage_24h >= 0 ? '▲' : '▼';
    const alpha = 0.15 + 0.45 * (vol / 10);
    return `<div class="heatmap-cell"
      style="background:rgba(${{hexToRgb(col)}},${{alpha.toFixed(2)}});border:1px solid ${{col}}40;"
      title="${{c.name}}: ${{vol.toFixed(2)}}%">
      <div class="hm-sym" style="color:${{col}};">${{c.symbol.toUpperCase()}}</div>
      <div class="hm-val" style="color:${{col}};">${{dir}}${{vol.toFixed(1)}}%</div>
      <div class="hm-name">${{c.name}}</div>
    </div>`;
  }}).join('');
}}

function renderAdvisor(){{
  const name  = document.getElementById('coinSelect').value;
  const asset = COINS.find(c => c.name === name);
  if (!asset) return;
  const vol = abs(asset.price_change_percentage_24h);
  let status, color, shadow, advice, signals;
  if (vol >= highCut) {{
    status = "CRITICAL RISK"; color = "#ef476f"; shadow = "rgba(239,71,111,0.4)";
    advice  = "🚨 High Danger! Use 1x leverage only. Extreme volatility detected. Avoid long-term entry here.";
    signals = ["🛑 Reduce Exposure", "📉 De-risk Portfolio", "⚠️ High Slippage"];
  }} else if (vol >= medCut) {{
    status = "MODERATE RISK"; color = "#ffd166"; shadow = "rgba(255,209,102,0.4)";
    advice  = "⚖️ Moderate Risk. Suitable for swing trading with tight stop-losses. Monitor support levels.";
    signals = ["⚖️ Balanced Entry", "📈 Trailing Stop", "🔍 Monitor Support"];
  }} else {{
    status = "SECURE / STABLE"; color = "#06d6a0"; shadow = "rgba(6,214,160,0.4)";
    advice  = "🛡️ Secure. Good for long-term holding. Low volatility baseline ideal for DCA strategies.";
    signals = ["🛡️ Accumulation Zone", "💎 HODL Candidate", "✅ Value Asset"];
  }}
  const fmt = v => v >= 1 ? `$${{v.toLocaleString()}}` : v >= 0.001 ? `$${{v.toFixed(4)}}` : `$${{v.toExponential(2)}}`;
  document.getElementById('advisorCard').innerHTML = `
  <div class="advisor-wrap" style="border:2px solid ${{color}};box-shadow:0 10px 30px ${{shadow}};">
    <div class="advisor-top">
      <div>
        <div style="color:${{color}};font-weight:800;font-size:12px;letter-spacing:1px;">STRATEGIC VERDICT</div>
        <div class="advisor-name">${{asset.name}} <span class="advisor-sym">(${{asset.symbol.toUpperCase()}})</span></div>
      </div>
      <div class="advisor-badge" style="background:${{color}};">${{status}}</div>
    </div>
    <div class="advisor-body">
      <div class="advisor-text">${{advice}}</div>
      <div class="signals-box">
        <div class="signals-title" style="color:${{color}};">SIGNALS:</div>
        ${{signals.map(s => `<div class="signal-item">${{s}}</div>`).join('')}}
      </div>
    </div>
    <div class="advisor-stats">
      <div><div class="stat-label">Volatility</div><div class="stat-val" style="color:${{color}};">${{vol.toFixed(2)}}%</div></div>
      <div><div class="stat-label">Current Price</div><div class="stat-val">${{fmt(asset.current_price)}}</div></div>
      <div><div class="stat-label">24h High</div><div class="stat-val" style="color:#06d6a0;">${{fmt(asset.high_24h)}}</div></div>
      <div><div class="stat-label">24h Low</div><div class="stat-val" style="color:#ef476f;">${{fmt(asset.low_24h)}}</div></div>
    </div>
  </div>`;
}}

function populateSelect(){{
  document.getElementById('coinSelect').innerHTML =
    COINS.map(c => `<option value="${{c.name}}">${{c.name}}</option>`).join('');
}}

function exportCSV(){{
  const rows = [
    ['name', 'current_price', 'price_change_percentage_24h'],
    ...COINS.map(c => [c.name, c.current_price, c.price_change_percentage_24h])
  ];
  const csv = rows.map(r => r.join(',')).join('\\n');
  const a = document.createElement('a');
  a.href = 'data:text/csv;charset=utf-8,' + encodeURIComponent(csv);
  a.download = 'risk_report.csv';
  a.click();
}}

function renderAll(){{
  const {{high, med, low}} = classify(COINS);
  renderDonut(high.length, med.length, low.length);
  renderVerdict(COINS);
  renderCards({{high, med, low}});
  renderHeatmap(COINS);
  renderAdvisor();
}}

populateSelect();
renderAll();
</script>
</body>
</html>"""

    # ── Inject into Streamlit tab via components.html ────────────────────────
    components.html(html, height=2200, scrolling=True)
