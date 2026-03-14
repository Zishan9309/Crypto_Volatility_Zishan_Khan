import streamlit as st

def render_risk_classification(data):
    # Custom CSS for the specific card designs in the image
    st.markdown("""
    <style>
        .risk-card {
            padding: 20px;
            border-radius: 15px;
            margin-bottom: 15px;
            color: white;
            min-height: 100px;
            box-shadow: 0 4px 15px rgba(0,0,0,0.3);
        }
        .high-risk-card { background: linear-gradient(135deg, #d0312d 0%, #990f02 100%); border-left: 5px solid #ff4b2b; }
        .med-risk-card { background: linear-gradient(135deg, #f0a500 0%, #cf7500 100%); border-left: 5px solid #ffd166; }
        .low-risk-card { background: linear-gradient(135deg, #0b8457 0%, #055e3d 100%); border-left: 5px solid #06d6a0; }
        
        .card-name { font-size: 18px; font-weight: 800; margin-bottom: 5px; }
        .card-val { font-size: 16px; opacity: 0.9; }
        
        .section-header { color: #4cc9f0; font-weight: 700; margin-bottom: 10px; display: flex; align-items: center; }
        .bullet-list { color: white; list-style-type: none; padding-left: 0; line-height: 1.8; }
        .bullet-list li::before { content: "• "; color: #4cc9f0; font-weight: bold; }
    </style>
    """, unsafe_allow_html=True)

    # --- MAIN PAGE LAYOUT ---
    st.markdown("<h1 style='color:white;'>🔷 Milestone 4: Risk Classification & Reporting</h1>", unsafe_allow_html=True)
    st.markdown("<p style='color:#778da9; margin-top:-20px;'>Final Analysis – Crypto Volatility and Risk Analyzer</p>", unsafe_allow_html=True)
    st.write("---")

    col_left, col_right = st.columns([1, 3])

    # --- LEFT SIDEBAR (Requirements & Outputs) ---
    with col_left:
        st.markdown("<div class='section-header'>📋 Requirements</div>", unsafe_allow_html=True)
        st.markdown("""<ul class='bullet-list'>
            <li>Risk thresholds for classification</li>
            <li>Visual highlighting of high-risk assets</li>
            <li>Summary reports (CSV, PNG, PDF)</li>
            <li>System validation & documentation</li>
        </ul>""", unsafe_allow_html=True)

        st.markdown("<br><div class='section-header'>📔 Outputs</div>", unsafe_allow_html=True)
        st.markdown("""<ul class='bullet-list'>
            <li>Complete dashboard with risk classification</li>
            <li>Categorized risk report with metrics</li>
            <li>Documentation & deployment guide</li>
        </ul>""", unsafe_allow_html=True)

        st.markdown("<br><div class='section-header'>📊 Project Completion Status</div>", unsafe_allow_html=True)
        st.progress(100)
        st.success("Milestone 4 Verified")

    # --- RIGHT SIDEBAR (Risk Classification Dashboard) ---
    with col_right:
        st.markdown("<div class='section-header'>📊 Risk Classification Dashboard</div>", unsafe_allow_html=True)
        
        c1, c2, c3 = st.columns(3)
        
        # Categorize data
        high = [c for c in data if abs(c.get('price_change_percentage_24h', 0) or 0) > 5]
        med = [c for c in data if 2 < abs(c.get('price_change_percentage_24h', 0) or 0) <= 5]
        low = [c for c in data if abs(c.get('price_change_percentage_24h', 0) or 0) <= 2]

        with c1:
            st.markdown("<h4 style='color:white;'>🔴 High Risk</h4>", unsafe_allow_html=True)
            for coin in high[:3]:
                st.markdown(f"""<div class="risk-card high-risk-card"><div class="card-name">{coin['name']}</div><div class="card-val">{abs(coin['price_change_percentage_24h']):.2f}%</div></div>""", unsafe_allow_html=True)

        with c2:
            st.markdown("<h4 style='color:white;'>🟡 Medium Risk</h4>", unsafe_allow_html=True)
            for coin in med[:3]:
                st.markdown(f"""<div class="risk-card med-risk-card"><div class="card-name">{coin['name']}</div><div class="card-val">{abs(coin['price_change_percentage_24h']):.2f}%</div></div>""", unsafe_allow_html=True)

        with c3:
            st.markdown("<h4 style='color:white;'>🟢 Low Risk</h4>", unsafe_allow_html=True)
            for coin in low[:3]:
                st.markdown(f"""<div class="risk-card low-risk-card"><div class="card-name">{coin['name']}</div><div class="card-val">{abs(coin['price_change_percentage_24h']):.2f}%</div></div>""", unsafe_allow_html=True)

        # --- RISK SUMMARY REPORT SECTION ---
        st.write("<br>", unsafe_allow_html=True)
        st.markdown("<div class='section-header'>📄 Risk Summary Report</div>", unsafe_allow_html=True)
        
        avg_vol = sum(abs(c.get('price_change_percentage_24h', 0) or 0) for c in data) / len(data) if data else 0
        
        st.markdown(f"""
        <div style="background:#1b263b; padding:20px; border-radius:12px; color:white;">
            Total Cryptocurrencies: <b>{len(data)}</b><br>
            Average Volatility: <b>{avg_vol:.2f}%</b><br>
            Risk Distribution:<br>
            <b>{len(high)} High / {len(med)} Medium / {len(low)} Low</b>
        </div>
        """, unsafe_allow_html=True)
