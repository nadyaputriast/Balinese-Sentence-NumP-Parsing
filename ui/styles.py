import streamlit as st

# ============================================================
# FIX 4: CSS di-build SEKALI sebagai module-level constant.
#         apply_styles() hanya memilih antara dua string yang
#         sudah jadi — tidak ada f-string rebuild tiap rerun.
# ============================================================

def _build_css(dark_mode: bool) -> str:
    if dark_mode:
        bg_color       = "#020617"
        sidebar_bg     = "#0f172a"
        card_bg        = "#1e293b"
        text_primary   = "#ffffff"
        text_secondary = "#94a3b8"
        border_color   = "#334155"
        accent_color   = "#38bdf8"
        chip_bg        = "#334155"
        input_bg       = "#1e293b"
        btn_hover_bg   = "rgba(56, 189, 248, 0.15)"
    else:
        bg_color       = "#f8fafc"
        sidebar_bg     = "#ffffff"
        card_bg        = "#ffffff"
        text_primary   = "#0f172a"
        text_secondary = "#64748b"
        border_color   = "#e2e8f0"
        accent_color   = "#0284c7"
        chip_bg        = "#f1f5f9"
        input_bg       = "#ffffff"
        btn_hover_bg   = "rgba(2, 132, 199, 0.1)"

    return f"""
    <style>
        @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&family=JetBrains+Mono:wght@400;500&display=swap');

        .stApp {{
            background-color: {bg_color};
            color: {text_primary} !important;
            font-family: 'Inter', sans-serif;
            transition: background-color 0.3s ease;
        }}
        .main, .block-container, .st-emotion-cache-1wrcr25,
        .st-emotion-cache-uf99v8, .st-emotion-cache-1avcm0n {{
            background-color: {bg_color} !important;
        }}
        .stAlert-success {{
            background-color: #16a34a22 !important;
            color: #16a34a !important;
            border-left: 6px solid #16a34a !important;
        }}
        .stAlert-error {{
            background-color: #dc262622 !important;
            color: #dc2626 !important;
            border-left: 6px solid #dc2626 !important;
        }}
        .stAlert-info {{
            background-color: #38bdf822 !important;
            color: #0284c7 !important;
            border-left: 6px solid #38bdf8 !important;
        }}
        .stAlert-warning {{
            background-color: #facc1522 !important;
            color: #b45309 !important;
            border-left: 6px solid #facc15 !important;
        }}
        .cyk-table th {{
            background-color: {chip_bg};
            color: {text_primary};
            border-bottom: 2px solid {accent_color};
            font-weight: bold;
        }}
        section[data-testid="stSidebar"] {{
            background-color: {sidebar_bg};
            border-right: 1px solid {border_color};
        }}
        section[data-testid="stSidebar"] h1,
        section[data-testid="stSidebar"] h2,
        section[data-testid="stSidebar"] h3,
        section[data-testid="stSidebar"] label,
        section[data-testid="stSidebar"] span,
        section[data-testid="stSidebar"] p,
        section[data-testid="stSidebar"] div {{
            color: {text_primary} !important;
        }}
        section[data-testid="stSidebar"] .stRadio div[role="radiogroup"] label {{
            background-color: transparent !important;
            color: {text_primary} !important;
        }}
        .custom-card, .cyk-table {{
            box-shadow: 0 2px 8px 0 rgba(0,0,0,0.07);
        }}
        .cyk-table td {{
            background-color: {card_bg};
            color: {text_primary};
        }}
        .stTextInput input {{
            background-color: {input_bg} !important;
            color: {text_primary} !important;
            border: 1px solid {border_color} !important;
            border-radius: 8px;
            padding: 0.75rem 1rem;
        }}
        .stTextInput input::placeholder {{
            color: {text_secondary} !important;
            opacity: 0.7;
        }}
        .stTextInput input:focus {{
            border-color: {accent_color} !important;
            box-shadow: 0 0 0 1px {accent_color} !important;
        }}
        div[data-testid="stHorizontalBlock"] button {{
            border-radius: 6px !important;
            padding: 0px 12px !important;
            font-size: 0.9rem !important;
            min-height: 32px !important;
            height: 32px !important;
            line-height: 1 !important;
            font-weight: 700 !important;
            margin: 0px !important;
            border: 1px solid {accent_color} !important;
            background-color: transparent !important;
            color: {accent_color} !important;
            font-family: 'JetBrains Mono', monospace !important;
            transition: all 0.2s;
        }}
        div[data-testid="stHorizontalBlock"] button:hover {{
            background-color: {accent_color} !important;
            color: {bg_color} !important;
            transform: translateY(-1px);
        }}
        button[kind="primary"], div[class*="mic-btn"] button {{
            background-color: {accent_color} !important;
            color: #ffffff !important;
            border: none !important;
            font-weight: 600 !important;
        }}
        .t-chip-static {{
            display: flex; align-items: center; justify-content: center;
            background-color: {chip_bg}; color: {text_primary};
            padding: 0 12px; height: 32px; border-radius: 6px;
            border: 1px solid {border_color};
            font-family: 'JetBrains Mono', monospace; font-size: 0.9rem;
        }}
        .nt-chip-static {{
            display: flex; align-items: center; justify-content: center;
            color: {accent_color};
            padding: 0 8px; height: 32px;
            font-weight: 800; font-family: 'JetBrains Mono', monospace;
            font-size: 1rem;
        }}
        .arrow {{
            display: flex; align-items: center; justify-content: center;
            color: {text_secondary}; opacity: 0.8; font-weight: bold;
            font-size: 1.2rem; height: 32px;
        }}
        .custom-card {{
            background-color: {card_bg};
            border: 1px solid {border_color};
            border-radius: 12px; padding: 1.5rem; margin-bottom: 1rem;
            box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.1);
        }}
        .cyk-table {{
            width: 100%; border-collapse: separate; border-spacing: 0;
            border: 1px solid {border_color}; border-radius: 8px;
            overflow: hidden; background-color: {card_bg};
        }}
        .cyk-table td {{
            padding: 10px; border-right: 1px solid {border_color};
            border-bottom: 1px solid {border_color};
            text-align: center; color: {text_primary};
        }}
        .vocab-grid {{
            display: flex;
            flex-wrap: wrap;
            gap: 8px;
            padding-top: 0.5rem;
        }}
        .vocab-chip {{
            display: inline-block;
            background-color: {card_bg};
            border: 1px solid {border_color};
            color: {text_primary};
            padding: 6px 14px;
            border-radius: 99px;
            font-size: 0.85rem;
            transition: all 0.2s;
            cursor: default;
        }}
        .vocab-chip:hover {{
            border-color: {accent_color};
            color: {accent_color};
            transform: translateY(-1px);
        }}
        .letter-header {{
            font-size: 1.2rem;
            font-weight: 700;
            color: {accent_color};
            margin-top: 1.5rem;
            margin-bottom: 0.5rem;
            border-bottom: 1px solid {border_color};
            padding-bottom: 0.2rem;
        }}
        .streamlit-expanderHeader {{
            background-color: {card_bg} !important;
            color: {text_primary} !important;
            border: 1px solid {border_color} !important;
        }}
        .streamlit-expanderContent {{
            background-color: {bg_color} !important;
            color: {text_primary} !important;
            border: 1px solid {border_color} !important;
            border-top: none !important;
        }}
        .stTextInput {{ margin-bottom: 0px; }}
        div[data-testid="stVerticalBlock"] > div.stTextInput > div > label {{ display: none; }}
    </style>
    """

# Build kedua varian sekali saat modul di-import
_CSS_DARK  = _build_css(dark_mode=True)
_CSS_LIGHT = _build_css(dark_mode=False)


def apply_styles(dark_mode: bool = False) -> None:
    """Inject CSS yang sudah pre-built — nol komputasi saat rerun."""
    st.markdown(_CSS_DARK if dark_mode else _CSS_LIGHT, unsafe_allow_html=True)