import streamlit as st


def render_sidebar():
    with st.sidebar:
        st.markdown("""
        <div style="
            text-align:center;
            padding:10px 0 20px 0;
        ">
            <img src="https://cdn-icons-png.flaticon.com/512/1048/1048953.png" width="60">
        </div>
        """, unsafe_allow_html=True)

        st.markdown("""
        <style>
        .nav-button {
            display:block;
            width:100%;
            padding:10px 14px;
            margin:6px 0;
            border-radius:8px;
            text-decoration:none;
            font-size:14px;
            font-weight:500;
            color:white;
            background:#0b1a2f;
            border:1px solid rgba(255,255,255,0.05);
        }
        .nav-button:hover {
            background:#1f5eff;
            color:white;
        }
        </style>
        """, unsafe_allow_html=True)

        nav_items = [
            "Overview",
            "TQs",
            "RFIs",
            "Analytics",
            "AI Insights",
            "Predictive Risk",
            "Response Performance",
            "Reports",
            "Settings"
        ]

        for item in nav_items:
            st.markdown(
                f'<a href="#" class="nav-button">{item}</a>',
                unsafe_allow_html=True
            )

        st.markdown("<br>", unsafe_allow_html=True)

        st.markdown("""
        <div style="
            background:#18113a;
            padding:15px;
            border-radius:12px;
            border:1px solid rgba(168,85,247,0.25);
        ">
            <div style="
                color:white;
                font-size:15px;
                font-weight:700;
            ">
                AI Assistant
            </div>
            <div style="
                color:#b8b8d1;
                font-size:12px;
                margin-top:6px;
            ">
                Ask anything about your data...
            </div>
        </div>
        """, unsafe_allow_html=True)