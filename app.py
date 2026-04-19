import streamlit as st
import pandas as pd
import os
from dotenv import load_dotenv
import unicodedata
import json

# Load Environment Variables
load_dotenv()

from core import cyk_algorithm, convert_to_cnf, remove_epsilon_productions, remove_unit_productions
from grammar import RULES_CFG
from ui import app_ui, styles
from utils import stats_manager, batch_processor

@st.cache_resource
def prepare_grammars():
    cfg_no_eps = remove_epsilon_productions(RULES_CFG)
    cfg_strict = remove_unit_productions(cfg_no_eps)
    cnf_strict = convert_to_cnf(cfg_strict)
    cnf_viz = cfg_no_eps
    return cnf_strict, cnf_viz

def run_cyk_cached(sentence: str):
    cache_key = f"cyk__{sentence}"
    if cache_key not in st.session_state:
        cnf_strict, cnf_viz = prepare_grammars()
        words = sentence.split()
        is_valid, table, _ = cyk_algorithm(cnf_strict, words)
        _, _, backpointers_viz = cyk_algorithm(cnf_viz, words)
        st.session_state[cache_key] = {
            "words": words,
            "is_valid": is_valid,
            "table": table,
            "backpointers_viz": backpointers_viz,
        }
    return st.session_state[cache_key]

@st.cache_data
def load_balinese_corpus():
    file_path = "scraping/balinese_lexicon.json"
    
    if not os.path.exists(file_path):
        st.error(f"⚠️ File corpus tidak ditemukan di: {file_path}")
        return set() 
        
    with open(file_path, "r", encoding="utf-8") as f:
        data = json.load(f)
        kata_dasar_set = set()
        
        for kategori, isi_kategori in data.items():
            if isinstance(isi_kategori, dict):
                for kata in isi_kategori.keys():
                    kata_dasar_set.add(kata.lower().strip())
                    
        return kata_dasar_set
    
def stem_kata_bali(kata, kamus_dasar):
    """
    Menganalisis 1 kata dan mencoba mengupas imbuhan bahasa Bali 
    (Akhiran, Awalan, Gabungan, dan Nasalisasi) untuk mencari kata dasarnya.
    """
    kata_pengecualian = ["petang", "patang", "telung", "limang"]
    if kata in kata_pengecualian or kata in kamus_dasar:
        return kata, None

    suffixes = ["ang", "ne", "in", "an", "a", "e"]
    prefixes = ["ma", "ka", "pa", "sa", "di", "a"]
    
    for suf in suffixes:
        if kata.endswith(suf):
            k_dasar = kata[:-len(suf)]
            if k_dasar in kamus_dasar:
                return k_dasar, f"**{kata}** ➡️ {k_dasar} (Hapus akhiran -{suf})"

    for pref in prefixes:
        if kata.startswith(pref):
            k_dasar = kata[len(pref):]
            if k_dasar in kamus_dasar:
                return k_dasar, f"**{kata}** ➡️ {k_dasar} (Hapus awalan {pref}-)"

    for pref in prefixes:
        for suf in suffixes:
            if kata.startswith(pref) and kata.endswith(suf):
                k_dasar = kata[len(pref):-len(suf)]
                if k_dasar in kamus_dasar:
                    return k_dasar, f"**{kata}** ➡️ {k_dasar} (Hapus {pref}- dan -{suf})"

    if kata.startswith("ng"):
        k_dasar = kata[2:] # Hapus 'ng'
        if k_dasar in kamus_dasar:
            return k_dasar, f"**{kata}** ➡️ {k_dasar} (Nasalisasi ng-)"
            
    if kata.startswith("ny"):
        for huruf_asli in ['j', 'c', 's']:
            k_dasar = huruf_asli + kata[2:]
            if k_dasar in kamus_dasar:
                return k_dasar, f"**{kata}** ➡️ {k_dasar} (Nasalisasi ny- menjadi {huruf_asli}-)"
                
    if kata.startswith("m") and len(kata) > 2:
        for huruf_asli in ['b', 'p']:
            k_dasar = huruf_asli + kata[1:]
            if k_dasar in kamus_dasar:
                return k_dasar, f"**{kata}** ➡️ {k_dasar} (Nasalisasi m- menjadi {huruf_asli}-)"
                
    if kata.startswith("n") and not kata.startswith("ny") and not kata.startswith("ng"):
        for huruf_asli in ['t', 'd']:
            k_dasar = huruf_asli + kata[1:]
            if k_dasar in kamus_dasar:
                return k_dasar, f"**{kata}** ➡️ {k_dasar} (Nasalisasi n- menjadi {huruf_asli}-)"

    return kata, None

def bersihkan_dan_stem_bali(kalimat, kamus_dasar):
    kalimat = kalimat.replace(".", "").replace(",", "")
    kata_kata = kalimat.split()
    
    hasil_bersih = []
    log_perubahan = []
    
    for kata in kata_kata:
        kata_dasar, catatan = stem_kata_bali(kata, kamus_dasar)
        hasil_bersih.append(kata_dasar)
        if catatan:
            log_perubahan.append(catatan)
            
    return " ".join(hasil_bersih), log_perubahan

KATA_DASAR_CORPUS = load_balinese_corpus()

@st.dialog("📝 Detail Analisis Kalimat", width="large")
def show_batch_detail(sentence):
    st.subheader(f'Kalimat: "{sentence}"')
    _, cnf_viz = prepare_grammars()
    result = run_cyk_cached(sentence)
    app_ui.render_analysis_results(
        result["words"], result["table"], result["is_valid"],
        cnf_viz, sentence, result["backpointers_viz"]
    )

def main():
    st.set_page_config(page_title="Balinese Parser", page_icon="🏝️", layout="wide")

    defaults = {
        "dark_mode": True,
        "widget_input": "",
        "batch_result_df": None,
        "batch_view_mode": "list",
        "batch_selected_sentence": None,
        "run_analysis": False,
        "last_text": "",
    }
    for k, v in defaults.items():
        if k not in st.session_state:
            st.session_state[k] = v

    if "lexicon_data" not in st.session_state:
        st.session_state["lexicon_data"] = app_ui.load_lexicon_data()

    with st.sidebar:
        st.header("⚙️ Menu")
        st.toggle("🌙 Dark Mode", key="dark_mode")
        st.divider()
        menu = st.radio(
            "Navigasi",
            ["🏠 Parsing & Visual", "📂 Batch Processing", "📊 Statistik", "📚 Referensi"],
            key="main_nav"
        )

    styles.apply_styles(st.session_state.dark_mode)
    _, cnf_viz = prepare_grammars()

    if menu == "🏠 Parsing & Visual":
        app_ui.render_header(st.session_state.dark_mode)
        text_val = st.text_input(
            "Input Kalimat", 
            key="widget_input",
            placeholder="cth: tiang numbas buku"
        )
        st.write("")

        st.button("🚀 Analisis Struktur", type="primary", use_container_width=True)

        if text_val:
            sentence_raw = text_val.lower().strip()
            
            sentence_normalized = unicodedata.normalize('NFKD', sentence_raw).encode('ASCII', 'ignore').decode('utf-8')
            
            sentence_final, log_perubahan = bersihkan_dan_stem_bali(sentence_normalized, KATA_DASAR_CORPUS)
            
            result = run_cyk_cached(sentence_final)
            
            if sentence_final != st.session_state.get("last_text", ""):
                stats_manager.update_stats(result["is_valid"], sentence_final)
                st.session_state.last_text = sentence_final
                
            st.divider()
            
            if log_perubahan:
                st.info(
                    "💡 **Catatan Morfologi:** Sistem menyesuaikan beberapa kata ke bentuk dasarnya (Lexicon) untuk analisis:\n\n" + 
                    "\n".join([f"- {perubahan}" for perubahan in log_perubahan])
                )
            
            app_ui.render_analysis_results(
                result["words"], result["table"], result["is_valid"],
                cnf_viz, sentence_final, result["backpointers_viz"]
            )

    elif menu == "📂 Batch Processing":
        st.title("📂 Batch File Processing")

        if st.session_state.batch_view_mode == "list":
            st.markdown("Upload CSV untuk validasi massal. Klik baris tabel untuk melihat detail.")
            uploaded = st.file_uploader("Upload File (kolom wajib: 'kalimat')", type=["csv", "xlsx", "xls"])

            if uploaded:
                if st.session_state.batch_result_df is None:
                    try:
                        st.info("👀 Preview Data:")
                        if uploaded.name.endswith(('.xlsx', '.xls')):
                            st.dataframe(pd.read_excel(uploaded).head(), use_container_width=True)
                        else:
                            st.dataframe(pd.read_csv(uploaded).head(), use_container_width=True)
                    except Exception:
                        pass

                if st.button("🚀 Proses Batch", type="primary", use_container_width=True):
                    with st.spinner("Memproses..."):
                        uploaded.seek(0)
                        df, err = batch_processor.process_file(uploaded, KATA_DASAR_CORPUS, bersihkan_dan_stem_bali)
                        if err:
                            st.error(err)
                        else:
                            st.session_state.batch_result_df = df
                            st.rerun()

            if st.session_state.batch_result_df is not None:
                st.divider()
                total = len(st.session_state.batch_result_df)
                valid = len(st.session_state.batch_result_df[
                    st.session_state.batch_result_df["status"] == "VALID"
                ])
                c1, c2, c3 = st.columns(3)
                c1.metric("Total", total)
                c2.metric("Valid ✅", valid)
                c3.metric("Invalid ❌", total - valid)

                st.markdown("#### 📋 Klik Baris untuk Detail (Full Screen)")
                event = st.dataframe(
                    st.session_state.batch_result_df,
                    use_container_width=True,
                    hide_index=True,
                    selection_mode="single-row",
                    on_select="rerun",
                    column_config={"status": st.column_config.TextColumn("Status", width="small")}
                )

                if len(event.selection.rows) > 0:
                    idx = event.selection.rows[0]
                    st.session_state.batch_selected_sentence = (
                        st.session_state.batch_result_df.iloc[idx]["kalimat"]
                    )
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
            sentence_original = st.session_state.batch_selected_sentence
            st.markdown(f"## 🔎 Detail Analisis: *\"{sentence_original}\"*")
            
            # --- LAKUKAN PEMBERSIHAN & STEMMING SEBELUM VISUALISASI ---
            sentence_raw = sentence_original.lower().strip()
            sentence_normalized = unicodedata.normalize('NFKD', sentence_raw).encode('ASCII', 'ignore').decode('utf-8')
            sentence_final, log_perubahan = bersihkan_dan_stem_bali(sentence_normalized, KATA_DASAR_CORPUS)
            
            # Tampilkan notifikasi log jika ada kata yang terpotong di batch
            if log_perubahan:
                st.info(
                    "💡 **Catatan Morfologi:** Sistem menyesuaikan kata ke bentuk dasarnya:\n\n" + 
                    "\n".join([f"- {perubahan}" for perubahan in log_perubahan])
                )
                
            # Gunakan sentence_final (yang sudah bersih) untuk CYK
            result = run_cyk_cached(sentence_final)
            
            # Render visualisasi
            app_ui.render_analysis_results(
                result["words"], result["table"], result["is_valid"],
                cnf_viz, sentence_final, result["backpointers_viz"] # <-- Harus menggunakan sentence_final
            )

    elif menu == "📊 Statistik":
        stats_manager.render_stats_dashboard(st.session_state.dark_mode)

    elif menu == "📚 Referensi":
        app_ui.render_grammar_expanders(RULES_CFG, st.session_state.dark_mode)

if __name__ == "__main__":
    main()
