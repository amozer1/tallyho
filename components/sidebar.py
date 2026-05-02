import streamlit as st
import base64


def get_base64_image(image_path):
    with open(image_path, "rb") as img_file:
        return base64.b64encode(img_file.read()).decode()


def render_sidebar(datasets: dict):
    """
    datasets = {
        "Tally Ho": df1,
        "Ferry PS": df2,
        "Rossal Outfall": df3,
        "Flass Lane": df4
    }
    """

    logo_base64 = get_base64_image("assets/logo.png")

    # STYLE
    st.markdown("""
    <style>
        [data-testid="stSidebarNav"] {display:none;}
        [data-testid="stSidebarNavItems"] {display:none;}

        section[data-testid="stSidebar"] {
            background: linear-gradient(180deg, #08111f 0%, #0b1a2f 100%);
        }

        .section-title {
            color:#b8b8d1;
            font-size:12px;
            margin-top:15px;
            margin-bottom:5px;
        }
    </style>
    """, unsafe_allow_html=True)

    with st.sidebar:

        # LOGO
        st.markdown(f"""
        <div style="text-align:center; padding:10px 0 20px 0;">
            <img src="data:image/png;base64,{logo_base64}" width="80">
        </div>
        """, unsafe_allow_html=True)

        # -------------------------
        # 🔽 ASSET SELECTOR
        # -------------------------
        st.markdown('<div class="section-title">ASSET</div>', unsafe_allow_html=True)

        asset = st.radio(
            "",
            list(datasets.keys())
        )

        df = datasets[asset]

        # CLEAN COLUMNS
        df = df.copy()
        df.columns = df.columns.str.strip().str.lower()

        # -------------------------
        # 🔽 OPTIONAL FILTERS
        # -------------------------
        st.markdown('<div class="section-title">FILTER</div>', unsafe_allow_html=True)

        doc_type = st.selectbox(
            "Doc Type",
            ["All"] + sorted(df["doc type"].dropna().unique().tolist())
        )

        status = st.selectbox(
            "Status",
            ["All"] + sorted(df["status"].dropna().unique().tolist())
        )

        filtered_df = df.copy()

        if doc_type != "All":
            filtered_df = filtered_df[filtered_df["doc type"] == doc_type]

        if status != "All":
            filtered_df = filtered_df[filtered_df["status"] == status]

        # -------------------------
        # 🔽 SEQUENCE SELECTOR
        # -------------------------
        st.markdown('<div class="section-title">SEQUENCE</div>', unsafe_allow_html=True)

        seq_list = sorted(filtered_df["seq no"].dropna().unique().tolist())

        seq_choice = st.selectbox(
            "Select Seq No",
            seq_list
        )

        return asset, filtered_df, seq_choice