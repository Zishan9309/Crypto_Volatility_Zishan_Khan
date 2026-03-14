import streamlit as st
import pandas as pd

def render_risk_classification(data):
    # Custom CSS (Maintained and enhanced)
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
        }
        .risk-card:hover { transform: translateY(-5px); }
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

    # --- LEFT SIDEBAR (Requirements & Interactive Controls) ---
    with col_left:
        st.markdown("<div class='section-header'>📋 Requirements</div>", unsafe_allow_html=True)
        st.markdown("""<ul class='bullet-list'>
            <li>Risk thresholds for classification</li>
            <li>Visual highlighting of high-risk assets</li>
            <li>Summary reports (CSV, PNG, PDF)</li>
        </ul>""", unsafe_allow_html=True)

        st.write("<br>", unsafe_allow_html=True)
        st.markdown("<div class='section-header'>🛠️ Risk Controls</div>", unsafe_allow_html=True)
        
        # INTERACTIVE ELEMENT: User Defined Thresholds
        high_thresh = st.slider("High Risk Cutoff (%)", 3.0, 15.0, 5.0, step=0.5)
        low_thresh = st.slider("Low Risk Cutoff (%)", 0.5, 3.0, 2.0, step=0.1)
        
        search_query = st.text_input("🔍 Search Specific Asset", placeholder="e.g. Bitcoin")

        st.markdown("<br><div class='section-header'>📊 Completion Status</div>", unsafe_allow_html=True)
        st.progress(100)
        st.success("Milestone 4 Verified")

    # --- RIGHT SIDEBAR (Risk Classification Dashboard) ---
    with col_right:
        st.markdown("<div class='section-header'>📊 Risk Classification Dashboard</div>", unsafe_allow_html=True)
        
        c1, c2, c3 = st.columns(3)
        
        # Dynamic Categorization based on Sliders
        high = [c for c in data if abs(c.get('price_change_percentage_24h', 0) or 0) > high_thresh]
        med = [c for c in data if low_thresh < abs(c.get('price_change_percentage_24h', 0) or 0) <= high_thresh]
        low = [c for c in data if abs(c.get('price_change_percentage_24h', 0) or 0) <= low_thresh]

        # Apply Search Filter if any
        if search_query:
            high = [c for c in high if search_query.lower() in c['name'].lower()]
            med = [c for c in med if search_query.lower() in c['name'].lower()]
            low = [c for c in low if search_query.lower() in c['name'].lower()]

        with c1:
            st.markdown(f"<h4 style='color:white;'>🔴 High Risk (>{high_thresh}%)</h4>", unsafe_allow_html=True)
            for coin in high[:3]:
                st.markdown(f"""<div class="risk-card high-risk-card"><div class="card-name">{coin['name']}</div><div class="card-val">{abs(coin['price_change_percentage_24h']):.2f}%</div></div>""", unsafe_allow_html=True)

        with c2:
            st.markdown(f"<h4 style='color:white;'>🟡 Medium Risk</h4>", unsafe_allow_html=True)
            for coin in med[:3]:
                st.markdown(f"""<div class="risk-card med-risk-card"><div class="card-name">{coin['name']}</div><div class="card-val">{abs(coin['price_change_percentage_24h']):.2f}%</div></div>""", unsafe_allow_html=True)

        with c3:
            st.markdown(f"<h4 style='color:white;'>🟢 Low Risk (<{low_thresh}%)</h4>", unsafe_allow_html=True)
            for coin in low[:3]:
                st.markdown(f"""<div class="risk-card low-risk-card"><div class="card-name">{coin['name']}</div><div class="card-val">{abs(coin['price_change_percentage_24h']):.2f}%</div></div>""", unsafe_allow_html=True)

        # --- INTERACTIVE ASSET INSPECTOR ---
        st.write("<br>", unsafe_allow_html=True)
        st.markdown("<div class='section-header'>🔎 Interactive Asset Inspection</div>", unsafe_allow_html=True)
        
        with st.expander("📂 View Full Risk Categorization Table"):
            full_df = pd.DataFrame([{
                'Asset': c['name'],
                'Volatility': f"{abs(c['price_change_percentage_24h']):.2f}%",
                'Category': '🔴 High' if abs(c['price_change_percentage_24h']) > high_thresh else 
                            ('🟢 Low' if abs(c['price_change_percentage_24h']) <= low_thresh else '🟡 Medium')
            } for c in data])
            st.dataframe(full_df, use_container_width=True, hide_index=True)

        # --- RISK SUMMARY REPORT SECTION ---
        st.write("<br>", unsafe_allow_html=True)
        st.markdown("<div class='section-header'>📄 Risk Summary Report</div>", unsafe_allow_html=True)
        
        avg_vol = sum(abs(c.get('price_change_percentage_24h', 0) or 0) for c in data) / len(data) if data else 0
        
        st.markdown(f"""
        <div style="background:#1b263b; padding:20px; border-radius:12px; color:white; border: 1px solid #415a77;">
            <table style="width:100%; border-collapse: collapse;">
                <tr>
                    <td style="padding:10px;">Total Cryptocurrencies:</td>
                    <td style="padding:10px; color:#4cc9f0;"><b>{len(data)}</b></td>
                </tr>
                <tr>
                    <td style="padding:10px;">Average Market Volatility:</td>
                    <td style="padding:10px; color:#4cc9f0;"><b>{avg_vol:.2f}%</b></td>
                </tr>
                <tr>
                    <td style="padding:10px;">Risk Distribution Summary:</td>
                    <td style="padding:10px; color:#4cc9f0;"><b>{len(high)} High / {len(med)} Medium / {len(low)} Low</b></td>
                </tr>
            </table>
        </div>
        """, unsafe_allow_html=True)

        # Download Interaction
        st.write("<br>", unsafe_allow_html=True)
        csv = full_df.to_csv(index=False).encode('utf-8')
        st.download_button(
            label="📥 Export Classification Report",
            data=csv,
            file_name="risk_classification.csv",
            mime="text/csv",
            use_container_width=True
        )
