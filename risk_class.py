import streamlit as st
import streamlit.components.v1 as components
import json
import requests

def render_risk_classification(data):
    """
    Renders the Risk Classification tab with the exact UI from the uploaded image.
    `data` — list of dicts from CoinGecko /coins/markets endpoint.
    """

    if not data:
        st.warning("⚠️ No data available. Please refresh the API on the Data Acquisition tab.")
        return

    # ── Sanitise: ensure no None values break the JavaScript ──────────────────
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

    # ── Full HTML/CSS/JS Replica ──────────────────────────────────────────────
    html = f"""
    <!DOCTYPE html>
    <html lang="en">
    <head>
    <meta charset="UTF-8"/>
    <meta name="viewport" content="width=device-width, initial-scale=1.0"/>
    <link href="https://fonts.googleapis.com/css2?family=Space+Grotesk:wght@400;600;700;800;900&family=JetBrains+Mono:wght@400;700&display=swap" rel="stylesheet"/>
    <script src="https://cdnjs.cloudflare.com/ajax/libs/Chart.js/4.4.0/chart.umd.min.js"></script>
    <style>
    *{{box-sizing:border-box;margin:0;padding:0;}}
    body{{font-family:'Space Grotesk',sans-serif;background:#0d1b2a;color:#fff;min-height:100vh;padding:20px;overflow-x:hidden;}}
    :root{{
      --red:#ef476f;--red-bg:rgba(239,71,111,0.18);--red-border:rgba(239,71,111,0.5);
      --yellow:#ffd166;--yellow-bg:rgba(255,209,102,0.18);--yellow-border:rgba(255,209,102,0.5);
      --green:#06d6a0;--green-bg:rgba(6,214,160,0.18);--green-border:rgba(6,214,160,0.5);
      --blue:#4cc9f0;--dark:#0d1b2a;--mid:#1b263b;--light:#415a77;--muted:#778da9;
    }}
    h1{{color:var(--blue);text-align:center;font-size:28px;font-weight:900;letter-spacing:2px;margin-bottom:4px;}}
    .subtitle{{text-align:center;color:var(--muted);font-size:11px;letter-spacing:3px;margin-bottom:20px;}}
    hr{{border:none;border-top:1px solid var(--light);margin:16px 0;opacity:0.3;}}

    /* EXPANDER SECTION */
    .expander{{background:var(--mid);border:1px solid var(--light);border-radius:12px;margin-bottom:18px;overflow:hidden;}}
    .expander-header{{padding:12px 18px;cursor:pointer;display:flex;justify-content:space-between;align-items:center;font-size:13px;font-weight:700;color:var(--blue);letter-spacing:1px;}}
    .expander-body{{padding:0 18px;max-height:0;overflow:hidden;transition:max-height .3s ease,padding .3s ease;}}
    .expander-body.open{{max-height:300px;padding:14px 18px;}}
    .slider-row{{display:flex;flex-direction:column;gap:15px;}}
    .slider-label{{font-size:12px;color:var(--muted);margin-bottom:6px;}}
    input[type=range]{{width:100%;accent-color:var(--blue);cursor:pointer;}}

    /* TOP SUMMARY ROW */
    .top-row{{display:grid;grid-template-columns:2fr 1fr;gap:16px;margin-bottom:18px;}}
    .chart-box{{background:var(--mid);border:1px solid var(--light);border-radius:16px;padding:16px;position:relative;}}
    .chart-box h4{{color:#fff;font-size:14px;margin-bottom:10px;font-weight:700;}}
    #donutChart{{max-height:220px !important;}}
    .verdict-container{{background:var(--mid);border:1px solid var(--light);border-radius:16px;padding:20px;display:flex;flex-direction:column;align-items:center;justify-content:center;text-align:center;gap:8px;}}
    .verdict-label{{color:var(--muted);font-size:11px;font-weight:700;letter-spacing:2px;}}
    .verdict-status{{font-size:32px;font-weight:900;}}
    .verdict-pct{{font-size:24px;font-weight:800;color:#fff;}}
    .verdict-sub{{color:var(--blue);font-size:11px;letter-spacing:2px;}}

    /* CLASSIFIED CLUSTERS */
    .clusters{{display:grid;grid-template-columns:repeat(3,1fr);gap:14px;margin-bottom:18px;}}
    .cluster-head{{font-size:13px;font-weight:800;margin-bottom:10px;text-transform:uppercase;}}
    .risk-card{{padding:14px;border-radius:12px;margin-bottom:10px;color:#fff;border:1px solid rgba(255,255,255,0.08);backdrop-filter:blur(5px);transition:transform .2s;}}
    .risk-card:hover{{transform:translateY(-3px);box-shadow:0 8px 20px rgba(0,0,0,0.3);}}
    .high-risk-block{{background:linear-gradient(135deg,rgba(208,49,45,.9),rgba(153,15,2,.9));border-left:4px solid #ff4b2b;}}
    .med-risk-block{{background:linear-gradient(135deg,rgba(240,165,0,.9),rgba(207,117,0,.9));border-left:4px solid #ffd166;}}
    .low-risk-block{{background:linear-gradient(135deg,rgba(11,132,87,.9),rgba(5,94,61,.9));border-left:4px solid #06d6a0;}}
    .card-title{{font-size:10px;font-weight:800;color:rgba(255,255,255,.6);margin-bottom:2px;}}
    .card-name{{font-size:16px;font-weight:900;margin-bottom:4px;}}
    .card-val{{font-size:13px;font-weight:700;}}

    /* HEATMAP */
    .heatmap-wrap{{background:var(--mid);border:1px solid var(--light);border-radius:16px;padding:16px;margin-bottom:18px;}}
    .heatmap-grid{{display:grid;grid-template-columns:repeat(5,1fr);gap:8px;}}
    .heatmap-cell{{border-radius:10px;padding:12px 8px;text-align:center;transition:all .2s ease;}}
    .hm-sym{{font-size:12px;font-weight:800;}}
    .hm-val{{font-size:14px;font-weight:900;margin-top:2px;}}
    .hm-name{{font-size:10px;opacity:.6;margin-top:2px;}}

    /* ADVISOR CARD */
    .advisor-wrap{{background:rgba(27,38,59,.8);border-radius:20px;padding:25px;margin-bottom:18px;transition:.5s;}}
    .advisor-badge{{padding:8px 18px;border-radius:50px;font-weight:900;font-size:13px;color:#0d1b2a;}}
    .stat-val{{font-size:16px;font-weight:800;}}
    select{{background:var(--mid);border:1px solid var(--light);color:#fff;padding:12px;border-radius:12px;width:100%;margin-bottom:15px;font-family:inherit;}}

    .export-btn{{display:block;width:100%;padding:16px;background:linear-gradient(135deg,#4cc9f0,#4361ee);border:none;border-radius:14px;color:#fff;font-size:15px;font-weight:800;cursor:pointer;}}
    </style>
    </head>
    <body>

    <h1>📊 RISK CLASSIFICATION</h1>
    <div class="subtitle">LIVE ASSET MONITORING · PORTFOLIO INTELLIGENCE</div>

    <div class="expander">
      <div class="expander-header" onclick="toggleExp()">🛠️ CONFIGURE RISK THRESHOLDS <span id="expArrow">▼</span></div>
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

    <div class="top-row">
      <div class="chart-box">
        <h4>🍩 Asset Risk Distribution</h4>
        <canvas id="donutChart"></canvas>
      </div>
      <div class="verdict-container">
        <div class="verdict-label">MARKET HEALTH</div>
        <div class="verdict-status" id="verdictStatus">—</div>
        <div class="verdict-pct" id="verdictPct">—</div>
        <div class="verdict-sub">AVG 24H DELTA</div>
      </div>
    </div>

    <h3 style="margin-bottom:12px; font-size:18px;">🗂️ Classified Asset Clusters</h3>
    <div class="clusters">
      <div><div class="cluster-head" style="color:var(--red);" id="highHead">🔴 CRITICAL</div><div id="highCards"></div></div>
      <div><div class="cluster-head" style="color:var(--yellow);" id="medHead">🟡 WARNING</div><div id="medCards"></div></div>
      <div><div class="cluster-head" style="color:var(--green);" id="lowHead">🟢 SECURE</div><div id="lowCards"></div></div>
    </div>

    <h3 style="margin-bottom:12px; font-size:18px;">🔥 Volatility Heatmap</h3>
    <div class="heatmap-wrap"><div class="heatmap-grid" id="heatmapGrid"></div></div>

    <h3 style="margin-bottom:12px; font-size:18px;">🤖 AI Strategic Portfolio Advisor</h3>
    <select id="coinSelect" onchange="renderAdvisor()"></select>
    <div id="advisorCard"></div>

    <button class="export-btn" onclick="exportCSV()">📥 EXPORT FINAL RISK CLASSIFICATION</button>

    <script>
    const COINS = {coins_json};
    let highCut = 5.0, medCut = 2.5, donutChart = null;

    const abs = v => Math.abs(v || 0);

    function toggleExp() {{
      const b = document.getElementById('expBody');
      b.classList.toggle('open');
      document.getElementById('expArrow').textContent = b.classList.contains('open') ? '▲' : '▼';
    }}

    function onSlider() {{
      highCut = parseFloat(document.getElementById('highSlider').value);
      medCut = parseFloat(document.getElementById('medSlider').value);
      document.getElementById('highVal').textContent = highCut.toFixed(1);
      document.getElementById('medVal').textContent = medCut.toFixed(1);
      renderAll();
    }}

    function renderDonut(h, m, l) {{
      const ctx = document.getElementById('donutChart').getContext('2d');
      if (donutChart) donutChart.destroy();
      donutChart = new Chart(ctx, {{
        type: 'doughnut',
        data: {{
          labels: ['High', 'Med', 'Low'],
          datasets: [{{ data:[h,m,l], backgroundColor:['#ef476f','#ffd166','#06d6a0'], borderWidth:0 }}]
        }},
        options: {{ cutout:'70%', plugins:{{ legend:{{ position:'right', labels:{{color:'#fff', font:{{family:'Space Grotesk'}}}} }} }} }}
      }});
    }}

    function renderAll() {{
      const high = COINS.filter(c => abs(c.price_change_percentage_24h) >= highCut);
      const med = COINS.filter(c => abs(c.price_change_percentage_24h) >= medCut && abs(c.price_change_percentage_24h) < highCut);
      const low = COINS.filter(c => abs(c.price_change_percentage_24h) < medCut);

      renderDonut(high.length, med.length, low.length);

      const avg = COINS.reduce((s,c)=> s + abs(c.price_change_percentage_24h), 0) / COINS.length;
      document.getElementById('verdictStatus').textContent = avg > 4 ? 'VOLATILE' : 'STABLE';
      document.getElementById('verdictStatus').style.color = avg > 4 ? '#ef476f' : '#06d6a0';
      document.getElementById('verdictPct').textContent = avg.toFixed(2) + '%';

      document.getElementById('highHead').textContent = `🔴 CRITICAL (${{high.length}})`;
      document.getElementById('medHead').textContent = `🟡 WARNING (${{med.length}})`;
      document.getElementById('lowHead').textContent = `🟢 SECURE (${{low.length}})`;

      const genCards = (arr, cls) => arr.slice(0,4).map(c => `
        <div class="risk-card ${{cls}}">
          <div class="card-title">Rank #${{c.market_cap_rank}}</div>
          <div class="card-name">${{c.name}}</div>
          <div class="card-val">${{abs(c.price_change_percentage_24h).toFixed(2)}}% Vol</div>
        </div>`).join('');

      document.getElementById('highCards').innerHTML = genCards(high, 'high-risk-block');
      document.getElementById('medCards').innerHTML = genCards(med, 'med-risk-block');
      document.getElementById('lowCards').innerHTML = genCards(low, 'low-risk-block');

      document.getElementById('heatmapGrid').innerHTML = COINS.map(c => {{
        const v = abs(c.price_change_percentage_24h);
        const col = v > highCut ? '#ef476f' : v > medCut ? '#ffd166' : '#06d6a0';
        return `<div class="heatmap-cell" style="background:rgba(255,255,255,0.05); border:1px solid ${{col}}44;">
          <div class="hm-sym" style="color:${{col}};">${{c.symbol}}</div>
          <div class="hm-val">${{v.toFixed(1)}}%</div>
        </div>`;
      }}).join('');

      renderAdvisor();
    }}

    function renderAdvisor() {{
      const asset = COINS.find(c => c.name === document.getElementById('coinSelect').value) || COINS[0];
      const v = abs(asset.price_change_percentage_24h);
      let res = v >= highCut ? {{s:'CRITICAL', c:'#ef476f', a:'High Danger! Use 1x leverage only.'}} : 
                v >= medCut ? {{s:'MODERATE', c:'#ffd166', a:'Healthy movement. Monitor support.'}} :
                {{s:'SECURE', c:'#06d6a0', a:'Ideal for long-term HODL.'}};
      
      document.getElementById('advisorCard').innerHTML = `
        <div class="advisor-wrap" style="border:2px solid ${{res.c}};">
          <div style="display:flex; justify-content:space-between; align-items:center; margin-bottom:15px;">
            <div><div style="color:${{res.c}}; font-size:12px; font-weight:800;">VERDICT</div><div style="font-size:22px; font-weight:900;">${{asset.name}}</div></div>
            <div class="advisor-badge" style="background:${{res.c}};">${{res.s}}</div>
          </div>
          <p style="font-size:15px; margin-bottom:15px;">${{res.a}}</p>
          <div style="display:grid; grid-template-columns:repeat(3,1fr); gap:10px; border-top:1px solid #333; padding-top:15px;">
            <div><small style="color:var(--muted);">Vol</small><br><span style="color:${{res.c}};">${{v.toFixed(2)}}%</span></div>
            <div><small style="color:var(--muted);">Price</small><br><span>$${{asset.current_price.toLocaleString()}}</span></div>
            <div><small style="color:var(--muted);">24h High</small><br><span style="color:#06d6a0;">$${{asset.high_24h.toLocaleString()}}</span></div>
          </div>
        </div>`;
    }}

    function exportCSV() {{
      let csv = "Name,Price,Volatility\\n" + COINS.map(c => `${{c.name}},${{c.current_price}},${{c.price_change_percentage_24h}}`).join("\\n");
      const blob = new Blob([csv], {{ type: 'text/csv' }});
      const url = window.URL.createObjectURL(blob);
      const a = document.createElement('a');
      a.setAttribute('href', url);
      a.setAttribute('download', 'risk_report.csv');
      a.click();
    }}

    document.getElementById('coinSelect').innerHTML = COINS.map(c => `<option value="${{c.name}}">${{c.name}}</option>`).join('');
    renderAll();
    </script>
    </body>
    </html>
    """

    components.html(html, height=1800, scrolling=True)

    # ── TAB ISOLATED CHATBOT EXECUTION ─────────────────────────────────────
    render_crypto_chatbot()


# ── NATIVE GROK CHATBOT ENGINE WITH FIXED TEXTBOX CSS ──────────────────────

def render_crypto_chatbot():
    """
    Appends a styled Groq-AI engine chat container matching the exact dark-blue 
    and cyan color hierarchy. Fixes unwanted box shadows / black blocks on inputs.
    """
    st.markdown(
        """
        <style>
        /* Force Subheader to have the exact Cyan/Blue tint color */
        .grok-header {
            color: #4cc9f0 !important;
            font-family: 'Space Grotesk', sans-serif !important;
            font-weight: 800 !important;
            letter-spacing: 1px;
            margin-top: 20px;
        }
        /* Style Streamlit Chat Messages Content Text and Background */
        [data-testid="stChatMessage"] {
            background-color: #1b263b !important;
            border: 1px solid rgba(65, 90, 119, 0.4) !important;
            border-radius: 12px !important;
            color: #ffffff !important;
            font-family: 'Space Grotesk', sans-serif !important;
        }
        /* Ensure specific targeted Markdown user/assistant text changes to pure white */
        [data-testid="stChatMessage"] p, [data-testid="stChatMessage"] span {
            color: #ffffff !important;
        }
        
        /* ── CRITICAL FIX FOR THE TEXT INPUT BLACK BOX EFFECT ── */
        [data-testid="stChatInput"], 
        [data-testid="stChatInput"] > div,
        .stChatInputContainer {
            background-color: #0d1b2a !important;
            background: #0d1b2a !important;
            border: 1px solid #415a77 !important;
            border-radius: 12px !important;
            box-shadow: none !important;
        }
        [data-testid="stChatInput"] textarea {
            color: #000000 !important;
            -webkit-text-fill-color: #000000 !important;
            background-color: #ffffff !important;
            background: #ffffff !important;
            border-radius: 8px !important;
            padding: 8px !important;
            box-shadow: none !important;
            outline: none !important;
        }
        [data-testid="stChatInput"] textarea::placeholder {
            color: #778da9 !important;
            opacity: 1 !important;
        }
        [data-testid="stChatInput"] button {
            color: #4cc9f0 !important;
            background-color: transparent !important;
        }
        [data-testid="stChatInput"] button:hover, 
        [data-testid="stChatInput"] button:active,
        [data-testid="stChatInput"] button:focus {
            color: #4cc9f0 !important;
            border-color: #4cc9f0 !important;
            box-shadow: 0 0 10px rgba(76, 201, 240, 0.4) !important;
        }
        [data-testid="stChatInput"] button svg {
            fill: #4cc9f0 !important;
            stroke: #4cc9f0 !important;
        }
        </style>
        """,
        unsafe_allow_html=True
    )

    st.markdown('<h3 class="grok-header">🤖 Live Crypto Analytics Assistant (Groq Cloud Engine)</h3>', unsafe_allow_html=True)

    # आपकी Groq API KEY यहाँ सेट है
    GROQ_API_KEY = "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"

    if "chat_history" not in st.session_state:
        st.session_state.chat_history = [
            {"role": "assistant", "content": "Hello! I am your Groq-powered assistant. Ask me anything about current crypto risk mappings, market stability, or volatility spikes."}
        ]

    for message in st.session_state.chat_history:
        with st.chat_message(message["role"]):
            st.markdown(f'<span style="color:#ffffff;">{message["content"]}</span>', unsafe_allow_html=True)

    if user_query := st.chat_input("Ask about asset volatility or market indicators...", key="grok_tab_chat_input"):
        st.session_state.chat_history.append({"role": "user", "content": user_query})
        with st.chat_message("user"):
            st.markdown(f'<span style="color:#ffffff;">{user_query}</span>', unsafe_allow_html=True)

        with st.chat_message("assistant"):
            response_placeholder = st.empty()
            response_placeholder.markdown("<em style='color:#778da9;'>Analyzing market conditions...</em>", unsafe_allow_html=True)

            headers = {
                "Authorization": f"Bearer {GROQ_API_KEY}",
                "Content-Type": "application/json"
            }
            
            # यहाँ हमने Groq Cloud का URL और मॉडल (llama3-8b) अपडेट किया है
            payload = {
                "model": "llama3-8b-8192",
                "messages": [
                    {"role": "system", "content": "You are an elite cryptocurrency risk analyst assistant. Provide sharp financial insights, mathematical volatility calculations, and concise tracking suggestions data in clear format."},
                    *st.session_state.chat_history
                ]
            }

            try:
                response = requests.post(
                    "https://api.groq.com/openai/v1/chat/completions",
                    headers=headers,
                    json=payload
                )
                
                if response.status_code == 200:
                    result = response.json()
                    ai_response = result["choices"][0]["message"]["content"]
                    response_placeholder.markdown(f'<span style="color:#ffffff;">{ai_response}</span>', unsafe_allow_html=True)
                    st.session_state.chat_history.append({"role": "assistant", "content": ai_response})
                else:
                    error_msg = f"❌ API Error: Connection failed (Status {response.status_code}). Setup/Key mismatch."
                    response_placeholder.markdown(f'<span style="color:#ef476f;">{error_msg}</span>', unsafe_allow_html=True)
            
            except Exception as e:
                response_placeholder.markdown(f"⚠️ Connection timeout error: {str(e)}")
