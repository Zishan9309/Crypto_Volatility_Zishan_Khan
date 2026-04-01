import streamlit as st
import pandas as pd
import plotly.graph_objects as go


def render_risk_classification(data):
    # ─────────────────────────────────────────────────────────────────────────
    # STYLING
    # ─────────────────────────────────────────────────────────────────────────
    st.markdown("""
    <style>
        @import url('https://fonts.googleapis.com/css2?family=Space+Grotesk:wght@400;600;700;800;900&display=swap');

        /* ── RISK CARDS ── */
        .risk-card {
            padding: 13px 14px;
            border-radius: 12px;
            margin-bottom: 8px;
            color: white;
            text-align: left;
            border: 1px solid rgba(255,255,255,0.08);
            transition: transform 0.25s, box-shadow 0.25s;
            backdrop-filter: blur(5px);
            animation: fadeInUp 0.35s ease both;
        }
        .risk-card:hover {
            transform: scale(1.025);
            box-shadow: 0 8px 20px rgba(0,0,0,0.45);
        }
        .high-risk-block { background: linear-gradient(135deg, rgba(208,49,45,0.9), rgba(153,15,2,0.9));  border-left: 4px solid #ff4b2b; }
        .med-risk-block  { background: linear-gradient(135deg, rgba(240,165,0,0.9), rgba(207,117,0,0.9)); border-left: 4px solid #ffd166; }
        .low-risk-block  { background: linear-gradient(135deg, rgba(11,132,87,0.9), rgba(5,94,61,0.9));   border-left: 4px solid #06d6a0; }

        .card-title { font-size: 11px; font-weight: 800; text-transform: uppercase; color: rgba(255,255,255,0.6); margin-bottom: 2px; }
        .card-name  { font-size: 15px; font-weight: 900; margin-bottom: 4px; }
        .card-val   { font-size: 13px; font-weight: 700; color: #ffffff; }

        /* ── VERDICT BOX ── */
        .verdict-container {
            background: #1b263b;
            padding: 24px 20px;
            border-radius: 16px;
            border: 1px solid #415a77;
            text-align: center;
        }

        /* ── ADVISOR CARD ── */
        .advisor-card {
            background: rgba(27, 38, 59, 0.8);
            border-radius: 20px;
            padding: 24px;
            color: white;
            transition: 0.5s;
        }

        /* ── HEATMAP ── */
        .heatmap-grid {
            display: grid;
            grid-template-columns: repeat(5, 1fr);
            gap: 6px;
            margin-bottom: 10px;
        }
        .heatmap-cell {
            border-radius: 10px;
            padding: 10px 8px;
            text-align: center;
            transition: transform 0.2s, box-shadow 0.2s;
        }
        .heatmap-cell:hover {
            transform: scale(1.06);
            box-shadow: 0 6px 18px rgba(0,0,0,0.5);
        }
        .hm-sym  { font-size: 11px; font-weight: 800; letter-spacing: 0.5px; opacity: 0.85; }
        .hm-val  { font-size: 14px; font-weight: 900; margin-top: 2px; }
        .hm-name { font-size: 9px;  opacity: 0.6; margin-top: 2px; white-space: nowrap; overflow: hidden; text-overflow: ellipsis; }

        .legend-wrap {
            display: flex; align-items: center; gap: 8px;
            margin-top: 8px; font-size: 11px; color: #778da9;
        }
        .legend-bar {
            height: 10px; flex: 1; border-radius: 5px;
            background: linear-gradient(90deg, #06d6a0, #ffd166, #ef476f);
        }

        .section-header {
            color: #ffffff; font-size: 16px; font-weight: 800;
            margin-bottom: 12px; margin-top: 4px;
        }

        @keyframes fadeInUp {
            from { opacity: 0; transform: translateY(10px); }
            to   { opacity: 1; transform: translateY(0); }
        }
    </style>
    """, unsafe_allow_html=True)

    # ─────────────────────────────────────────────────────────────────────────
    # GUARD — empty data
    # ─────────────────────────────────────────────────────────────────────────
    if not data:
        st.warning("⚠️ No data available. Please refresh the API on the Data Acquisition tab.")
        return

    # ─────────────────────────────────────────────────────────────────────────
    # HEADER
    # ─────────────────────────────────────────────────────────────────────────
    st.markdown("<h1 style='color:#4cc9f0; text-align:center; letter-spacing:2px;'>📊 RISK CLASSIFICATION</h1>", unsafe_allow_html=True)
    st.markdown("<p style='text-align:center; color:#778da9; font-size:12px; letter-spacing:3px; margin-top:-10px;'></p>", unsafe_allow_html=True)
    st.write("---")

    # ─────────────────────────────────────────────────────────────────────────
    # CONFIGURE THRESHOLDS
    # ─────────────────────────────────────────────────────────────────────────
    with st.expander("🛠️ CONFIGURE RISK THRESHOLDS"):
        high_cutoff = st.slider("High Risk Definition (%)", 3.0, 10.0, 5.0, step=0.5, key="rc_high")
        med_cutoff  = st.slider("Medium Risk Definition (%)", 1.0, float(high_cutoff - 0.5), 2.5, step=0.5, key="rc_med")

    # ─────────────────────────────────────────────────────────────────────────
    # CLASSIFICATION  — same logic as original
    # ─────────────────────────────────────────────────────────────────────────
    high = [c for c in data if abs(c.get('price_change_percentage_24h', 0) or 0) >= high_cutoff]
    med  = [c for c in data if med_cutoff <= abs(c.get('price_change_percentage_24h', 0) or 0) < high_cutoff]
    low  = [c for c in data if abs(c.get('price_change_percentage_24h', 0) or 0) < med_cutoff]

    # ─────────────────────────────────────────────────────────────────────────
    # TOP ROW — DONUT + VERDICT
    # ─────────────────────────────────────────────────────────────────────────
    col_donut, col_verdict = st.columns([2, 1])

    with col_donut:
        st.markdown("<div class='section-header'>🍩 Asset Risk Distribution</div>", unsafe_allow_html=True)
        fig = go.Figure(data=[go.Pie(
            labels=['High Risk', 'Medium Risk', 'Low Risk'],
            values=[len(high), len(med), len(low)],
            hole=0.6,
            marker_colors=['#ef476f', '#ffd166', '#06d6a0'],
            textinfo='percent+label',
            pull=[0.1, 0, 0]
        )])
        fig.update_layout(
            paper_bgcolor='rgba(0,0,0,0)',
            plot_bgcolor='rgba(0,0,0,0)',
            height=300,
            font_color="white",
            font=dict(family="Space Grotesk"),
            margin=dict(t=0, b=0, l=0, r=0),
            showlegend=False
        )
        st.plotly_chart(fig, use_container_width=True)

    with col_verdict:
        avg_v    = sum(abs(c.get('price_change_percentage_24h', 0) or 0) for c in data) / len(data)
        v_status = "VOLATILE" if avg_v > 4 else "STABLE"
        v_color  = "#ef476f"  if avg_v > 4 else "#06d6a0"
        st.markdown(f"""
        <div class="verdict-container">
            <div style="color:#778da9; font-size:11px; font-weight:700; letter-spacing:2px;">MARKET HEALTH</div>
            <div style="color:{v_color}; font-size:30px; font-weight:900; margin:10px 0;">{v_status}</div>
            <div style="font-size:22px; font-weight:800; color:white;">{avg_v:.2f}%</div>
            <div style="color:#4cc9f0; font-size:11px; letter-spacing:2px;">AVG 24H DELTA</div>
        </div>
        """, unsafe_allow_html=True)

    # ─────────────────────────────────────────────────────────────────────────
    # CLASSIFIED ASSET CLUSTERS  — same logic as original
    # ─────────────────────────────────────────────────────────────────────────
    st.markdown("<div class='section-header'>🗂️ Classified Asset Clusters</div>", unsafe_allow_html=True)
    c1, c2, c3 = st.columns(3)

    with c1:
        st.markdown(f"<p style='color:#ef476f; font-weight:800; font-size:13px;'>🔴 CRITICAL ASSETS ({len(high)})</p>", unsafe_allow_html=True)
        for coin in high[:5]:
            st.markdown(f"""
            <div class="risk-card high-risk-block">
                <div class="card-title">Rank #{coin.get('market_cap_rank', '—')}</div>
                <div class="card-name">{coin['name']}</div>
                <div class="card-val">{abs(coin.get('price_change_percentage_24h', 0) or 0):.2f}% Volatility</div>
            </div>""", unsafe_allow_html=True)

    with c2:
        st.markdown(f"<p style='color:#ffd166; font-weight:800; font-size:13px;'>🟡 WARNING ZONE ({len(med)})</p>", unsafe_allow_html=True)
        for coin in med[:5]:
            st.markdown(f"""
            <div class="risk-card med-risk-block">
                <div class="card-title">Rank #{coin.get('market_cap_rank', '—')}</div>
                <div class="card-name">{coin['name']}</div>
                <div class="card-val">{abs(coin.get('price_change_percentage_24h', 0) or 0):.2f}% Volatility</div>
            </div>""", unsafe_allow_html=True)

    with c3:
        st.markdown(f"<p style='color:#06d6a0; font-weight:800; font-size:13px;'>🟢 SECURE ASSETS ({len(low)})</p>", unsafe_allow_html=True)
        for coin in low[:5]:
            st.markdown(f"""
            <div class="risk-card low-risk-block">
                <div class="card-title">Rank #{coin.get('market_cap_rank', '—')}</div>
                <div class="card-name">{coin['name']}</div>
                <div class="card-val">{abs(coin.get('price_change_percentage_24h', 0) or 0):.2f}% Volatility</div>
            </div>""", unsafe_allow_html=True)

    st.write("---")

    # ─────────────────────────────────────────────────────────────────────────
    # NEW — VOLATILITY HEATMAP
    # ─────────────────────────────────────────────────────────────────────────
    st.markdown("<div class='section-header'>🔥 Volatility Heatmap</div>", unsafe_allow_html=True)

    def heat_color(vol):
        t = min(vol / 10.0, 1.0)
        if t < 0.5:
            u = t * 2
            r = int(6   + (255 - 6)   * u)
            g = int(214 + (209 - 214) * u)
            b = int(160 + (102 - 160) * u)
        else:
            u = (t - 0.5) * 2
            r = int(255 + (239 - 255) * u)
            g = int(209 + (71  - 209) * u)
            b = int(102 + (111 - 102) * u)
        return f"rgb({min(255,r)},{max(0,g)},{max(0,b)})"

    cells_html = ""
    for coin in data:
        vol   = abs(coin.get('price_change_percentage_24h', 0) or 0)
        col   = heat_color(vol)
        direc = "▲" if (coin.get('price_change_percentage_24h', 0) or 0) >= 0 else "▼"
        alpha = 0.15 + 0.45 * min(vol / 10.0, 1.0)
        rgb_vals = col.replace("rgb(", "").replace(")", "")
        cells_html += f"""
        <div class="heatmap-cell"
             style="background:rgba({rgb_vals},{alpha:.2f}); border:1px solid {col}40;"
             title="{coin['name']}: {vol:.2f}%">
            <div class="hm-sym" style="color:{col};">{coin.get('symbol','').upper()}</div>
            <div class="hm-val" style="color:{col};">{direc}{vol:.1f}%</div>
            <div class="hm-name">{coin['name']}</div>
        </div>"""

    st.markdown(f"""
    <div style="background:#1b263b; border:1px solid #415a77; border-radius:16px; padding:16px; margin-bottom:18px;">
        <div class="heatmap-grid">{cells_html}</div>
        <div class="legend-wrap">
            <span>Low</span>
            <div class="legend-bar"></div>
            <span>High</span>
        </div>
    </div>
    """, unsafe_allow_html=True)

    st.write("---")

    # ─────────────────────────────────────────────────────────────────────────
    # AI STRATEGIC PORTFOLIO ADVISOR  — same logic as original
    # ─────────────────────────────────────────────────────────────────────────
    st.markdown("<div class='section-header'> Portfolio Advisor</div>", unsafe_allow_html=True)

    sel_coin = st.selectbox(
        "Select Asset for personalised risk strategy:",
        options=[c['name'] for c in data],
        key="rc_advisor_select"
    )
    asset = next((c for c in data if c['name'] == sel_coin), None)

    if asset:
        vol = abs(asset.get('price_change_percentage_24h', 0) or 0)

        if vol >= high_cutoff:
            status, color, shadow = "CRITICAL RISK", "#ef476f", "rgba(239,71,111,0.4)"
            advice  = "🚨 High Danger! Use 1x leverage only. Extreme volatility detected. Avoid long-term entry here."
            signals = ["🛑 Reduce Exposure", "📉 De-risk Portfolio", "⚠️ High Slippage"]
        elif vol >= med_cutoff:
            status, color, shadow = "MODERATE RISK", "#ffd166", "rgba(255,209,102,0.4)"
            advice  = "⚖️ Moderate Risk. Suitable for swing trading with tight stop-losses. Monitor support levels."
            signals = ["⚖️ Balanced Entry", "📈 Trailing Stop", "🔍 Monitor Support"]
        else:
            status, color, shadow = "SECURE / STABLE", "#06d6a0", "rgba(6,214,160,0.4)"
            advice  = "🛡️ Secure. Good for long-term holding. Low volatility baseline ideal for DCA strategies."
            signals = ["🛡️ Accumulation Zone", "💎 HODL Candidate", "✅ Value Asset"]

        def fmt_price(v):
            if v is None:   return "N/A"
            if v >= 1:      return f"${v:,.2f}"
            if v >= 0.001:  return f"${v:.4f}"
            return f"${v:.2e}"

        signals_html = "".join(
            [f'<div style="margin-bottom:5px; font-size:14px;">{s}</div>' for s in signals]
        )

        st.markdown(f"""
        <div class="advisor-card" style="border:2px solid {color}; box-shadow:0 10px 30px {shadow};">
            <div style="display:flex; justify-content:space-between; align-items:center; margin-bottom:20px;">
                <div>
                    <span style="color:{color}; font-weight:800; font-size:12px; letter-spacing:1px;">STRATEGIC VERDICT</span>
                    <h2 style="margin:4px 0 0 0; color:white; font-size:20px;">
                        {sel_coin}
                        <small style="font-size:13px; color:#778da9;">({asset.get('symbol','').upper()})</small>
                    </h2>
                </div>
                <div style="background:{color}; color:#0d1b2a; padding:8px 20px; border-radius:50px; font-weight:900; font-size:13px;">
                    {status}
                </div>
            </div>
            <div style="display:flex; gap:24px; margin-bottom:20px;">
                <div style="flex:2; font-size:15px; line-height:1.7;">{advice}</div>
                <div style="flex:1; background:rgba(0,0,0,0.2); padding:14px; border-radius:14px;">
                    <p style="margin:0 0 8px 0; font-weight:700; font-size:12px; color:{color};">SIGNALS:</p>
                    {signals_html}
                </div>
            </div>
            <div style="display:grid; grid-template-columns:repeat(4,1fr); gap:14px;
                        border-top:1px solid rgba(255,255,255,0.08); padding-top:16px;">
                <div>
                    <small style="color:#778da9; font-size:11px;">Volatility</small><br>
                    <b style="color:{color}; font-size:15px;">{vol:.2f}%</b>
                </div>
                <div>
                    <small style="color:#778da9; font-size:11px;">Current Price</small><br>
                    <b style="font-size:15px;">{fmt_price(asset.get('current_price'))}</b>
                </div>
                <div>
                    <small style="color:#778da9; font-size:11px;">24h High</small><br>
                    <b style="color:#06d6a0; font-size:15px;">{fmt_price(asset.get('high_24h'))}</b>
                </div>
                <div>
                    <small style="color:#778da9; font-size:11px;">24h Low</small><br>
                    <b style="color:#ef476f; font-size:15px;">{fmt_price(asset.get('low_24h'))}</b>
                </div>
            </div>
        </div>
        """, unsafe_allow_html=True)

    # ─────────────────────────────────────────────────────────────────────────
    # EXPORT
    # ─────────────────────────────────────────────────────────────────────────
    st.write("<br>", unsafe_allow_html=True)
    csv = (
        pd.DataFrame(data)[['name', 'symbol', 'current_price', 'price_change_percentage_24h', 'market_cap_rank']]
        .to_csv(index=False)
        .encode('utf-8')
    )
    st.download_button(
        label="📥 EXPORT FINAL RISK CLASSIFICATION",
        data=csv,
        file_name="risk_report.csv",
        use_container_width=True,
        key="rc_export"
    )
