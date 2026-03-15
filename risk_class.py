import streamlit as st
import pandas as pd
import numpy as np
import plotly.graph_objects as go

def render_risk_classification(data):
    # ---------------- REFINED NEON GLASS-UI STYLING ----------------
    st.markdown("""
    <style>
        /* Medium-Sized Blocks with Glassmorphism */
        .risk-card {
            padding: 15px;
            border-radius: 12px;
            margin-bottom: 12px;
            color: white;
            text-align: left;
            border: 1px solid rgba(255,255,255,0.1);
            transition: all 0.3s ease;
            backdrop-filter: blur(5px);
        }
        .risk-card:hover {
            transform: scale(1.02);
            box-shadow: 0 8px 20px rgba(0,0,0,0.4);
        }
        
        /* Proper Color Gradients for Clusters */
        .high-risk-block { background: linear-gradient(135deg, rgba(208, 49, 45, 0.9), rgba(153, 15, 2, 0.9)); border-left: 4px solid #ff4b2b; }
        .med-risk-block { background: linear-gradient(135deg, rgba(240, 165, 0, 0.9), rgba(207, 117, 0, 0.9)); border-left: 4px solid #ffd166; }
        .low-risk-block { background: linear-gradient(135deg, rgba(11, 132, 87, 0.9), rgba(5, 94, 61, 0.9)); border-left: 4px solid #06d6a0; }

        .card-title { font-size: 14px; font-weight: 800; text-transform: uppercase; color: rgba(255,255,255,0.7); margin-bottom: 2px; }
        .card-name { font-size: 18px; font-weight: 900; margin-bottom: 5px; }
        .card-val { font-size: 16px; font-weight: 700; color: #ffffff; }
        
        .verdict-container {
            background: #1b263b;
            padding: 20px;
            border-radius: 20px;
            border: 1px solid #415a77;
            text-align: center;
        }

        /* Advisor Intelligence Card Styling */
        .advisor-card {
            background: rgba(27, 38, 59, 0.8);
            border-radius: 20px;
            padding: 30px;
            color: white;
            transition: 0.5s;
        }
    </style>
    """, unsafe_allow_html=True)

    # --- HEADER ---
    st.markdown("<h1 style='color:white; text-align:center;'>📊 Milestone 4: Risk Segmentation</h1>", unsafe_allow_html=True)
    st.write("---")

    # --- INTERACTIVE THRESHOLD SLIDER ---
    with st.expander("🛠️ CONFIGURE RISK THRESHOLDS"):
        high_cutoff = st.slider("High Risk Definition (%)", 3.0, 10.0, 5.0)
        med_cutoff = st.slider("Medium Risk Definition (%)", 1.0, high_cutoff, 2.5)

    # Classification Logic
    high = [c for c in data if abs(c.get('price_change_percentage_24h', 0) or 0) >= high_cutoff]
    med = [c for c in data if med_cutoff <= abs(c.get('price_change_percentage_24h', 0) or 0) < high_cutoff]
    low = [c for c in data if abs(c.get('price_change_percentage_24h', 0) or 0) < med_cutoff]

    # --- TOP SECTION: DONUT DISTRIBUTION & VERDICT ---
    col_donut, col_verdict = st.columns([2, 1])

    with col_donut:
        st.markdown("<h4 style='color:white;'>🍩 Asset Risk Distribution</h4>", unsafe_allow_html=True)
        fig = go.Figure(data=[go.Pie(
            labels=['High Risk', 'Medium Risk', 'Low Risk'],
            values=[len(high), len(med), len(low)],
            hole=.6,
            marker_colors=['#ef476f', '#ffd166', '#06d6a0'],
            textinfo='percent+label',
            pull=[0.1, 0, 0] 
        )])
        fig.update_layout(
            paper_bgcolor='rgba(0,0,0,0)', 
            plot_bgcolor='rgba(0,0,0,0)', 
            height=300, 
            font_color="white", 
            margin=dict(t=0, b=0, l=0, r=0),
            showlegend=False
        )
        st.plotly_chart(fig, use_container_width=True)

    with col_verdict:
        avg_v = sum(abs(c.get('price_change_percentage_24h', 0) or 0) for c in data) / len(data) if data else 0
        v_status = "VOLATILE" if avg_v > 4 else "STABLE"
        v_color = "#ef476f" if avg_v > 4 else "#06d6a0"
        
        st.markdown(f"""
        <div class="verdict-container">
            <div style="color:#778da9; font-size:12px; font-weight:700;">MARKET HEALTH</div>
            <div style="color:{v_color}; font-size:32px; font-weight:900; margin:10px 0;">{v_status}</div>
            <div style="font-size:24px; font-weight:800; color:white;">{avg_v:.2f}%</div>
            <div style="color:#4cc9f0; font-size:11px;">AVG HOURLY DELTA</div>
        </div>
        """, unsafe_allow_html=True)

    # --- MIDDLE SECTION: MEDIUM-SIZED CLASSIFIED BLOCKS ---
    st.markdown("<h3 style='color:white;'>🗂️ Classified Asset Clusters</h3>", unsafe_allow_html=True)
    
    c1, c2, c3 = st.columns(3)

    with c1:
        st.markdown(f"<p style='color:#ef476f; font-weight:bold;'>🔴 CRITICAL ASSETS ({len(high)})</p>", unsafe_allow_html=True)
        for coin in high[:5]:
            st.markdown(f"""
            <div class="risk-card high-risk-block">
                <div class="card-title">Rank #{coin.get('market_cap_rank')}</div>
                <div class="card-name">{coin['name']}</div>
                <div class="card-val">{abs(coin['price_change_percentage_24h']):.2f}% Volatility</div>
            </div>
            """, unsafe_allow_html=True)

    with c2:
        st.markdown(f"<p style='color:#ffd166; font-weight:bold;'>🟡 WARNING ZONE ({len(med)})</p>", unsafe_allow_html=True)
        for coin in med[:5]:
            st.markdown(f"""
            <div class="risk-card med-risk-block">
                <div class="card-title">Rank #{coin.get('market_cap_rank')}</div>
                <div class="card-name">{coin['name']}</div>
                <div class="card-val">{abs(coin['price_change_percentage_24h']):.2f}% Volatility</div>
            </div>
            """, unsafe_allow_html=True)

    with c3:
        st.markdown(f"<p style='color:#06d6a0; font-weight:bold;'>🟢 SECURE ASSETS ({len(low)})</p>", unsafe_allow_html=True)
        for coin in low[:5]:
            st.markdown(f"""
            <div class="risk-card low-risk-block">
                <div class="card-title">Rank #{coin.get('market_cap_rank')}</div>
                <div class="card-name">{coin['name']}</div>
                <div class="card-val">{abs(coin['price_change_percentage_24h']):.2f}% Volatility</div>
            </div>
            """, unsafe_allow_html=True)

    # --- BOTTOM SECTION: SMART AI PORTFOLIO ADVISOR ---
    st.write("---")
    st.markdown("<h3 style='color:white;'>🤖 AI Strategic Portfolio Advisor</h3>", unsafe_allow_html=True)
    
    sel_coin = st.selectbox("Select Asset for personalized risk strategy:", options=[c['name'] for c in data])
    asset = next((c for c in data if c['name'] == sel_coin), None)
    
    if asset:
        vol = abs(asset.get('price_change_percentage_24h', 0))
        
        # Advisor Logic & Theming
        if vol >= high_cutoff:
            status, color, shadow, advice = "CRITICAL RISK", "#ef476f", "rgba(239, 71, 111, 0.4)", "🚨 High Danger! Use 1x leverage only. Extreme volatility detected. Avoid long-term entry here."
            signals = ["🛑 Reduce Exposure", "📉 De-risk Portfolio", "⚠️ High Slippage"]
        elif vol >= med_cutoff:
            status, color, shadow, advice = "MODERATE RISK", "#ffd166", "rgba(255, 209, 102, 0.4)", "⚖️ Moderate Risk. Suitable for swing trading with tight stop-losses. Monitor support levels."
            signals = ["⚖️ Balanced Entry", "📈 Trailing Stop", "🔍 Monitor Support"]
        else:
            status, color, shadow, advice = "SECURE / STABLE", "#06d6a0", "rgba(6, 214, 160, 0.4)", "🛡️ Secure. Good for long-term holding. Low volatility baseline ideal for DCA strategies."
            signals = ["🛡️ Accumulation Zone", "💎 HODL Candidate", "✅ Value Asset"]

        # Strategic Advisor Card
        st.markdown(f"""
        <div class="advisor-card" style="border: 2px solid {color}; box-shadow: 0 10px 30px {shadow};">
            <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 20px;">
                <div>
                    <span style="color: {color}; font-weight: 800; font-size: 14px; letter-spacing: 1px;">STRATEGIC VERDICT</span>
                    <h2 style="margin: 0; color: white;">{sel_coin} <small style="font-size: 14px; color: #778da9;">({asset['symbol'].upper()})</small></h2>
                </div>
                <div style="background: {color}; color: #0d1b2a; padding: 8px 20px; border-radius: 50px; font-weight: 900;">
                    {status}
                </div>
            </div>
            <div style="display: flex; gap: 30px; margin-bottom: 20px;">
                <div style="flex: 2;">
                    <p style="font-size: 18px; line-height: 1.6;">{advice}</p>
                </div>
                <div style="flex: 1; background: rgba(0,0,0,0.2); padding: 15px; border-radius: 15px;">
                    <p style="margin: 0 0 10px 0; font-weight: bold; color: {color};">SIGNALS:</p>
                    {"".join([f'<div style="margin-bottom: 5px; font-size: 14px;">{s}</div>' for s in signals])}
                </div>
            </div>
            <div style="display: grid; grid-template-columns: repeat(4, 1fr); gap: 15px; border-top: 1px solid rgba(255,255,255,0.1); padding-top: 20px;">
                <div><small style="color: #778da9;">Volatility</small><br><b style="color: {color};">{vol:.2f}%</b></div>
                <div><small style="color: #778da9;">Current Price</small><br><b>${asset.get('current_price', 0):,}</b></div>
                <div><small style="color: #778da9;">24h High</small><br><b style="color: #06d6a0;">${asset.get('high_24h', 0):,}</b></div>
                <div><small style="color: #778da9;">24h Low</small><br><b style="color: #ef476f;">${asset.get('low_24h', 0):,}</b></div>
            </div>
        </div>
        """, unsafe_allow_html=True)

    # --- DOWNLOAD EXPORT ---
    st.write("<br>", unsafe_allow_html=True)
    csv = pd.DataFrame(data)[['name', 'current_price', 'price_change_percentage_24h']].to_csv(index=False).encode('utf-8')
    st.download_button(label="📥 EXPORT FINAL RISK CLASSIFICATION", data=csv, file_name="risk_report.csv", use_container_width=True)
