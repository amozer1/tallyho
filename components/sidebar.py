import streamlit as st
import base64


def get_base64_image(image_path):
    with open(image_path, "rb") as img_file:
        return base64.b64encode(img_file.read()).decode()


def render_sidebar():
    logo_base64 = get_base64_image("assets/logo.png")

    with st.sidebar:
        # =========================
        # SIDEBAR STYLE
        # =========================
        st.markdown("""
        <style>
            section[data-testid="stSidebar"] {
                background: linear-gradient(180deg, #08111f 0%, #0b1a2f 100%);
            }

            .nav-button {
                display:block;
                width:100%;
                padding:12px 14px;
                margin:6px 0;
                border-radius:10px;
                text-decoration:none;
                font-size:14px;
                font-weight:500;
                color:white;
                background:#0f223b;
                border:1px solid rgba(255,255,255,0.05);
                transition:0.3s;
            }

            .nav-button:hover {
                background:#1f5eff;
                color:white;
            }

            .assistant-box {
                background:#17113a;
                padding:16px;
                border-radius:12px;
                border:1px solid rgba(168,85,247,0.25);
                margin-top:30px;
            }
        </style>
        """, unsafe_allow_html=True)

        # =========================
        # LOGO
        # =========================
        st.markdown(f"""
        <div style="text-align:center; padding:10px 0 25px 0;">
            <img src="data:image/png;base64,{logo_base64}" width="85">
        </div>
        """, unsafe_allow_html=True)

        # =========================
        # NAVIGATION
        # =========================
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

        # =========================
        # AI ASSISTANT
        # =========================
        st.markdown("""
        <div class="assistant-box">
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