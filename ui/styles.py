import streamlit as st

def apply_styles(dark_mode=False):
    # --- PALETTE DEFINITION ---
    if dark_mode:
        # Dark Mode
        bg_color = "#020617"        # Background Utama (Sangat Gelap)
        sidebar_bg = "#0f172a"      # Background Sidebar
        card_bg = "#1e293b"         # Background Card
        text_primary = "#ffffff"    # Teks Putih
        text_secondary = "#94a3b8"  # Teks Abu-abu
        border_color = "#334155"    # Border
        accent_color = "#38bdf8"    # Biru Terang
        chip_bg = "#334155"         # Background Chip Statis
        btn_hover_bg = "rgba(56, 189, 248, 0.15)"
        
        input_bg = "#1e293b"        # Input field background
        
    else:
        # Light Mode
        bg_color = "#f8fafc"        # Putih Abu-abu (Main BG)
        sidebar_bg = "#ffffff"      # Putih Bersih (Sidebar)
        card_bg = "#ffffff"
        text_primary = "#0f172a"    # Hitam/Biru Gelap
        text_secondary = "#64748b"
        border_color = "#e2e8f0"
        accent_color = "#0284c7"    # Biru Tua
        chip_bg = "#f1f5f9"         # Very Light Gray
        btn_hover_bg = "rgba(2, 132, 199, 0.1)"
        
        input_bg = "#ffffff"

    css = f"""
    <style>
        @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&family=JetBrains+Mono:wght@400;500&display=swap');
        
        /* --- MAIN APP --- */
        .stApp {{
            background-color: {bg_color};
            color: {text_primary} !important;
            font-family: 'Inter', sans-serif;
            transition: background-color 0.3s ease;
        }}
        
        /* --- SIDEBAR STYLING --- */
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

        /* --- INPUT FIELD --- */
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

        /* --- BUTTONS (Interactive in Rules) --- */
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
        
        /* Primary Buttons */
        button[kind="primary"], div[class*="mic-btn"] button {{
            background-color: {accent_color} !important;
            color: #ffffff !important;
            border: none !important;
            font-weight: 600 !important;
        }}

        /* --- CHIPS & TEXT (Rules) --- */
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
        
        /* --- CARDS & TABLE --- */
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
        
        /* --- VOCABULARY GRID (FIXED CURLY BRACES) --- */
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
        
        /* Letter Header */
        .letter-header {{
            font-size: 1.2rem;
            font-weight: 700;
            color: {accent_color};
            margin-top: 1.5rem;
            margin-bottom: 0.5rem;
            border-bottom: 1px solid {border_color};
            padding-bottom: 0.2rem;
        }}

        /* Expanders Fix */
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
        
        /* Fix Input Label */
        .stTextInput {{ margin-bottom: 0px; }}
        div[data-testid="stVerticalBlock"] > div.stTextInput > div > label {{ display: none; }}
    </style>
    """
    st.markdown(css, unsafe_allow_html=True)