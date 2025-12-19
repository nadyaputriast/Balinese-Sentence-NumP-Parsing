import streamlit as st
import pandas as pd
import os
from dotenv import load_dotenv

# Load Environment Variables
load_dotenv()

# Import Modules
# (HAPUS IMPORT SR DISINI SUPAYA TIDAK ERROR)
from core import cyk_algorithm, create_parse_tree, convert_to_cnf, remove_epsilon_productions, remove_unit_productions
from grammar import RULES_CFG
from ui import app_ui, styles
from utils import stats_manager, batch_processor

# --- FUNGSI MODAL DETAIL (POP-UP) ---
@st.dialog("📝 Detail Analisis Kalimat", width="large")
def show_batch_detail(sentence):
    """
    Menampilkan detail (Tabel & Tree) saat baris batch diklik.
    """
    st.subheader(f'Kalimat: "{sentence}"')
    
    # Analisis ulang kalimat ini secara realtime
    words = sentence.lower().split()
    cfg = remove_unit_productions(remove_epsilon_productions(RULES_CFG))
    cnf = convert_to_cnf(cfg)
    is_valid, table = cyk_algorithm(cnf, words)
    
    # Panggil visualisasi reusable yang sudah kita buat di app_ui
    app_ui.render_analysis_results(words, table, is_valid, cnf, sentence)

def main():
    st.set_page_config(page_title="Balinese Parser", page_icon="🏝️", layout="wide")
    
    # --- 1. INIT STATE ---
    if 'dark_mode' not in st.session_state: st.session_state['dark_mode'] = True
    if 'input_text' not in st.session_state: st.session_state.input_text = ""
    if 'ai_explanation' not in st.session_state: st.session_state.ai_explanation = None
    if 'batch_result_df' not in st.session_state: st.session_state.batch_result_df = None
    if 'batch_view_mode' not in st.session_state: st.session_state.batch_view_mode = "list"
    if 'batch_selected_sentence' not in st.session_state: st.session_state.batch_selected_sentence = None

    # --- 2. SIDEBAR ---
    with st.sidebar:
        st.header("⚙️ Menu")
        st.toggle("🌙 Dark Mode", key="dark_mode")
        st.divider()
        menu = st.radio("Navigasi", ["🏠 Parsing & Visual", "📂 Batch Processing", "📊 Statistik", "📚 Referensi"], key="main_nav")

    # --- 3. APPLY STYLES ---
    styles.apply_styles(st.session_state.dark_mode)

    # --- MAIN PAGE ---
    if menu == "🏠 Parsing & Visual":
        app_ui.render_header(st.session_state.dark_mode)
        
        # HAPUS KOLOM MIC, CUKUP TEXT INPUT SAJA
        text_val = st.text_input("Input Kalimat", key="widget_input", value=st.session_state.input_text, placeholder="cth: tiang numbas buku")
        
        st.write("") # Spacer

        if st.button("🚀 Analisis Struktur", type="primary", use_container_width=True):
            st.session_state.input_text = text_val; st.session_state.ai_explanation = None; st.session_state.run_analysis = True
        
        if st.session_state.get('run_analysis') or (text_val and text_val != st.session_state.get('last_text', '')):
            st.session_state.last_text = text_val
            sentence = st.session_state.input_text.lower()
            if sentence:
                words = sentence.split()
                cfg = remove_unit_productions(remove_epsilon_productions(RULES_CFG))
                cnf = convert_to_cnf(cfg)
                is_valid, table = cyk_algorithm(cnf, words)
                stats_manager.update_stats(is_valid, sentence)

                st.divider()
                app_ui.render_analysis_results(words, table, is_valid, cnf, sentence)
            else: st.session_state.run_analysis = False

    # --- LOGIC BATCH PROCESSING (MASTER-DETAIL) ---
    elif menu == "📂 Batch Processing":
        st.title("📂 Batch File Processing")

        if st.session_state.batch_view_mode == "list":
            st.markdown("Upload CSV untuk validasi massal. Klik baris tabel untuk melihat detail.")
            uploaded = st.file_uploader("Upload CSV (kolom: 'kalimat')", type=["csv"])
            
            if uploaded:
                if st.session_state.batch_result_df is None:
                    try:
                        st.info("👀 Preview Data:")
                        st.dataframe(pd.read_csv(uploaded).head(), use_container_width=True)
                    except: pass
                
                if st.button("🚀 Proses Batch", type="primary", use_container_width=True):
                    with st.spinner("Memproses..."):
                        uploaded.seek(0)
                        df, err = batch_processor.process_csv(uploaded)
                        if err: st.error(err)
                        else: 
                            st.session_state.batch_result_df = df
                            st.rerun()

            if st.session_state.batch_result_df is not None:
                st.divider()
                total = len(st.session_state.batch_result_df)
                valid = len(st.session_state.batch_result_df[st.session_state.batch_result_df['status'] == 'VALID'])
                c1, c2, c3 = st.columns(3)
                c1.metric("Total", total)
                c2.metric("Valid ✅", valid)
                c3.metric("Invalid ❌", total - valid)
                
                st.markdown("#### 📋 Klik Baris untuk Detail (Full Screen)")
                event = st.dataframe(st.session_state.batch_result_df, use_container_width=True, hide_index=True, selection_mode="single-row", on_select="rerun", column_config={"status": st.column_config.TextColumn("Status", width="small")})
                
                if len(event.selection.rows) > 0:
                    idx = event.selection.rows[0]
                    sentence = st.session_state.batch_result_df.iloc[idx]['kalimat']
                    st.session_state.batch_selected_sentence = sentence
                    st.session_state.batch_view_mode = "detail"
                    st.rerun()
                
                if st.button("🔄 Reset"):
                    st.session_state.batch_result_df = None
                    st.rerun()

        elif st.session_state.batch_view_mode == "detail":
            if st.button("← Kembali ke Daftar Batch"):
                st.session_state.batch_view_mode = "list"
                st.rerun()
            st.divider()
            sentence = st.session_state.batch_selected_sentence
            st.markdown(f"## 🔎 Detail Analisis: *\"{sentence}\"*")
            words = sentence.lower().split()
            cfg = remove_unit_productions(remove_epsilon_productions(RULES_CFG))
            cnf = convert_to_cnf(cfg)
            is_valid, table = cyk_algorithm(cnf, words)
            app_ui.render_analysis_results(words, table, is_valid, cnf, sentence)

    elif menu == "📊 Statistik":
        stats_manager.render_stats_dashboard(st.session_state.dark_mode)

    elif menu == "📚 Referensi":
        app_ui.render_grammar_expanders(RULES_CFG, st.session_state.dark_mode)

if __name__ == "__main__":
    main()
