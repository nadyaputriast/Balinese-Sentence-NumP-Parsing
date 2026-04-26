import streamlit as st
import pandas as pd
import os
import io
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
            st.markdown(
                "Upload satu atau beberapa file untuk validasi massal. "
                "Kolom wajib: **`kalimat`**"
            )

            uploaded_files = st.file_uploader(
                "Upload File",
                type=["csv", "xlsx", "xls", "docx", "txt"],
                accept_multiple_files=True,
                help=(
                    "**CSV / Excel**: butuh kolom `kalimat`\n\n"
                    "**Word (.docx)**: tabel dengan header `kalimat`, "
                    "atau list (bullet/numbered), atau paragraf biasa\n\n"
                    "**TXT**: tiap baris = 1 kalimat"
                )
            )

            if uploaded_files:
                with st.expander(f"👀 Preview {len(uploaded_files)} file yang dipilih"):
                    for f in uploaded_files:
                        st.markdown(f"**{f.name}**")
                        try:
                            f.seek(0)
                            if f.name.lower().endswith(('.xlsx', '.xls')):
                                st.dataframe(pd.read_excel(f).head(3), use_container_width=True)
                            elif f.name.lower().endswith('.csv'):
                                st.dataframe(pd.read_csv(f).head(3), use_container_width=True)
                            elif f.name.lower().endswith('.txt'):
                                lines = f.read().decode('utf-8', errors='ignore').splitlines()
                                lines = [l.strip() for l in lines if l.strip()][:3]
                                st.dataframe(pd.DataFrame({'kalimat': lines}), use_container_width=True)
                            elif f.name.lower().endswith('.docx'):
                                from docx import Document
                                import io
                                doc = Document(io.BytesIO(f.read()))
                                paras = [p.text.strip() for p in doc.paragraphs if p.text.strip()][:3]
                                st.dataframe(pd.DataFrame({'kalimat': paras}), use_container_width=True)
                            else:
                                st.caption("_(preview tidak tersedia)_")
                            f.seek(0)
                        except Exception:
                            st.caption("_(gagal membaca preview)_")

                if st.button("🚀 Proses Semua File", type="primary", use_container_width=True):
                    with st.spinner("Memproses..."):
                        df, err = batch_processor.process_files(
                            uploaded_files,
                            KATA_DASAR_CORPUS,
                            bersihkan_dan_stem_bali
                        )
                        if err:
                            st.error(err)
                        else:
                            st.session_state.batch_result_df = df
                            st.session_state.excel_cache = None
                            st.rerun()

            if st.session_state.batch_result_df is not None:
                df_result = st.session_state.batch_result_df
                st.divider()

                # Metrics
                total = len(df_result)
                valid = len(df_result[df_result["status"] == "VALID"])
                c1, c2, c3 = st.columns(3)
                c1.metric("Total Kalimat", total)
                c2.metric("Valid ✅", valid)
                c3.metric("Invalid ❌", total - valid)

                # Filter per sumber
                if 'sumber' in df_result.columns:
                    sources = df_result['sumber'].unique().tolist()
                    if len(sources) > 1:
                        selected_source = st.selectbox(
                            "🔍 Filter per file:",
                            options=["Semua"] + sources
                        )
                        df_view = (
                            df_result if selected_source == "Semua"
                            else df_result[df_result['sumber'] == selected_source]
                        )
                    else:
                        df_view = df_result
                else:
                    df_view = df_result

                st.markdown("#### 📥 Download Hasil")
                col_excel, col_reset = st.columns([3, 1])

                with col_excel:
                    if st.session_state.get("excel_cache") is None:
                        st.session_state.excel_cache = batch_processor.to_excel_bytes(df_result)

                    st.download_button(
                        label="⬇️ Download Excel",
                        data=st.session_state.excel_cache,
                        file_name="hasil_validasi.xlsx",
                        mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
                        use_container_width=True,
                    )

                with col_reset:
                    if st.button("🗑️ Reset", use_container_width=True):
                        st.session_state.batch_result_df = None
                        st.session_state.excel_cache = None
                        st.rerun()

                st.markdown("#### 📋 Klik baris untuk detail")
                event = st.dataframe(
                    df_view,
                    use_container_width=True,
                    hide_index=True,
                    selection_mode="single-row",
                    on_select="rerun",
                    column_config={
                        "sumber": st.column_config.TextColumn("Sumber File", width="medium"),
                        "status": st.column_config.TextColumn("Status",      width="small"),
                    }
                )

                if len(event.selection.rows) > 0:
                    idx = event.selection.rows[0]
                    st.session_state.batch_selected_sentence = df_view.iloc[idx]["kalimat"]
                    st.session_state.batch_view_mode = "detail"
                    st.rerun()

        elif st.session_state.batch_view_mode == "detail":
            if st.button("← Kembali ke Daftar Batch"):
                st.session_state.batch_view_mode = "list"
                st.rerun()
                
            st.divider()
            sentence_original = st.session_state.batch_selected_sentence
            st.markdown(f"## 🔎 Detail Analisis: *\"{sentence_original}\"*")

            sentence_raw = sentence_original.lower().strip()
            sentence_normalized = unicodedata.normalize('NFKD', sentence_raw).encode('ASCII', 'ignore').decode('utf-8')
            sentence_final, log_perubahan = bersihkan_dan_stem_bali(sentence_normalized, KATA_DASAR_CORPUS)

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
                cnf_viz, sentence_final, result["backpointers_viz"]
            )

    elif menu == "📊 Statistik":
        stats_manager.render_stats_dashboard(st.session_state.dark_mode)

    elif menu == "📚 Referensi":
        app_ui.render_grammar_expanders(RULES_CFG, st.session_state.dark_mode)

if __name__ == "__main__":
    main()
