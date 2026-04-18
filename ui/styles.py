import streamlit as st

def _build_css(dark_mode: bool) -> str:
    # Definisi Palet Warna
    if dark_mode:
        bg_color       = "#020617"  # Slate 950 (Sangat gelap)
        sidebar_bg     = "#0f172a"  # Slate 900
        card_bg        = "#1e293b"  # Slate 800
        text_primary   = "#f8fafc"  # Slate 50 (Putih terang)
        text_secondary = "#94a3b8"  # Slate 400 (Abu-abu)
        border_color   = "#334155"  # Slate 700
        accent_color   = "#38bdf8"  # Sky 400 (Biru terang)
        chip_bg        = "#334155"  # Slate 700
        input_bg       = "#0f172a"  # Slate 900
        btn_hover_bg   = "rgba(56, 189, 248, 0.15)"
        success_bg     = "rgba(16, 185, 129, 0.15)"
        error_bg       = "rgba(239, 68, 68, 0.15)"
        chat_bg        = "rgba(255, 255, 255, 0.05)"
        chat_border    = "rgba(255, 255, 255, 0.1)"
    else:
        bg_color       = "#f8fafc"  # Slate 50
        sidebar_bg     = "#ffffff"  # Putih
        card_bg        = "#ffffff"  # Putih
        text_primary   = "#0f172a"  # Slate 900 (Hitam pekat)
        text_secondary = "#64748b"  # Slate 500 (Abu-abu)
        border_color   = "#e2e8f0"  # Slate 200
        accent_color   = "#0284c7"  # Sky 600
        chip_bg        = "#f1f5f9"  # Slate 100
        input_bg       = "#ffffff"  # Putih
        btn_hover_bg   = "rgba(2, 132, 199, 0.1)"
        success_bg     = "rgba(16, 185, 129, 0.1)"
        error_bg       = "rgba(239, 68, 68, 0.1)"
        chat_bg        = "rgba(0, 0, 0, 0.03)"
        chat_border    = "rgba(0, 0, 0, 0.08)"

    return f"""
    <style>
        @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&family=JetBrains+Mono:wght@400;500;600&display=swap');

        /* ========== GLOBAL TEXT & BACKGROUND ========== */
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
        
        p, span, li, h1, h2, h3, h4, h5, h6 {{
            color: {text_primary} !important;
        }}
        
        /* ========== ALERTS & NOTIFICATIONS ========== */
        .stAlert {{
            border-radius: 12px !important;
            padding: 1rem 1.25rem !important;
            border-left-width: 4px !important;
            margin: 1rem 0 !important;
        }}
        
        .stAlert-success {{
            background-color: {success_bg} !important;
            color: #10b981 !important;
            border-left-color: #10b981 !important;
        }}
        
        .stAlert-error {{
            background-color: {error_bg} !important;
            color: #ef4444 !important;
            border-left-color: #ef4444 !important;
        }}
        
        /* ========== SIDEBAR ========== */
        section[data-testid="stSidebar"] {{
            background-color: {sidebar_bg};
            border-right: 1px solid {border_color};
            padding-top: 2rem;
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
        
        /* ========== CARDS & CONTAINERS ========== */
        .custom-card {{
            background-color: {card_bg};
            border: 1px solid {border_color};
            border-radius: 12px;
            padding: 1.5rem;
            margin-bottom: 1.5rem;
            box-shadow: 0 1px 3px 0 rgba(0, 0, 0, 0.1), 0 1px 2px 0 rgba(0, 0, 0, 0.06);
            transition: all 0.2s;
        }}
        
        /* ========== CYK TABLE ========== */
        .cyk-table {{
            width: 100%;
            border-collapse: separate;
            border-spacing: 0;
            border: 1px solid {border_color};
            border-radius: 10px;
            overflow: hidden;
            background-color: {card_bg};
            box-shadow: 0 2px 8px 0 rgba(0,0,0,0.08);
        }}
        
        .cyk-table th {{
            background-color: {chip_bg};
            color: {text_primary};
            border-bottom: 2px solid {accent_color};
            font-weight: 700;
            padding: 12px;
            font-family: 'JetBrains Mono', monospace;
        }}
        
        .cyk-table td {{
            padding: 12px;
            border-right: 1px solid {border_color};
            border-bottom: 1px solid {border_color};
            text-align: center;
            color: {text_primary};
            background-color: {card_bg};
            font-family: 'JetBrains Mono', monospace;
            font-size: 0.9rem;
        }}
        
        /* ========== INPUT FIELDS & CURSOR FIX ========== */
        .stTextInput input {{
            background-color: {input_bg} !important;
            color: {text_primary} !important;
            caret-color: {accent_color} !important;
            border: 1px solid {border_color} !important;
            border-radius: 8px !important;
            padding: 0.75rem 1rem !important;
            font-family: 'Inter', sans-serif !important;
            transition: all 0.2s !important;
        }}
        
        .stTextInput input::placeholder {{
            color: {text_secondary} !important;
            opacity: 0.7;
        }}
        
        .stTextInput input:focus {{
            border-color: {accent_color} !important;
            box-shadow: 0 0 0 2px rgba(56, 189, 248, 0.2) !important;
            outline: none !important;
        }}
        
        /* ========== BUTTONS ========== */
        .stButton button {{
            border-radius: 8px !important;
            padding: 0.5rem 1.5rem !important;
            font-weight: 600 !important;
            transition: all 0.2s !important;
            border: 1px solid {border_color} !important;
            background-color: {card_bg} !important;
            color: {text_primary} !important;
        }}
        
        .stButton button:hover {{
            background-color: {btn_hover_bg} !important;
            border-color: {accent_color} !important;
            transform: translateY(-1px);
        }}
        
        button[kind="primary"] {{
            background-color: {accent_color} !important;
            color: #ffffff !important;
            border: none !important;
        }}
        
        button[kind="primary"]:hover {{
            background-color: #0ea5e9 !important;
            transform: translateY(-1px);
        }}

        /* Tombol Download PDF */
        .stDownloadButton button {{
            background-color: #10b981 !important;
            color: white !important;
            border: none !important;
            font-weight: 600 !important;
        }}
        
        .stDownloadButton button:hover {{
            background-color: #059669 !important;
            transform: translateY(-1px);
        }}

        /* Tombol Rule Inline */
        div[data-testid="stHorizontalBlock"] button {{
            border-radius: 6px !important;
            padding: 0.4rem 1rem !important;
            font-size: 0.9rem !important;
            min-height: 36px !important;
            height: 36px !important;
            line-height: 1 !important;
            font-weight: 700 !important;
            margin: 0px !important;
            border: 1.5px solid {accent_color} !important;
            background-color: transparent !important;
            color: {accent_color} !important;
            font-family: 'JetBrains Mono', monospace !important;
        }}
        
        div[data-testid="stHorizontalBlock"] button:hover {{
            background-color: {accent_color} !important;
            color: #ffffff !important;
            transform: translateY(-2px);
        }}
        
        /* ========== CHIPS (Grammar & Vocab) ========== */
        .t-chip-static {{
            display: flex;
            align-items: center;
            justify-content: center;
            background-color: {chip_bg};
            color: {text_primary};
            padding: 0 14px;
            height: 36px;
            border-radius: 6px;
            border: 1px solid {border_color};
            font-family: 'JetBrains Mono', monospace;
            font-size: 0.9rem;
            font-weight: 500;
        }}
        
        .nt-chip-static {{
            display: flex;
            align-items: center;
            justify-content: center;
            color: {accent_color};
            padding: 0 10px;
            height: 36px;
            font-weight: 800;
            font-family: 'JetBrains Mono', monospace;
            font-size: 1.05rem;
        }}
        
        .arrow {{
            display: flex;
            align-items: center;
            justify-content: center;
            color: {text_secondary} !important;
            opacity: 0.7;
            font-weight: bold;
            font-size: 1.3rem;
            height: 36px;
        }}
        
        .vocab-grid {{
            display: flex;
            flex-wrap: wrap;
            gap: 10px;
            padding-top: 0.75rem;
        }}
        
        .vocab-chip {{
            display: inline-block;
            background-color: {card_bg};
            border: 1px solid {border_color};
            color: {text_primary};
            padding: 8px 16px;
            border-radius: 20px;
            font-size: 0.9rem;
            font-weight: 500;
            transition: all 0.2s;
            cursor: pointer;
        }}
        
        .vocab-chip:hover {{
            border-color: {accent_color};
            color: {accent_color} !important;
            transform: translateY(-2px);
        }}
        
        /* ========== WIDGET LABELS & CHECKBOXES FIX ========== */
        [data-testid="stCheckbox"] label p, 
        [data-testid="stWidgetLabel"] p,
        .stCheckbox label span {{
            color: {text_primary} !important;
            font-weight: 500;
        }}

        /* ========== EXPANDERS FIX ========== */
        [data-testid="stExpander"] details summary {{
            background-color: {card_bg} !important;
            border: 1px solid {border_color} !important;
            border-radius: 8px !important;
            padding: 1rem !important;
            transition: all 0.2s !important;
        }}
        
        [data-testid="stExpander"] details summary:hover {{
            background-color: {btn_hover_bg} !important;
            border-color: {accent_color} !important;
        }}
        
        [data-testid="stExpander"] details summary p {{
            color: {text_primary} !important;
            font-weight: 600 !important;
        }}
        
        [data-testid="stExpander"] details summary svg {{
            fill: {text_primary} !important;
            color: {text_primary} !important;
        }}
        
        [data-testid="stExpander"] details > div {{
            background-color: {bg_color} !important;
            border: 1px solid {border_color} !important;
            border-top: none !important;
            border-radius: 0 0 10px 10px !important;
            padding: 1rem !important;
        }}
        
        /* ========== DIALOG / MODAL (TANYA AI) FIX ========== */
        /* Memaksa background modal agar sinkron dengan warna card_bg */
        div[role="dialog"],
        div[role="dialog"] > div,
        div[data-testid="stDialog"] > div,
        div[data-testid="stModal"] > div {{
            background-color: {card_bg} !important;
            border-color: {border_color} !important;
        }}
        
        /* Memaksa warna tombol close (X) di pojok kanan atas modal */
        div[role="dialog"] button[aria-label="Close"] svg,
        div[role="dialog"] button[title="Close"] svg {{
            fill: {text_primary} !important;
            stroke: {text_primary} !important;
        }}

        /* Container dalam chat (kotak besar tempat chat berada) */
        div[role="dialog"] [data-testid="stVerticalBlockBorderWrapper"] {{
            background-color: {bg_color} !important;
            border: 1px solid {border_color} !important;
            border-radius: 12px;
        }}

        /* Balon Chat User dan AI */
        [data-testid="stChatMessage"] {{
            border-radius: 12px;
            padding: 0.8rem 1.2rem;
            margin-bottom: 0.8rem;
            background-color: {chat_bg} !important;
            border: 1px solid {chat_border} !important;
        }}
        
        [data-testid="stChatMessage"] div[data-testid="stMarkdownContainer"] p,
        [data-testid="stChatMessage"] div[data-testid="stMarkdownContainer"] span {{
            color: {text_primary} !important;
        }}

        /* Chat Input Field (Kotak ketik terbawah) */
        [data-testid="stChatInput"] {{
            background-color: transparent !important;
        }}
        
        /* Memaksa SEMUA kontainer di dalam stChatInput menjadi gelap */
        [data-testid="stChatInput"] div {{
            background-color: {input_bg} !important;
            border-color: {border_color} !important;
        }}

        [data-testid="stChatInput"] textarea {{
            background-color: {input_bg} !important;
            color: {text_primary} !important;
            caret-color: {accent_color} !important;
        }}
        
        [data-testid="stChatInput"] textarea::placeholder {{
            color: {text_secondary} !important;
            opacity: 0.8 !important;
        }}

        /* Tombol panah kirim (Submit) */
        [data-testid="stChatInput"] button {{
            background-color: transparent !important;
            border: none !important;
        }}
        
        [data-testid="stChatInput"] button svg {{
            fill: {text_primary} !important;
        }}
        
        [data-testid="stChatInput"] button:hover svg {{
            fill: {accent_color} !important;
        }}

        /* ========== RADIO BUTTONS (Tabs) FIX ========== */
        div[data-testid="stHorizontalBlock"] > div:has(> div > div > div[role="radiogroup"]) {{
            background-color: transparent;
            border-bottom: 1px solid {border_color};
            margin-bottom: 1.5rem;
        }}
        div[role="radiogroup"] {{
            display: flex;
            gap: 0.5rem;
            background-color: transparent;
        }}
        div[role="radiogroup"] label {{
            padding: 0.75rem 1.8rem;
            margin-right: 0;
            border-radius: 8px 8px 0 0;
            background-color: transparent !important;
            color: {text_secondary} !important;
            font-weight: 600;
            transition: all 0.2s;
            cursor: pointer;
            border: none;
            border-bottom: 3px solid transparent;
        }}
        div[role="radiogroup"] label p {{
            color: {text_secondary} !important;
        }}
        div[role="radiogroup"] label:hover, 
        div[role="radiogroup"] label:hover p {{
            background-color: {btn_hover_bg} !important;
            color: {text_primary} !important;
        }}
        div[role="radiogroup"] label[data-selected="true"],
        div[role="radiogroup"] label[data-selected="true"] p {{
            background-color: {btn_hover_bg} !important;
            color: {accent_color} !important;
            border-bottom: 3px solid {accent_color} !important;
            font-weight: 700 !important;
        }}
        
        /* ========== MISC ========== */
        .stTextInput {{
            margin-bottom: 0px;
        }}
        
        div[data-testid="stVerticalBlock"] > div.stTextInput > div > label {{
            display: none;
        }}
        
        html {{
            scroll-behavior: smooth;
        }}
        
        .element-container {{
            margin-bottom: 0.75rem;
        }}
        
        .stSpinner > div {{
            border-top-color: {accent_color} !important;
        }}
        
        hr {{
            border-color: {border_color} !important;
            margin: 2rem 0 !important;
        }}
    </style>
    """

_CSS_DARK  = _build_css(dark_mode=True)
_CSS_LIGHT = _build_css(dark_mode=False)

def apply_styles(dark_mode: bool = False) -> None:
    """Apply CSS styles to the Streamlit app."""
    st.markdown(_CSS_DARK if dark_mode else _CSS_LIGHT, unsafe_allow_html=True)