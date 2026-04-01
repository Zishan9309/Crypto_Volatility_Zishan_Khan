import streamlit as st
import streamlit.components.v1 as components
import json
import pandas as pd

def render_risk_classification(data):
    """
    Renders the Risk Classification tab with the exact UI from the uploaded image.
    Uses the user's provided working Python logic inside an interactive HTML component.
    """

    if not data:
        st.warning("⚠️ No data available. Please refresh the API on the Data Acquisition tab.")
        return

    # ── Sanitise Data for JavaScript ──────────────────────────────────────────
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

    # ── Full HTML/CSS/JS Replica ──────────────────────────────────────────────
    html = f"""
    <!DOCTYPE html>
    <html lang="en">
    <head>
    <meta charset="UTF-8"/>
    <link href="https://fonts.googleapis.com/css2?family=Space+Grotesk:wght@400;600;700;800;900&family=JetBrains+Mono:wght@400;700&display=swap" rel="stylesheet"/>
    <script src="https://cdnjs.cloudflare.com/ajax/libs/Chart.js/4.4.0/chart.umd.min.js"></script>
    <style>
        *{{box-sizing:border-box;margin:0;padding:0;}}
        body{{font-family:'Space Grotesk',sans-serif;background:#0d1b2a;color:#fff;min-height:100vh;padding:10px;overflow-x:hidden;}}
        
        :root{{
          --red:#ef476f; --yellow:#ffd166; --green:#06d6a0; --blue:#4cc9f0;
          --mid:#1b263b; --light:#415a77; --muted:#778da9;
        }}

        h1{{color:var(--blue);text-align:center;font-size:26px;font-weight:900;letter-spacing:2px;margin-bottom:5px;}}
        .subtitle{{text-align:center;color:var(--muted);font-size:11px;letter-spacing:3px;margin-bottom:20px;text-transform:uppercase;}}
        hr{{border:none;border-top:1px solid var(--light);margin:15px 0;opacity:0.3;}}

        /* CONFIG EXPANDER */
        .expander{{background:var(--mid);border:1px solid var(--light);border-radius:12px;margin-bottom:18px;overflow:hidden;}}
        .expander-header{{padding:12px 18px;cursor:pointer;display:flex;justify-content:space-between;align-items:center;font-size:13px;font-weight:700;color:var(--blue);}}
        .expander-body{{padding:0 18px;max-height:0;overflow:hidden;transition:max-height .3s ease;}}
        .expander-body.open{{max-height:300px;padding:15px 18px;}}
        .slider-label{{font-size:12px;color:var(--muted);margin-bottom:8px;display:flex;justify-content:space-between;}}
        input[type=range]{{width:100%;accent-color:var(--blue);margin-bottom:15px;cursor:pointer;}}

        /* GRID LAYOUT */
        .top-row{{display:grid;grid-template-columns:1.5fr 1fr;gap:15px;margin-bottom:20px;}}
        .chart-box{{background:var(--mid);border:1px solid var(--light);border-radius:16px;padding:15px;}}
        .verdict-container{{background:var(--mid);border:1px solid var(--light);border-radius:16px;padding:20px;display:flex;flex-direction:column;align-items:center;justify-content:center;}}
        
        .clusters{{display:grid;grid-template-columns:repeat(3,1fr);gap:15px;margin-bottom:20px;}}
        .risk-card{{padding:14px;border-radius:12px;margin-bottom:10px;color:#fff;border:1px solid rgba(255,255,255,0.08);backdrop-filter:blur(5px);}}
        .high-risk-block{{background:linear-gradient(135deg,rgba(208,49,45,.9),rgba(153,15,2,.9));border-left:4px solid #ff4b2b;}}
        .med-risk-block{{background:linear-gradient(135deg,rgba(240,165,0,.9),rgba(207,117,0,.9));border-left:4px solid #ffd166;}}
        .low-risk-block{{background:linear-gradient(135deg,rgba(11,132,87,.9),rgba(5,94,61,.9));border-left:4px solid #06d6a0;}}

        .card-name{{font-size:16px;font-weight:900;}}
        .card-val{{font-size:13px;font-weight:700;opacity:0.9;}}

        /* HEATMAP */
        .heatmap-grid{{display:grid;grid-template-columns:repeat(5,1fr);gap:8px;}}
        .heatmap-cell{{background:rgba(255,255,255,0.03);border-radius:10px;padding:12px;text-align:center;border:1px solid var(--light);}}

        /* ADVISOR */
        .advisor-wrap{{background:rgba(27,38,59,.9);border-radius:20px;padding:25px;border:2px solid var(--blue);transition: 0.3s;}}
        select{{background:var(--mid);border:1px solid var(--light);color:#fff;padding:12px;border-radius:10px;width:100%;margin-bottom:15px;font-family:inherit;}}
    </style>
    </head>
    <body>

    <h1>📊 RISK SEGMENTATION</h1>
    <div class="subtitle">Real-Time Data Logic Engine · Milestone 4</div>

    <div class="expander">
      <div class="expander-header" onclick="toggleExp()">🛠️ CONFIGURE RISK THRESHOLDS <span id="expArrow">▼</span></div>
      <div class="expander-body" id="expBody">
          <div class="slider-label"><span>High Risk Cutoff (Critical)</span><b id="highVal">5.0%</b></div>
          <input type="range" id="highSlider" min="3" max="10" step="0.5" value="5" oninput="updateLogic()"/>
          
          <div class="slider-label"><span>Medium Risk Cutoff (Warning)</span><b id="medVal">2.5%</b></div>
          <input type="range" id="medSlider" min="1" max="4.5" step="0.5" value="2.5" oninput="updateLogic()"/>
      </div>
    </div>

    <div class="top-row">
      <div class="chart-box">
        <h4 style="font-size:13px;margin-bottom:10px;">🍩 Risk Exposure Donut</h4>
        <canvas id="donutChart"></canvas>
      </div>
      <div class="verdict-container">
        <div style="font-size:11px;color:var(--muted);letter-spacing:1px;">MARKET HEALTH</div>
        <div id="vStatus" style="font-size:32px;font-weight:900;margin:5px 0;">STABLE</div>
        <div id="vAvg" style="font-size:22px;font-weight:800;color:var(--blue);">0.00%</div>
      </div>
    </div>

    <div class="clusters">
      <div>
        <div id="hHead" style="color:var(--red);font-weight:800;font-size:13px;margin-bottom:10px;">🔴 CRITICAL (0)</div>
        <div id="hCards"></div>
      </div>
      <div>
        <div id="mHead" style="color:var(--yellow);font-weight:800;font-size:13px;margin-bottom:10px;">🟡 WARNING (0)</div>
        <div id="mCards"></div>
      </div>
      <div>
        <div id="lHead" style="color:var(--green);font-weight:800;font-size:13px;margin-bottom:10px;">🟢 SECURE (0)</div>
        <div id="lCards"></div>
      </div>
    </div>

    <div style="font-weight:800;margin-bottom:10px;font-size:15px;color:var(--blue);">🔥 Volatility Heatmap</div>
    <div class="heatmap-grid" id="hmGrid"></div>

    <div style="font-weight:800;margin:25px 0 10px 0;font-size:15px;color:var(--blue);">🤖 AI Strategic Advisor</div>
    <select id="coinSelect" onchange="renderAdvisor()"></select>
    <div id="advisorCard"></div>

    <script>
    const DATA = {coins_json};
    let hCut = 5.0, mCut = 2.5, myChart = null;

    function toggleExp() {{
        const b = document.getElementById('expBody');
        b.classList.toggle('open');
        document.getElementById('expArrow').textContent = b.classList.contains('open') ? '▲' : '▼';
    }}

    function updateLogic() {{
        hCut = parseFloat(document.getElementById('highSlider').value);
        mCut = parseFloat(document.getElementById('medSlider').value);
        
        if(mCut >= hCut) {{
            mCut = hCut - 0.5;
            document.getElementById('medSlider').value = mCut;
        }}

        document.getElementById('highVal').textContent = hCut.toFixed(1) + "%";
        document.getElementById('medVal').textContent = mCut.toFixed(1) + "%";
        renderAll();
    }}

    function renderAll() {{
        // Filter based on user provided working Python logic
        const hArr = DATA.filter(c => Math.abs(c.price_change_percentage_24h) >= hCut);
        const mArr = DATA.filter(c => Math.abs(c.price_change_percentage_24h) >= mCut && Math.abs(c.price_change_percentage_24h) < hCut);
        const lArr = DATA.filter(c => Math.abs(c.price_change_percentage_24h) < mCut);

        document.getElementById('hHead').textContent = `🔴 CRITICAL ($\{{hArr.length}})`;
        document.getElementById('mHead').textContent = `🟡 WARNING ($\{{mArr.length}})`;
        document.getElementById('lHead').textContent = `🟢 SECURE ($\{{lArr.length}})`;

        const genCards = (arr, cls) => arr.slice(0, 4).map(c => `
            <div class="risk-card $\{{cls}}">
                <div style="font-size:10px;opacity:0.7;font-weight:bold;">RANK #$\{{c.market_cap_rank}}</div>
                <div class="card-name">$\{{c.name}}</div>
                <div class="card-val">$\{{Math.abs(c.price_change_percentage_24h).toFixed(2)}}% Volatility</div>
            </div>
        `).join('');

        document.getElementById('hCards').innerHTML = genCards(hArr, 'high-risk-block');
        document.getElementById('mCards').innerHTML = genCards(mArr, 'med-risk-block');
        document.getElementById('lCards').innerHTML = genCards(lArr, 'low-risk-block');

        const avg = DATA.reduce((sum, c) => sum + Math.abs(c.price_change_percentage_24h), 0) / DATA.length;
        document.getElementById('vStatus').textContent = avg > 4 ? 'VOLATILE' : 'STABLE';
        document.getElementById('vStatus').style.color = avg > 4 ? '#ef476f' : '#06d6a0';
        document.getElementById('vAvg').textContent = avg.toFixed(2) + "%";

        document.getElementById('hmGrid').innerHTML = DATA.slice(0, 15).map(c => {{
            const val = Math.abs(c.price_change_percentage_24h);
            const color = val >= hCut ? '#ef476f' : val >= mCut ? '#ffd166' : '#06d6a0';
            return `<div class="heatmap-cell" style="border-bottom: 3px solid $\{{color}};">
                <div style="color:$\{{color}};font-weight:900;font-size:12px;">$\{{c.symbol}}</div>
                <div style="font-weight:800;font-size:14px;margin-top:2px;">$\{{val.toFixed(1)}}%</div>
            </div>`;
        }}).join('');

        const ctx = document.getElementById('donutChart').getContext('2d');
        if(myChart) myChart.destroy();
        myChart = new Chart(ctx, {{
            type: 'doughnut',
            data: {{
                labels: ['High', 'Med', 'Low'],
                datasets: [{{
                    data: [hArr.length, mArr.length, lArr.length],
                    backgroundColor: ['#ef476f', '#ffd166', '#06d6a0'],
                    borderWidth: 0
                }}]
            }},
            options: {{ cutout: '75%', plugins: {{ legend: {{ display: false }} }} }}
        }});
        renderAdvisor();
    }}

    function renderAdvisor() {{
        const coinName = document.getElementById('coinSelect').value;
        const c = DATA.find(x => x.name === coinName) || DATA[0];
        const val = Math.abs(c.price_change_percentage_24h);
        let color = val >= hCut ? '#ef476f' : val >= mCut ? '#ffd166' : '#06d6a0';
        document.getElementById('advisorCard').innerHTML = `
            <div class="advisor-wrap" style="border-color: $\{{color}};">
                <h2 style="margin:0;">$\{{c.name}} Analysis</h2>
                <p style="font-size:16px;font-weight:600;margin:10px 0;">Strategy: $\{{val >= hCut ? 'Critical Risk. Avoid Leverage.' : val >= mCut ? 'Moderate Risk. Use Stop Loss.' : 'Stable Asset. Ideal for HODL.'}}</p>
                <div style="display:grid;grid-template-columns:repeat(3,1fr);gap:10px;text-align:center;border-top:1px solid #415a77;padding-top:15px;">
                    <div><small style="color:var(--muted);">Price</small><br><b>$ $\{{c.current_price.toLocaleString()}}</b></div>
                    <div><small style="color:var(--muted);">24H High</small><br><b style="color:var(--green);">$ $\{{c.high_24h.toLocaleString()}}</b></div>
                    <div><small style="color:var(--muted);">24H Low</small><br><b style="color:var(--red);">$ $\{{c.low_24h.toLocaleString()}}</b></div>
                </div>
            </div>`;
    }

    document.getElementById('coinSelect').innerHTML = DATA.map(c => `<option value="$\{{c.name}}">$\{{c.name}}</option>`).join('');
    renderAll();
    </script>
    </body>
    </html>
    """

    components.html(html, height=1400, scrolling=True)

    # Sidebar Export functionality (Native Streamlit)
    st.write("---")
    csv = pd.DataFrame(data)[['name', 'current_price', 'price_change_percentage_24h']].to_csv(index=False).encode('utf-8')
    st.download_button(label="📥 EXPORT FINAL RISK CLASSIFICATION", data=csv, file_name="risk_report.csv", use_container_width=True)
