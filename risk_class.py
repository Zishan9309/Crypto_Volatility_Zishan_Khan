import streamlit as st
import pandas as pd
import numpy as np
import plotly.graph_objects as go

def render_risk_classification(data):
    # ---------------- ADVANCED NEON UI STYLING ----------------
    st.markdown("""
    <style>
        /* Interactive Glowing Cards */
        .risk-card {
            padding: 24px;
            border-radius: 20px;
            margin-bottom: 20px;
            color: white;
            text-align: center;
            border: 1px solid rgba(255,255,255,0.1);
            transition: all 0.4s cubic-bezier(0.175, 0.885, 0.32, 1.275);
            cursor: pointer;
            position: relative;
            overflow: hidden;
        }
        .risk-card:hover {
            transform: translateY(-10px) scale(1.03);
            box-shadow: 0 15px 30px rgba(0,0,0,0.5);
        }
        
        .high-risk-neon { background: linear-gradient(145deg, #1a0a0a, #d0312d); box-shadow: 0 0 15px rgba(208, 49, 45, 0.2); border-bottom: 4px solid #ff4b2b; }
        .med-risk-neon { background: linear-gradient(145deg, #1a150a, #f0a500); box-shadow: 0 0 15px rgba(240, 165, 0, 0.2); border-bottom: 4px solid #ffd166; }
        .low-risk-neon { background: linear-gradient(145deg, #0a1a14, #0b8457); box-shadow: 0 0 15px rgba(11, 132, 87, 0.2); border-bottom: 4px solid #06d6a0; }
        
        .high-risk-neon:hover { box-shadow: 0 0 25px rgba(208, 49, 45, 0.6); }
        .med-risk-neon:hover { box-shadow: 0 0 25px rgba(240, 165, 0, 0.6); }
        .low-risk-neon:hover { box-shadow: 0 0 25px rgba(11, 132, 87, 0.6); }

        .card-name { font-size: 20px; font-weight: 900; letter-spacing: 1px; margin-bottom: 8px; text-transform: uppercase; }
        .card-tag { background: rgba(0,0,0,0.3); padding: 4px 12px; border-radius: 20px; font-size: 12px; font-weight: bold; }
        
        .metric-value { font-family: 'JetBrains Mono', monospace; font-size: 26px; font-weight: 800; color: #ffffff; }
        
        /* New Animated Verdict Box */
        .verdict-container {
            background: #1b263b;
            padding: 30px;
            border-radius: 25px;
            border: 2px dashed #4cc9f0;
            text-align: center;
            margin-bottom: 30px;
        }
    </style>
    """, unsafe_allow_html=True)

    # --- HEADER ---
    st.markdown("<h1 style='color:white; text-align:center;'>🚀 Advanced Market Risk Intelligence</h1>", unsafe_allow_html=True)
    st.markdown("<p style='color:#4cc9f0; text-align:center; font-weight:600;'>Quantifying Volatility using Dynamic Classification Algorithms</p>", unsafe_allow_html=True)
    st.write("---")

    # --- NEW: INTERACTIVE RISK THRESHOLD SIMULATOR ---
    with st.expander("⚙️ CONFIGURE DYNAMIC RISK THRESHOLDS (Algorithm Tuning)", expanded=True):
        col_s1, col_s2, col_s3 = st.columns([1, 1, 1])
        with col_s1:
            high_cutoff = st.slider("High Risk (Red Zone %)", 3.0, 15.0, 5.0)
        with col_s2:
            med_cutoff = st.slider("Medium Risk (Yellow Zone %)", 1.5, high_cutoff, 2.5)
        with col_s3:
            st.info(f"Current Model: Assets > {high_cutoff}% are flagged for Immediate Attention.")

    # Logic for categorization based on user input
    high = [c for c in data if abs(c.get('price_change_percentage_24h', 0) or 0) >= high_cutoff]
    med = [c for c in data if med_cutoff <= abs(c.get('price_change_percentage_24h', 0) or 0) < high_cutoff]
    low = [c for c in data if abs(c.get('price_change_percentage_24h', 0) or 0) < med_cutoff]

    # --- TOP SECTION: HEALTH VERDICT & DISTRIBUTION MAP ---
    c_map, c_verdict = st.columns([2, 1])

    with c_map:
        st.markdown("<h4 style='color:white;'>📊 Risk Exposure Distribution</h4>", unsafe_allow_html=True)
        # Using a Funnel/Area Chart for distribution visualization
        fig = go.Figure(go.Funnel(
            y = ["Low Risk", "Medium Risk", "High Risk"],
            x = [len(low), len(med), len(high)],
            textposition = "inside",
            textinfo = "value+percent initial",
            opacity = 0.85,
            marker = {"color": ["#06d6a0", "#ffd166", "#ef476f"],
                     "line": {"width": [4, 2, 2], "color": ["#ffffff", "#ffffff", "#ffffff"]}},
            connector = {"line": {"color": "#4cc9f0", "width": 3}}
        ))
        fig.update_layout(paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)', height=300, font_color="white", margin=dict(t=0, b=0, l=0, r=0))
        st.plotly_chart(fig, use_container_width=True)

    with c_verdict:
        avg_v = sum(abs(c.get('price_change_percentage_24h', 0) or 0) for c in data) / len(data) if data else 0
        v_status = "STABLE" if avg_v < 3 else "UNSTABLE"
        v_color = "#06d6a0" if avg_v < 3 else "#ef476f"
        
        st.markdown(f"""
        <div class="verdict-container">
            <div style="color:#778da9; font-size:12px; font-weight:700;">LIVE MARKET PULSE</div>
            <div style="color:{v_color}; font-size:42px; font-weight:900; margin:5px 0;">{v_status}</div>
            <div class="metric-value">{avg_v:.2f}%</div>
            <div style="color:#4cc9f0; font-size:11px; margin-top:10px;">GLOBAL VOLATILITY AVG</div>
        </div>
        """, unsafe_allow_html=True)

    # --- MIDDLE SECTION: THE NEON RISK CARDS ---
    st.markdown("<h3 style='color:white;'>🗂️ Classified Asset Clusters</h3>", unsafe_allow_html=True)
    
    col1, col2, col3 = st.columns(3)

    with col1:
        st.markdown(f"<p style='color:#ef476f; font-weight:bold;'>🔥 CRITICAL ({len(high)})</p>", unsafe_allow_html=True)
        for coin in high[:4]:
            st.markdown(f"""<div class="risk-card high-risk-neon"><div class="card-tag">RANK #{coin.get('market_cap_rank')}</div><div class="card-name">{coin['name']}</div><div class="metric-value">{abs(coin['price_change_percentage_24h']):.2f}%</div></div>""", unsafe_allow_html=True)

    with col2:
        st.markdown(f"<p style='color:#ffd166; font-weight:bold;'>⚖️ MODERATE ({len(med)})</p>", unsafe_allow_html=True)
        for coin in med[:4]:
            st.markdown(f"""<div class="risk-card med-risk-neon"><div class="card-tag">RANK #{coin.get('market_cap_rank')}</div><div class="card-name">{coin['name']}</div><div class="metric-value">{abs(coin['price_change_percentage_24h']):.2f}%</div></div>""", unsafe_allow_html=True)

    with col3:
        st.markdown(f"<p style='color:#06d6a0; font-weight:bold;'>🛡️ SECURE ({len(low)})</p>", unsafe_allow_html=True)
        for coin in low[:4]:
            st.markdown(f"""<div class="risk-card low-risk-neon"><div class="card-tag">RANK #{coin.get('market_cap_rank')}</div><div class="card-name">{coin['name']}</div><div class="metric-value">{abs(coin['price_change_percentage_24h']):.2f}%</div></div>""", unsafe_allow_html=True)

    # --- NEW SECTION: INTERACTIVE RISK ADVISOR ENGINE ---
    st.write("---")
    st.markdown("<h3 style='color:white;'>🔍 AI Risk Advisor & Intelligence Deep-Dive</h3>", unsafe_allow_html=True)
    
    selected_asset = st.selectbox("Search asset for immediate classification & strategy:", options=[c['name'] for c in data])
    asset_data = next((c for c in data if c['name'] == selected_asset), None)
    
    if asset_data:
        vol = abs(asset_data.get('price_change_percentage_24h', 0))
        # Intelligence Logic
        if vol >= high_cutoff:
            advice, style, icon = "EXTREME DANGER: De-leverage positions immediately. High chance of liquidations.", "border-left: 10px solid #ef476f;", "🚨"
        elif vol >= med_cutoff:
            advice, style, icon = "MODERATE RISK: Suitable for swing trading with tight stop-losses.", "border-left: 10px solid #ffd166;", "⚖️"
        else:
            advice, style, icon = "STABLE GROWTH: Strong candidate for long-term HODL. Low statistical risk.", "border-left: 10px solid #06d6a0;", "🛡️"
            
        st.markdown(f"""
        <div style="background:#16213e; padding:30px; border-radius:20px; {style} color:white;">
            <div style="display:flex; justify-content:space-between; align-items:center;">
                <h2 style="margin:0;">{icon} {selected_asset} Analysis</h2>
                <span class="card-tag" style="background:#4cc9f0; color:#0d1b2a;">STATUS: VALIDATED</span>
            </div>
            <p style="font-size:20px; margin:20px 0; line-height:1.5;">{advice}</p>
            <div style="display:flex; gap:20px;">
                <div style="background:rgba(255,255,255,0.05); padding:10px 20px; border-radius:10px;">
                    <small style="color:#778da9;">24H High</small><br><b>${asset_data.get('high_24h'):,}</b>
                </div>
                <div style="background:rgba(255,255,255,0.05); padding:10px 20px; border-radius:10px;">
                    <small style="color:#778da9;">24H Low</small><br><b>${asset_data.get('low_24h'):,}</b>
                </div>
                <div style="background:rgba(255,255,255,0.05); padding:10px 20px; border-radius:10px;">
                    <small style="color:#778da9;">Category Rank</small><br><b>#{asset_data.get('market_cap_rank')}</b>
                </div>
            </div>
        </div>
        """, unsafe_allow_html=True)

    # --- FOOTER EXPORT ---
    st.write("<br>", unsafe_allow_html=True)
    csv = pd.DataFrame(data)[['name', 'symbol', 'current_price', 'price_change_percentage_24h']].to_csv(index=False).encode('utf-8')
    st.download_button(
        label="📥 GENERATE MILESTONE 4 EXECUTIVE RISK SUMMARY",
        data=csv,
        file_name="milestone4_risk_report.csv",
        mime="text/csv",
        use_container_width=True
    )
