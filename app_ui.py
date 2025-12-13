import streamlit as st
import pandas as pd

# --- CSS STYLES ---
def get_custom_css(dark_mode=False):
    # Background colors
    bg_color = "#0f172a" if dark_mode else "#ffffff"
    card_bg = "#1e293b" if dark_mode else "#f9fafb"
    card_bg_alt = "#334155" if dark_mode else "#f3f4f6"
    
    # Text colors
    text_color = "#e2e8f0" if dark_mode else "#1f2937"
    text_secondary = "#94a3b8" if dark_mode else "#6b7280"
    text_muted = "#64748b" if dark_mode else "#9ca3af"
    
    # Border colors
    border_color = "#334155" if dark_mode else "#e5e7eb"
    border_light = "#475569" if dark_mode else "#d1d5db"
    
    # Primary colors
    primary_color = "#60a5fa" if dark_mode else "#1e40af"
    primary_light = "#93c5fd" if dark_mode else "#3b82f6"
    primary_dark = "#3b82f6" if dark_mode else "#1e3a8a"
    
    # Status colors
    success_bg = "#064e3b" if dark_mode else "#d1fae5"
    success_text = "#34d399" if dark_mode else "#065f46"
    success_border = "#059669" if dark_mode else "#10b981"
    
    warning_bg = "#422006" if dark_mode else "#fef3c7"
    warning_text = "#fbbf24" if dark_mode else "#92400e"
    warning_border = "#f59e0b" if dark_mode else "#fbbf24"
    
    error_bg = "#450a0a" if dark_mode else "#fee2e2"
    error_text = "#f87171" if dark_mode else "#991b1b"
    error_border = "#dc2626" if dark_mode else "#f87171"
    
    info_bg = "#0c4a6e" if dark_mode else "#dbeafe"
    info_text = "#60a5fa" if dark_mode else "#1e40af"
    info_border = "#0284c7" if dark_mode else "#60a5fa"
    
    # Register colors (Sor Singgih)
    register_kasar_bg = "#7f1d1d" if dark_mode else "#fee2e2"
    register_kasar_text = "#fca5a5" if dark_mode else "#991b1b"
    
    register_alus_bg = "#1e3a8a" if dark_mode else "#dbeafe"
    register_alus_text = "#93c5fd" if dark_mode else "#1e40af"
    
    register_netral_bg = "#374151" if dark_mode else "#f3f4f6"
    register_netral_text = "#d1d5db" if dark_mode else "#374151"
    
    register_madia_bg = "#713f12" if dark_mode else "#fef3c7"
    register_madia_text = "#fbbf24" if dark_mode else "#92400e"
    
    # Formula/Code colors
    formula_bg = "#422006" if dark_mode else "#fffbeb"
    formula_text = "#fbbf24" if dark_mode else "#d97706"
    formula_border = "#fcd34d" if dark_mode else "#fcd34d"
    
    # Example colors
    example_text = "#34d399" if dark_mode else "#059669"
    example_border = "#10b981" if dark_mode else "#10b981"
    
    # Hover states
    hover_bg = primary_light if dark_mode else "#dbeafe"
    hover_text = "#ffffff" if dark_mode else primary_color
    
    return f"""
    <style>
    /* Reset & Base */
    .stApp {{ 
        background-color: {bg_color} !important; 
        color: {text_color} !important;
    }}
    .main {{ 
        padding: 1rem; 
        background-color: {bg_color};
        color: {text_color};
    }}
    
    /* Text styling */
    p, span, div, li {{
        color: {text_color} !important;
    }}
    
    /* Header Styles */
    .stTitle {{
        color: {primary_color} !important;
        font-size: 5rem !important;
        margin-bottom: 1rem !important;
        text-align: center !important;
    }}
    .main-title {{
        text-align: center;
        color: {primary_color};
        font-size: 2.5rem;
        margin-bottom: 2rem;
    }}
    
    h1, h2, h3, h4, h5, h6 {{
        color: {primary_color} !important;
    }}
    
    /* Button Styles */
    .stButton>button {{
        width: 100%;
        background-color: {primary_color};
        color: white;
        padding: 0.75rem;
        border-radius: 0.5rem;
        border: none;
        font-weight: bold;
        transition: all 0.3s ease;
    }}
    .stButton>button:hover {{ 
        background-color: {primary_dark};
        transform: translateY(-2px);
        box-shadow: 0 4px 12px rgba(0,0,0,0.15);
    }}
    
    /* Input Styles */
    .stTextInput>div>div>input {{
        background-color: {card_bg} !important;
        color: {text_color} !important;
        border: 1px solid {border_color} !important;
        border-radius: 0.5rem;
    }}
    
    .stTextInput>div>div>input:focus {{
        border-color: {primary_color} !important;
        box-shadow: 0 0 0 1px {primary_color} !important;
    }}
    
    /* Checkbox Styles */
    .stCheckbox {{
        color: {text_color} !important;
    }}
    
    .stCheckbox label {{
        color: {text_color} !important;
    }}
    
    /* DataFrame Styles */
    .dataframe {{
        width: 100%;
        font-size: 0.9rem;
        border-collapse: collapse;
        background-color: {card_bg};
        color: {text_color};
    }}
    .dataframe td, .dataframe th {{
        padding: 0.75rem;
        border: 1px solid {border_color};
        text-align: center;
        color: {text_color};
    }}
    .dataframe th {{
        background-color: {card_bg_alt};
        font-weight: bold;
    }}
    .dataframe td:empty {{ border: none; }}
    
    /* Expander Styles */
    .streamlit-expanderHeader {{
        background-color: {card_bg} !important;
        color: {text_color} !important;
        border: 1px solid {border_color} !important;
        border-radius: 0.5rem !important;
    }}
    
    .streamlit-expanderHeader:hover {{
        background-color: {card_bg_alt} !important;
    }}
    
    .streamlit-expanderContent {{
        background-color: {card_bg} !important;
        border: 1px solid {border_color} !important;
        border-top: none !important;
        color: {text_color} !important;
    }}
    
    /* Parse Tree Styles */
    .parse-tree-title {{
        text-align: center;
        color: {primary_color};
        margin-top: 2rem;
        margin-bottom: 1rem;
    }}
    .parse-tree-container {{
        display: flex;
        justify-content: center;
        align-items: center;
        width: 100%;
        background-color: {card_bg};
        padding: 2rem;
        border-radius: 0.5rem;
        border: 1px solid {border_color};
    }}
    
    /* Sor Singgih Labels */
    .register-kasar {{ 
        background-color: {register_kasar_bg}; 
        padding: 0.2rem 0.5rem; 
        border-radius: 0.3rem; 
        color: {register_kasar_text}; 
        font-weight: bold; 
    }}
    .register-alus {{ 
        background-color: {register_alus_bg}; 
        padding: 0.2rem 0.5rem; 
        border-radius: 0.3rem; 
        color: {register_alus_text}; 
        font-weight: bold; 
    }}
    .register-netral {{ 
        background-color: {register_netral_bg}; 
        padding: 0.2rem 0.5rem; 
        border-radius: 0.3rem; 
        color: {register_netral_text}; 
    }}
    .register-madia {{ 
        background-color: {register_madia_bg}; 
        padding: 0.2rem 0.5rem; 
        border-radius: 0.3rem; 
        color: {register_madia_text}; 
    }}
    
    /* Feedback Boxes */
    .sor-singgih-box {{ 
        background-color: {info_bg}; 
        border-left: 4px solid {info_border}; 
        padding: 1rem; 
        margin: 1rem 0; 
        border-radius: 0.5rem;
        color: {text_color};
    }}
    .sor-singgih-box p, .sor-singgih-box strong {{
        color: {text_color} !important;
    }}
    
    .warning-box {{ 
        background-color: {warning_bg}; 
        border-left: 4px solid {warning_border}; 
        padding: 1rem; 
        margin: 1rem 0; 
        border-radius: 0.5rem;
        color: {text_color};
    }}
    .warning-box p, .warning-box strong {{
        color: {text_color} !important;
    }}
    
    .suggestion-box {{ 
        background-color: {success_bg}; 
        border-left: 4px solid {success_border}; 
        padding: 1rem; 
        margin: 1rem 0; 
        border-radius: 0.5rem;
        color: {text_color};
    }}
    .suggestion-box p, .suggestion-box strong {{
        color: {text_color} !important;
    }}
    
    /* --- Vocabulary Chips Styles --- */
    .vocab-container {{
        display: flex;
        flex-wrap: wrap;
        gap: 0.5rem;
        padding: 0.5rem 0;
    }}
    .vocab-chip {{
        background-color: {card_bg_alt};
        border: 1px solid {border_color};
        border-radius: 9999px;
        padding: 0.25rem 0.75rem;
        font-size: 0.85rem;
        color: {text_color};
        transition: all 0.2s;
        cursor: pointer;
    }}
    .vocab-chip:hover {{
        background-color: {hover_bg};
        border-color: {primary_color};
        color: {hover_text};
        transform: translateY(-1px);
    }}
    .vocab-letter-group {{ 
        margin-bottom: 1rem; 
    }}
    .vocab-letter-header {{
        font-weight: bold;
        color: {primary_color};
        border-bottom: 2px solid {border_color};
        margin-bottom: 0.5rem;
        padding-bottom: 0.2rem;
        font-size: 1rem;
    }}

    /* --- Grammar Visual Styles --- */
    .grammar-box {{
        background-color: {card_bg};
        border: 1px solid {border_color};
        border-radius: 8px;
        padding: 1.5rem;
        margin-bottom: 1rem;
        box-shadow: 0 1px 3px rgba(0,0,0,0.1);
    }}
    .grammar-box p {{
        color: {text_secondary} !important;
    }}
    .grammar-title {{
        color: {primary_color};
        font-weight: bold;
        font-size: 1.1rem;
        margin-bottom: 0.75rem;
        border-bottom: 2px solid {border_color};
        padding-bottom: 0.25rem;
        display: inline-block;
    }}
    .rule-row {{
        display: flex;
        flex-direction: row;
        align-items: center;
        margin-bottom: 0.75rem;
        padding: 0.75rem;
        background-color: {card_bg_alt};
        border-radius: 6px;
        border: 1px solid {border_color};
    }}
    .rule-formula {{
        font-family: 'Courier New', monospace;
        font-weight: bold;
        color: {formula_text};
        background-color: {formula_bg};
        padding: 4px 10px;
        border-radius: 4px;
        border: 1px solid {formula_border};
        margin-right: 1rem;
        min-width: 140px; 
        text-align: center;
        flex-shrink: 0;
    }}
    .rule-desc {{ 
        color: {text_color}; 
        flex-grow: 1; 
        font-size: 0.95rem; 
        font-weight: 500;
    }}
    .rule-example {{
        font-style: italic;
        color: {example_text};
        font-size: 0.9rem;
        border-left: 3px solid {example_border};
        padding-left: 0.75rem;
        margin-left: 1rem;
        min-width: 200px;
        flex-shrink: 0;
    }}
    .arrow-down {{
        text-align: center;
        font-size: 1.5rem;
        color: {text_muted};
        margin: -5px 0 15px 0;
        font-weight: bold;
    }}
    
    /* Sidebar Styles */
    [data-testid="stSidebar"] {{
        background-color: {card_bg} !important;
    }}
    
    [data-testid="stSidebar"] * {{
        color: {text_color} !important;
    }}
    
    /* Radio button styles */
    .stRadio label {{
        color: {text_color} !important;
    }}
    
    /* Caption styles */
    .stCaption {{
        color: {text_secondary} !important;
    }}
    
    /* Info/Warning/Error boxes from streamlit */
    .stAlert {{
        background-color: {card_bg} !important;
        color: {text_color} !important;
        border-color: {border_color} !important;
    }}
    
    /* Form Styles */
    .stForm {{
        background-color: {card_bg} !important;
        border: 1px solid {border_color} !important;
        border-radius: 0.5rem;
        padding: 1rem;
    }}
    
    .stTextArea textarea {{
        background-color: {card_bg} !important;
        color: {text_color} !important;
        border: 1px solid {border_color} !important;
        border-radius: 0.5rem;
    }}
    
    .stTextArea textarea:focus {{
        border-color: {primary_color} !important;
        box-shadow: 0 0 0 1px {primary_color} !important;
    }}
    
    .stSelectbox {{
        color: {text_color} !important;
    }}
    
    .stSelectbox > div > div {{
        background-color: {card_bg} !important;
        color: {text_color} !important;
        border: 1px solid {border_color} !important;
    }}
    
    /* Code tag in text */
    code {{
        background-color: {card_bg_alt} !important;
        color: {primary_color} !important;
        padding: 0.2rem 0.4rem;
        border-radius: 0.3rem;
        font-family: 'Courier New', monospace;
    }}
    
    /* Small text */
    small {{
        color: {text_secondary} !important;
    }}
    
    @media (max-width: 768px) {{
        .rule-row {{ 
            flex-direction: column; 
            align-items: flex-start; 
        }}
        .rule-formula {{ 
            margin-bottom: 0.5rem; 
            width: 100%; 
        }}
        .rule-example {{ 
            margin-left: 0; 
            margin-top: 0.5rem; 
            border-left: none; 
            border-top: 2px solid {example_border}; 
            padding-top: 0.25rem; 
            padding-left: 0; 
            width: 100%;
        }}
    }}
    </style>
"""

def apply_styles(dark_mode=False):
    st.markdown(get_custom_css(dark_mode), unsafe_allow_html=True)

def render_header(dark_mode=False):
    text_color = "#94a3b8" if dark_mode else "#4B5563"
    subtitle_color = "#64748b" if dark_mode else "#6b7280"
    st.markdown(f"""
        <h1 class="main-title">Parsing Kalimat Bahasa Bali Berpredikat Frasa Numeralia</h1>
        <h3 style='font-size: 2rem; color: {subtitle_color}; text-align: center'>Dibuat oleh Kelompok 5 Kelas D</h3>
        <p style='font-size: 1.1rem; color: {text_color}; margin-bottom: 2rem; text-align: justify;'>
        Website ini dapat digunakan untuk memvalidasi apakah suatu kalimat dengan predikat frasa numeralia valid 
        atau tidak. Frasa numeralia merupakan kelompok kata yang menunjukkan bilangan atau jumlah tertentu.
        </p>
    """, unsafe_allow_html=True)

def render_grammar_expanders(rules_cfg, dark_mode=False):
    primary_color = "#60a5fa" if dark_mode else "#1e40af"
    text_color = "#94a3b8" if dark_mode else "#6b7280"
    
    # --- BAGIAN 1: PANDUAN TATA BAHASA (Visual Storytelling) ---
    with st.expander("📚 Panduan Struktur Tata Bahasa (Grammar Guide)", expanded=False):
        
        # 1. STRUKTUR UTAMA KALIMAT
        # PERHATIKAN: Semua tag HTML di bawah ini RATA KIRI (tanpa spasi di depan)
        st.markdown(f"""
<div class='grammar-box'>
<div class='grammar-title'>1. Struktur Inti Kalimat (K)</div>
<p style='color:{text_color}; margin-bottom:1rem;'>Sebuah kalimat dalam bahasa Bali yang valid harus memiliki struktur dasar minimal:</p>
<div class='rule-row'>
<div class='rule-formula'>S + P</div>
<div class='rule-desc'>Subjek diikuti oleh Predikat</div>
<div class='rule-example'>Contoh: "Tiang (S) numbas (P)"</div>
</div>
<div class='rule-row'>
<div class='rule-formula'>S + P + Pel</div>
<div class='rule-desc'>Subjek + Predikat + Pelengkap</div>
<div class='rule-example'>Contoh: "Tiang (S) numbas (P) buku (Pel)"</div>
</div>
<div class='rule-row'>
<div class='rule-formula'>S + P + Ket</div>
<div class='rule-desc'>Subjek + Predikat + Keterangan</div>
<div class='rule-example'>Contoh: "Ipun (S) luas (P) ke pasar (Ket)"</div>
</div>
</div>
<div class='arrow-down'>⬇️</div>
""", unsafe_allow_html=True)

        # 2. STRUKTUR FRASA NUMERALIA (Fokus Aplikasi)
        st.markdown(f"""
<div class='grammar-box' style='border-left: 5px solid {primary_color};'>
<div class='grammar-title'>2. Pembentukan Predikat Frasa Numeralia (NumP)</div>
<p style='color:{text_color}; margin-bottom:1rem;'>
Karena aplikasi ini berfokus pada <b>Numeralia</b>, berikut adalah cara membentuk Frasa Bilangan yang valid:
</p>
<div class='rule-row'>
<div class='rule-formula'>Num</div>
<div class='rule-desc'>Hanya Kata Bilangan saja</div>
<div class='rule-example'>Contoh: "... telu"</div>
</div>
<div class='rule-row'>
<div class='rule-formula'>Num + Noun</div>
<div class='rule-desc'>Kata Bilangan diikuti Kata Benda</div>
<div class='rule-example'>Contoh: "... duang tali"</div>
</div>
<div class='rule-row'>
<div class='rule-formula'>NumP + Det</div>
<div class='rule-desc'>Frasa Bilangan + Kata Penunjuk</div>
<div class='rule-example'>Contoh: "... duang tali punika"</div>
</div>
<div class='rule-row'>
<div class='rule-formula'>NumP + NumP</div>
<div class='rule-desc'>Gabungan dua Frasa Bilangan</div>
<div class='rule-example'>Contoh: "... duang tali limang rupiah"</div>
</div>
</div>
<div class='arrow-down'>⬇️</div>
""", unsafe_allow_html=True)

        # 3. KOMPONEN PENDUKUNG
        st.markdown(f"""
<div class='grammar-box'>
<div class='grammar-title'>3. Komponen Pendukung Lainnya</div>
<p style='color:{text_color}; margin-bottom:1rem;'>Komponen lain yang membentuk Subjek atau Keterangan:</p>
<div class='rule-row'>
<div class='rule-formula'>NP (Nomina)</div>
<div class='rule-desc'>Frasa Benda. Nama Orang, Kata Ganti, atau Kata Benda + Penunjuk.</div>
<div class='rule-example'>Contoh: "Tiang", "Buku punika"</div>
</div>
<div class='rule-row'>
<div class='rule-formula'>PP (Preposisi)</div>
<div class='rule-desc'>Frasa Depan. Diawali kata depan (di, ke, uli).</div>
<div class='rule-example'>Contoh: "di pasar", "ka sekolah"</div>
</div>
</div>
""", unsafe_allow_html=True)

    # --- BAGIAN 2: VOCABULARY (Dropdown & Chips) ---
    vocab_mapping = {
        "Num": "🔢 Kata Bilangan (Numeralia)",
        "Noun": "📦 Kata Benda (Noun)",
        "V": "🏃 Kata Kerja (Verb)",
        "Adj": "✨ Kata Sifat (Adjective)",
        "PropNoun": "🏷️ Kata Benda Nama Diri (Proper Noun)",
        "Pronoun": "👤 Kata Ganti (Pronoun)",
        "Prep": "🔗 Kata Depan (Preposition)",
        "Adv": "⏳ Kata Keterangan (Adverb)",
        "Det": "👉 Kata Penunjuk (Determiner)"
    }

    def group_words_by_letter(word_list):
        grouped = {}
        for word in sorted(word_list):
            first_letter = word[0].upper()
            if first_letter not in grouped:
                grouped[first_letter] = []
            grouped[first_letter].append(word)
        return grouped

    with st.expander("📖 Lihat Vocabulary Bahasa Bali", expanded=False):
        st.markdown(f"""
            <h3 style='color: {primary_color}; margin-bottom: 1rem;'>Kamus Kata</h3>
            <p style='color: {text_color}; margin-bottom: 1.5rem;'>Klik pada kategori di bawah untuk melihat daftar kata yang tersedia.</p>
        """, unsafe_allow_html=True)
        
        # --- FITUR SEARCH ---
        st.markdown(f"<h4 style='color: {primary_color}; margin-top: 1rem;'>🔍 Cari Kata</h4>", unsafe_allow_html=True)
        
        search_col1, search_col2 = st.columns([3, 1])
        with search_col1:
            search_word = st.text_input(
                "Masukkan kata yang ingin dicari:",
                placeholder="Contoh: tiang, numbas, buku...",
                key="vocab_search",
                label_visibility="collapsed"
            )
        with search_col2:
            search_button = st.button("🔍 Cari", key="search_vocab_btn", use_container_width=True)
        
        if search_button and search_word:
            search_word_lower = search_word.lower().strip()
            found = False
            found_in = []
            
            # Cari di semua kategori
            for key, label in vocab_mapping.items():
                raw_words = [item[0] for item in rules_cfg.get(key, [])]
                if search_word_lower in raw_words:
                    found = True
                    found_in.append(label)
            
            if found:
                success_bg = "#064e3b" if dark_mode else "#d1fae5"
                success_text = "#34d399" if dark_mode else "#065f46"
                categories = ", ".join(found_in)
                st.markdown(f"""
                    <div style='background-color: {success_bg}; color: {success_text}; padding: 1rem; 
                                border-radius: 0.5rem; margin: 1rem 0; border-left: 4px solid {success_text};'>
                        ✅ Kata <strong>"{search_word_lower}"</strong> ditemukan!<br>
                        <small>Kategori: {categories}</small>
                    </div>
                """, unsafe_allow_html=True)
            else:
                error_bg = "#450a0a" if dark_mode else "#fee2e2"
                error_text = "#f87171" if dark_mode else "#991b1b"
                st.markdown(f"""
                    <div style='background-color: {error_bg}; color: {error_text}; padding: 1rem; 
                                border-radius: 0.5rem; margin: 1rem 0; border-left: 4px solid {error_text};'>
                        ❌ Kata <strong>"{search_word_lower}"</strong> tidak ditemukan dalam database.
                    </div>
                """, unsafe_allow_html=True)
                
                # Form untuk menambah kata baru
                st.markdown(f"<h4 style='color: {primary_color}; margin-top: 1.5rem;'>➕ Tambah Kata Baru</h4>", unsafe_allow_html=True)
                
                with st.form(key="add_word_form"):
                    st.text_input("Kata:", value=search_word_lower, disabled=True, key="new_word_display")
                    
                    word_type = st.selectbox(
                        "Jenis Kata:",
                        options=list(vocab_mapping.keys()),
                        format_func=lambda x: vocab_mapping[x],
                        key="word_type_select"
                    )
                    
                    word_notes = st.text_area(
                        "Catatan (opsional):",
                        placeholder="Contoh: arti, konteks penggunaan, dll.",
                        key="word_notes"
                    )
                    
                    submit_button = st.form_submit_button("💾 Simpan Kata")
                    
                    if submit_button:
                        warning_bg = "#422006" if dark_mode else "#fef3c7"
                        warning_text = "#fbbf24" if dark_mode else "#92400e"
                        st.markdown(f"""
                            <div style='background-color: {warning_bg}; color: {warning_text}; padding: 1rem; 
                                        border-radius: 0.5rem; margin: 1rem 0; border-left: 4px solid {warning_text};'>
                                ⚠️ <strong>Fitur dalam pengembangan!</strong><br>
                                Data yang ingin ditambahkan:<br>
                                • Kata: <strong>{search_word_lower}</strong><br>
                                • Jenis: <strong>{vocab_mapping[word_type]}</strong><br>
                                • Catatan: {word_notes if word_notes else "-"}<br><br>
                                <small>Untuk saat ini, silakan tambahkan kata ke file <code>cfg_grammar.py</code> secara manual.</small>
                            </div>
                        """, unsafe_allow_html=True)
        
        st.markdown("---")
        
        # --- DAFTAR VOCABULARY PER KATEGORI ---
        st.markdown(f"<h4 style='color: {primary_color}; margin-top: 1.5rem;'>📚 Daftar Lengkap</h4>", unsafe_allow_html=True)
        
        for key, label in vocab_mapping.items():
            # Mengambil kata pertama dari setiap list [kata]
            raw_words = [item[0] for item in rules_cfg.get(key, [])]
            if raw_words:
                with st.expander(f"{label} ({len(raw_words)} kata)"):
                    grouped_words = group_words_by_letter(raw_words)
                    for letter, words in grouped_words.items():
                        chips_html = "".join([f'<span class="vocab-chip">{w}</span>' for w in words])
                        st.markdown(f"""
                            <div class="vocab-letter-group">
                                <div class="vocab-letter-header">{letter}</div>
                                <div class="vocab-container">{chips_html}</div>
                            </div>
                        """, unsafe_allow_html=True)

def render_input_section(dark_mode=False):
    primary_color = "#60a5fa" if dark_mode else "#1e40af"
    warning_bg = "#422006" if dark_mode else "#fef3c7"
    warning_text = "#fbbf24" if dark_mode else "#92400e"
    st.markdown(f"""
        <h2 style='color: {primary_color}; margin-top: 2rem; margin-bottom: 1rem;'>Input Kalimat</h2>
        <div style='background-color: {warning_bg}; color: {warning_text}; padding: 1rem; border-radius: 0.5rem; margin-bottom: 1rem; border-left: 4px solid {warning_text};'>
            ⚠️ Pastikan kalimat tidak mengandung typo dan tanpa tanda baca (kecuali tanda hubung).
        </div>
    """, unsafe_allow_html=True)

# Helper function untuk tabel CYK (Format Cell)
def format_cell_content(cell_set):
    if not cell_set:
        return "∅"
    return "{" + ", ".join(sorted(cell_set)) + "}"

def render_sor_singgih_result(words, sor_singgih_analysis, pronoun_dict, dark_mode=False):
    primary_color = "#60a5fa" if dark_mode else "#1e40af"
    st.markdown(f"<h2 style='color: {primary_color}; margin-top: 2rem; margin-bottom: 1rem; text-align: center;'>🎭 Analisis Sor Singgih Numeralia</h2>", unsafe_allow_html=True)
    
    if not (sor_singgih_analysis['numeralia_found'] or sor_singgih_analysis['pronoun_found']):
        st.info("ℹ️ Tidak ada numeralia yang terdeteksi dalam kalimat ini.")
        return

    # Color coding logic
    colored_words = []
    for i, word in enumerate(words):
        word_lower = word.lower()
        num_info = next((n for n in sor_singgih_analysis['numeralia_found'] if n['position'] == i), None)
        
        if num_info:
            reg = num_info['register']
            cls = "register-kasar" if reg == 'kasar' else "register-alus" if reg == 'alus' else "register-netral"
            colored_words.append(f'<span class="{cls}">{word}</span>')
        elif word_lower in pronoun_dict:
            reg = pronoun_dict[word_lower]['register']
            cls = "register-kasar" if reg == 'kasar' else "register-alus" if reg == 'alus' else "register-madia" if reg == 'madia' else ""
            colored_words.append(f'<span class="{cls}">{word}</span>' if cls else word)
        else:
            colored_words.append(word)

    text_color = "#e2e8f0" if dark_mode else "#1f2937"
    secondary_color = "#94a3b8" if dark_mode else "#6b7280"
    
    st.markdown(f"""
        <div class='sor-singgih-box'>
            <p style='margin-bottom: 0.5rem; color: {text_color};'><strong>Kalimat dengan Color Coding:</strong></p>
            <p style='font-size: 1.1rem; color: {text_color};'>{' '.join(colored_words)}</p>
            <p style='font-size: 0.85rem; margin-top: 0.5rem; color: {secondary_color};'>
                <span class="register-kasar">Kasar</span> <span class="register-alus">Alus</span> 
                <span class="register-madia">Madia</span> <span class="register-netral">Netral</span>
            </p>
        </div>
    """, unsafe_allow_html=True)

    # Table of found numeralia
    if sor_singgih_analysis['numeralia_found']:
        st.markdown(f"<p style='color: {text_color};'><strong>Numeralia yang ditemukan:</strong></p>", unsafe_allow_html=True)
        num_data = []
        for num in sor_singgih_analysis['numeralia_found']:
            alternatives = []
            if 'alus' in num['data']: alternatives.append(f"Alus: {num['data']['alus']}")
            if 'kasar' in num['data']: alternatives.append(f"Kasar: {num['data']['kasar']}")
            
            num_data.append({
                'Kata': num['word'], 'Register': num['register'].upper(),
                'Arti': num['data'].get('meaning', '-'),
                'Alternatif': ', '.join(alternatives) if alternatives else '-'
            })
        st.dataframe(pd.DataFrame(num_data), use_container_width=True, hide_index=True)

    # Consistency checks
    if sor_singgih_analysis['is_consistent']:
        st.markdown(f"""<div class='suggestion-box'><p style='color: {text_color};'>✅ <strong>Konsistensi Sor Singgih: BAIK</strong><br>Penggunaan register sudah konsisten.</p></div>""", unsafe_allow_html=True)
    else:
        for inc in sor_singgih_analysis['inconsistencies']:
            color = {'high': '#f87171', 'medium': '#fbbf24', 'low': '#34d399'}.get(inc["severity"], text_color)
            st.markdown(f"""<div class='warning-box'><p style='color: {text_color};'>⚠️ <strong style='color: {color};'>{inc['message']}</strong></p></div>""", unsafe_allow_html=True)
        
        # Suggestions
        if sor_singgih_analysis['suggestions']:
            st.markdown(f"<p style='color: {text_color};'><strong>💡 Saran Perbaikan:</strong></p>", unsafe_allow_html=True)
            for sugg in sor_singgih_analysis['suggestions']:
                st.markdown(f"<p style='color: {text_color};'>• {sugg}</p>", unsafe_allow_html=True)
            
            from sor_singgih_numeralia import format_suggestion 
            alt_sentences = format_suggestion(words, sor_singgih_analysis)
            if alt_sentences:
                st.markdown(f"<p style='color: {text_color};'><strong>✨ Contoh Kalimat yang Konsisten:</strong></p>", unsafe_allow_html=True)
                for alt in alt_sentences:
                    st.markdown(f"""<div class='suggestion-box'><p style='color: {text_color};'><strong>{alt['version']}:</strong><br>"{alt['sentence'].capitalize()}."</p></div>""", unsafe_allow_html=True)

def render_parse_table(words, parse_table, dark_mode=False):
    primary_color = "#60a5fa" if dark_mode else "#1e40af"
    st.markdown(f"<h2 style='color: {primary_color}; margin-top: 2rem; margin-bottom: 1rem; text-align: center;'>Tabel Filling (CYK Algorithm)</h2>", unsafe_allow_html=True)
    n = len(words)
    display_table = [[""] * n for _ in range(n + 1)]
    display_table[n] = words.copy()
    
    for i in range(n):
        for j in range(n - i):
            display_table[n-1-i][j] = format_cell_content(parse_table[j][j + i])
    
    df = pd.DataFrame(display_table)
    st.write(df.to_html(index=False, header=False, classes='dataframe'), unsafe_allow_html=True)

def render_validation_result(is_valid, formatted_sentence, dark_mode=False):
    if is_valid:
        valid_bg = "#064e3b" if dark_mode else "#d1fae5"
        valid_text = "#34d399" if dark_mode else "#065f46"
        st.markdown(f"""
            <div style='background-color: {valid_bg}; color: {valid_text}; padding: 1rem; border-radius: 0.5rem; margin: 2rem 0; text-align: center; border: 2px solid {valid_text};'>
                ✅ Kalimat <strong>"{formatted_sentence}."</strong> VALID menurut tata bahasa Bali
            </div>
        """, unsafe_allow_html=True)
        st.markdown("<h2 class='parse-tree-title'>Pohon Parsing</h2>", unsafe_allow_html=True)
    else:
        invalid_bg = "#450a0a" if dark_mode else "#fee2e2"
        invalid_text = "#f87171" if dark_mode else "#991b1b"
        st.markdown(f"""
            <div style='background-color: {invalid_bg}; color: {invalid_text}; padding: 1rem; border-radius: 0.5rem; margin: 2rem 0; text-align: center; border: 2px solid {invalid_text};'>
                ❌ Kalimat <strong>"{formatted_sentence}."</strong> TIDAK VALID menurut tata bahasa Bali
            </div>
        """, unsafe_allow_html=True)