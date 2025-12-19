import streamlit as st
from cfg_grammar import RULES_CFG, PRONOUN_SOR_SINGGIH
from cnf import convert_to_cnf, remove_epsilon_productions, remove_unit_productions
from cyk import cyk_algorithm
from parse_tree import create_parse_tree
from sor_singgih_numeralia import check_numeralia_consistency
import app_ui

# --- Helper Functions (Sama seperti sebelumnya) ---
def extract_proper_nouns(grammar):
    proper_nouns = set()
    for noun_list in grammar.get("PropNoun", []):
        if noun_list and isinstance(noun_list, list):
            proper_nouns.add(noun_list[0])
    return proper_nouns

def format_propnoun(sentence, proper_nouns):
    words = sentence.split()
    formatted_words = []
    for word in words:
        if word in proper_nouns:
            formatted_words.append(word.capitalize())
        else:
            formatted_words.append(word)
    return " ".join(formatted_words)

def main():
    # Setup Page
    st.set_page_config(
        page_title="Parsing Kalimat Bahasa Bali",
        page_icon="🏝️",
        layout="wide",
        initial_sidebar_state="expanded"
    )
    
    # Initialize session state for dark mode
    if 'dark_mode' not in st.session_state:
        st.session_state.dark_mode = False
    
    # --- SIDEBAR NAVIGATION ---
    with st.sidebar:
        # Toggle Dark Mode
        st.markdown("### ⚙️ Pengaturan Tampilan")
        dark_mode_toggle = st.toggle(
            "🌙 Mode Gelap" if not st.session_state.dark_mode else "☀️ Mode Terang",
            value=st.session_state.dark_mode,
            key="dark_mode_toggle"
        )
        
        if dark_mode_toggle != st.session_state.dark_mode:
            st.session_state.dark_mode = dark_mode_toggle
            st.rerun()
        
        st.markdown("---")
        
        # Pilihan Menu
        selected_menu = st.radio(
            "Pilih Halaman:",
            ["🏠 Beranda & Parsing", "📚 Referensi Tata Bahasa", "🎭 Panduan Sor Singgih"],
            index=0
        )
        
        st.markdown("---")
        st.caption("© Putu Nadya Putri Astina")
        st.caption("Teknologi: CYK Algorithm & CFG")
    
    # Apply styles with current dark mode setting
    app_ui.apply_styles(st.session_state.dark_mode)

    # --- MAIN CONTENT AREA ---
    
    # 1. HALAMAN UTAMA (PARSING)
    if selected_menu == "🏠 Beranda & Parsing":
        app_ui.render_header(st.session_state.dark_mode)
        
        # Input Section
        app_ui.render_input_section(st.session_state.dark_mode)
        sentence = st.text_input("", placeholder="Contoh: Tiang numbas buku duang lusin...")
        sentence = sentence.lower()
        
        col1, col2 = st.columns([1, 3])
        with col1:
            check_sor_singgih = st.checkbox("🎭 Cek Sor Singgih", value=True)
        
        if st.button("🔍 Periksa Validitas Kalimat"):
            if sentence:
                words = sentence.strip().split()
                
                with st.spinner("Sedang menganalisis struktur dan semantik..."):
                    # Proses Algoritma
                    cnf = convert_to_cnf(remove_unit_productions(remove_epsilon_productions(RULES_CFG)))
                    is_valid, parse_table = cyk_algorithm(cnf, words)
                    
                    # Tampilkan Hasil Sor Singgih
                    if check_sor_singgih:
                        sor_singgih_analysis = check_numeralia_consistency(words)
                        app_ui.render_sor_singgih_result(words, sor_singgih_analysis, PRONOUN_SOR_SINGGIH, st.session_state.dark_mode)
                    
                    # Tampilkan Tabel CYK
                    app_ui.render_parse_table(words, parse_table, st.session_state.dark_mode)
                    
                    # Hasil Validasi Akhir
                    proper_nouns = extract_proper_nouns(RULES_CFG)
                    formatting_sentence = format_propnoun(sentence.capitalize(), proper_nouns)
                    
                    if is_valid:
                        st.markdown("<div class='parse-tree-container'>", unsafe_allow_html=True)
                        dot = create_parse_tree(words, parse_table, cnf)
                        st.graphviz_chart(dot)
                        st.markdown("</div>", unsafe_allow_html=True)
            else:
                st.warning("Mohon masukkan kalimat terlebih dahulu.")

    # 2. HALAMAN REFERENSI (TATA BAHASA)
    elif selected_menu == "📚 Referensi Tata Bahasa":
        st.title("📚 Referensi Tata Bahasa & Kosakata")
        st.markdown("""
        Halaman ini memuat daftar aturan produksi Context Free Grammar (CFG) dan kosakata 
        yang dikenali oleh sistem ini.
        """)
        # Memanggil fungsi render expander yang sudah ada di app_ui
        app_ui.render_grammar_expanders(RULES_CFG, st.session_state.dark_mode)

    # 3. HALAMAN PANDUAN (SOR SINGGIH)
    elif selected_menu == "🎭 Panduan Sor Singgih":
        st.title("🎭 Panduan Sor Singgih Numeralia")
        
        info_bg = "#0c4a6e" if st.session_state.dark_mode else "#dbeafe"
        info_text = "#e2e8f0" if st.session_state.dark_mode else "#1f2937"
        st.markdown(f"""
        <div style='background-color: {info_bg}; color: {info_text}; padding: 1.5rem; border-radius: 0.5rem; margin-bottom: 2rem; border-left: 4px solid #60a5fa;'>
            <strong>Apa itu Sor Singgih Numeralia?</strong><br>
            Dalam bahasa Bali, angka/bilangan (numeralia) memiliki tingkatan bahasa yang harus 
            disesuaikan dengan lawan bicara dan kata ganti (pronoun) yang digunakan.
        </div>
        """, unsafe_allow_html=True)
        
        # Kita bisa manual render konten panduan di sini atau panggil dari app_ui
        # Contoh konten statis:
        col1, col2, col3 = st.columns(3)
        
        card_bg = "#1e293b" if st.session_state.dark_mode else "#f9fafb"
        text_color = "#e2e8f0" if st.session_state.dark_mode else "#1f2937"
        border_color = "#334155" if st.session_state.dark_mode else "#e5e7eb"
        
        with col1:
            st.markdown(f"""
            <div style='background-color: {card_bg}; padding: 1.5rem; border-radius: 0.5rem; border: 1px solid {border_color}; height: 100%;'>
                <h3 style='color: #f87171;'>🔴 Basa Kasar</h3>
                <p style='color: {text_color};'>Digunakan ke teman sebaya/akrab.</p>
                <code style='background-color: #450a0a; color: #fca5a5; padding: 0.5rem; display: block; border-radius: 0.3rem;'>besik, dua, telu, papat</code>
            </div>
            """, unsafe_allow_html=True)
        with col2:
            st.markdown(f"""
            <div style='background-color: {card_bg}; padding: 1.5rem; border-radius: 0.5rem; border: 1px solid {border_color}; height: 100%;'>
                <h3 style='color: #60a5fa;'>🔵 Basa Alus</h3>
                <p style='color: {text_color};'>Digunakan untuk menghormati orang lain.</p>
                <code style='background-color: #1e3a8a; color: #93c5fd; padding: 0.5rem; display: block; border-radius: 0.3rem;'>asiki, kalih, tiga, sekawan</code>
            </div>
            """, unsafe_allow_html=True)
        with col3:
            st.markdown(f"""
            <div style='background-color: {card_bg}; padding: 1.5rem; border-radius: 0.5rem; border: 1px solid {border_color}; height: 100%;'>
                <h3 style='color: #9ca3af;'>⚪ Netral</h3>
                <p style='color: {text_color};'>Bisa dipakai di semua situasi.</p>
                <code style='background-color: #374151; color: #d1d5db; padding: 0.5rem; display: block; border-radius: 0.3rem;'>lima, pitu, sanga</code>
            </div>
            """, unsafe_allow_html=True)

if __name__ == "__main__":
    main()