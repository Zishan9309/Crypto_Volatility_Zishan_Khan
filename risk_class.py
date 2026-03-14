import streamlit as st
import pandas as pd
import numpy as np
import plotly.graph_objects as go

def render_risk_classification(data):
    # Custom CSS for the specific card designs and new interactive elements
    st.markdown("""
    <style>
        .risk-card {
            padding: 20px;
            border-radius: 15px;
            margin-bottom: 15px;
            color: white;
            min-height: 100px;
            box-shadow: 0 4px 15px rgba(0,0,0,0.3);
            transition: 0.3s;
            text-align: center;
        }
        .risk-card:hover { transform: scale(1.02); }
        .high-risk-card { background: linear-gradient(135deg, #d0312d 0%, #990f02 100%); border-bottom: 5px solid #ff4b2b; }
        .med-risk-card { background: linear-gradient(135deg, #f0a500 0%, #cf7500 100%); border-bottom: 5px solid #ffd166; }
        .low-risk-card { background: linear-gradient(135deg, #0b8457 0%, #055e3d 100%); border-bottom: 5px solid #06d6a0; }
        
        .card-name { font-size: 18px; font-weight: 800; margin-bottom: 5px; }
        .card-val { font-size: 16px; opacity: 0.9; }
        
        .section-header { color: #4cc9f0; font-weight: 700; margin-bottom: 15px; font-size: 24px; text-transform: uppercase; }
        
        .risk-score-box {
            background: #1b263b;
            border: 1px solid #415a77;
            padding: 20px;
            border-radius: 15px;
            text-align: center;
            margin-bottom: 20px;
        }
    </style>
    """, unsafe_allow_html=True)

    # --- HEADER ---
    st.markdown("<h1 style='color:white;'>🛡️ Milestone 4: Advanced Risk Classification</h1>", unsafe_allow_html=True)
    st.markdown("<p style='color:#778da9; margin-top:-20px;'>Final System Validation – Real-time Market Risk Categorization</p>", unsafe_allow_html=True)
    st.write("---")

    # --- TOP INTERACTIVE SECTION: RISK INTENSITY COMPARISON ---
    st.markdown("<div class='section-header'>📊 Risk Intensity Analysis</div>", unsafe_allow_html=True)
    
    col_chart, col_stats = st.columns([2, 1])

    # Logic for categorization
    high = [c for c in data if abs(c.get('price_change_percentage_24h', 0) or 0) > 5]
    med = [c for c in data if 2 < abs(c.get('price_change_percentage_24h', 0) or 0) <= 5]
    low = [c for c in data if abs(c.get('price_change_percentage_24h', 0) or 0) <= 2]

    with col_chart:
        # NEW: Risk Intensity Radar/Bar Chart to show concentration
        categories = ['High Risk', 'Medium Risk', 'Low Risk']
        counts = [len(high), len(med), len(low)]
        
        fig = go.Figure(go.Bar(
            x=categories,
            y=counts,
            marker_color=['#ef476f', '#ffd166', '#06d6a0'],
            text=counts,
            textposition='auto',
        ))
        fig.update_layout(
            paper_bgcolor='rgba(0,0,0,0)',
            plot_bgcolor='rgba(0,0,0,0)',
            font_color="white",
            height=300,
            margin=dict(l=20, r=20, t=20, b=20),
            yaxis=dict(title="Number of Assets", gridcolor="#2b3a4f")
        )
        st.plotly_chart(fig, use_container_width=True)

    with col_stats:
        # NEW: Live AI Risk Verdict
        avg_v = sum(abs(c.get('price_change_percentage_24h', 0) or 0) for c in data) / len(data) if data else 0
        verdict = "⚠️ VOLATILE" if avg_v > 4 else "✅ STABLE"
        v_color = "#ef476f" if avg_v > 4 else "#06d6a0"
        
        st.markdown(f"""
        <div class="risk-score-box">
            <div style="color:#778da9; font-size:12px; font-weight:600;">MARKET HEALTH VERDICT</div>
            <div style="color:{v_color}; font-size:32px; font-weight:900; margin:10px 0;">{verdict}</div>
            <div style="color:white; font-size:14px;">Average Volatility: <b>{avg_v:.2f}%</b></div>
        </div>
        """, unsafe_allow_html=True)
        
        st.info("The system automatically flags assets with >5% movement as High Risk.")

    # --- MIDDLE SECTION: THE RISK CARDS (STAYING AS IS PER IMAGE) ---
    st.markdown("<div class='section-header'>🗂️ Asset Classification Dashboard</div>", unsafe_allow_html=True)
    
    c1, c2, c3 = st.columns(3)

    with c1:
        st.markdown("<h4 style='color:#ef476f; text-align:center;'>🔴 HIGH RISK</h4>", unsafe_allow_html=True)
        for coin in high[:4]:
            st.markdown(f"""<div class="risk-card high-risk-card"><div class="card-name">{coin['name']}</div><div class="card-val">{abs(coin['price_change_percentage_24h']):.2f}% Vol</div></div>""", unsafe_allow_html=True)

    with c2:
        st.markdown("<h4 style='color:#ffd166; text-align:center;'>🟡 MEDIUM RISK</h4>", unsafe_allow_html=True)
        for coin in med[:4]:
            st.markdown(f"""<div class="risk-card med-risk-card"><div class="card-name">{coin['name']}</div><div class="card-val">{abs(coin['price_change_percentage_24h']):.2f}% Vol</div></div>""", unsafe_allow_html=True)

    with c3:
        st.markdown("<h4 style='color:#06d6a0; text-align:center;'>🟢 LOW RISK</h4>", unsafe_allow_html=True)
        for coin in low[:4]:
            st.markdown(f"""<div class="risk-card low-risk-card"><div class="card-name">{coin['name']}</div><div class="card-val">{abs(coin['price_change_percentage_24h']):.2f}% Vol</div></div>""", unsafe_allow_html=True)

    # --- NEW BOTTOM INTERACTIVE ELEMENT: RISK ADVISORY SEARCH ---
    st.write("---")
    st.markdown("<div class='section-header'>🔍 Smart Risk Advisory</div>", unsafe_allow_html=True)
    
    selected_asset = st.selectbox("Select any asset to get a deep-dive risk recommendation:", options=[c['name'] for c in data])
    
    asset_data = next((c for c in data if c['name'] == selected_asset), None)
    
    if asset_data:
        vol = abs(asset_data.get('price_change_percentage_24h', 0))
        if vol > 5:
            advice = "This asset shows extreme volatility. **Recommendation:** Avoid short-term leverage; use hedged positions."
            icon = "❌"
        elif vol > 2:
            advice = "Moderate volatility detected. **Recommendation:** Suitable for growth-oriented portfolios with medium stop-losses."
            icon = "⚖️"
        else:
            advice = "Low volatility observed. **Recommendation:** Ideal for stable long-term holding or value preservation."
            icon = "🛡️"
            
        st.markdown(f"""
        <div style="background:#1b263b; padding:25px; border-radius:15px; border-left:10px solid #4cc9f0; color:white;">
            <h3 style="margin-top:0;">{icon} Advisory for {selected_asset}</h3>
            <p style="font-size:18px;">{advice}</p>
            <hr style="opacity:0.2;">
            <span style="color:#778da9;">Asset Rank: #{asset_data.get('market_cap_rank')} | 24h Low: ${asset_data.get('low_24h'):,}</span>
        </div>
        """, unsafe_allow_html=True)

    # --- FINAL REPORT DOWNLOAD ---
    st.write("<br>", unsafe_allow_html=True)
    full_df = pd.DataFrame(data)[['name', 'current_price', 'price_change_percentage_24h']]
    csv = full_df.to_csv(index=False).encode('utf-8')
    st.download_button(
        label="📥 DOWNLOAD COMPREHENSIVE RISK REPORT (PDF/CSV)",
        data=csv,
        file_name="final_risk_report.csv",
        mime="text/csv",
        use_container_width=True
    )
