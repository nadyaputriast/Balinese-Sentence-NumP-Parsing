import streamlit as st
import pandas as pd
import os
from dotenv import load_dotenv

load_dotenv()

from core import cyk_algorithm, create_parse_tree, convert_to_cnf, remove_epsilon_productions, remove_unit_productions
from grammar import RULES_CFG
from ui import app_ui, styles
from utils import stats_manager, batch_processor


# ============================================================
# FIX 1: @st.cache_resource — grammar dihitung SEKALI seumur
#         proses, tidak recompute walau session reset
# ============================================================
@st.cache_resource
def prepare_grammars():
    cfg_no_eps = remove_epsilon_productions(RULES_CFG)
    cfg_strict = remove_unit_productions(cfg_no_eps)
    cnf_strict = convert_to_cnf(cfg_strict)
    cnf_viz = cfg_no_eps
    return cnf_strict, cnf_viz


# ============================================================
# FIX 2: Cache hasil CYK per kalimat di session_state
#         supaya tidak double-run saat rerun UI
# ============================================================
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

    # ============================================================
    # FIX 3: Init semua session state sekaligus di awal,
    #         termasuk lexicon agar load_lexicon_data() hanya
    #         dipanggil sekali dan disimpan di session_state
    # ============================================================
    defaults = {
        "dark_mode": True,
        "input_text": "",
        "batch_result_df": None,
        "batch_view_mode": "list",
        "batch_selected_sentence": None,
        "run_analysis": False,
        "last_text": "",
    }
    for k, v in defaults.items():
        if k not in st.session_state:
            st.session_state[k] = v

    # Lexicon di-load sekali, disimpan di session_state
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

    # FIX 4: apply_styles dipanggil sekali per render, sudah optimal
    styles.apply_styles(st.session_state.dark_mode)

    _, cnf_viz = prepare_grammars()

    if menu == "🏠 Parsing & Visual":
        app_ui.render_header(st.session_state.dark_mode)
        text_val = st.text_input(
            "Input Kalimat", key="widget_input",
            value=st.session_state.input_text,
            placeholder="cth: tiang numbas buku"
        )
        st.write("")

        if st.button("🚀 Analisis Struktur", type="primary", use_container_width=True):
            st.session_state.input_text = text_val
            st.session_state.run_analysis = True

        if st.session_state.get("run_analysis") or (
            text_val and text_val != st.session_state.get("last_text", "")
        ):
            st.session_state.last_text = text_val
            sentence = st.session_state.input_text.lower().strip()
            if sentence:
                result = run_cyk_cached(sentence)
                stats_manager.update_stats(result["is_valid"], sentence)
                st.divider()
                app_ui.render_analysis_results(
                    result["words"], result["table"], result["is_valid"],
                    cnf_viz, sentence, result["backpointers_viz"]
                )
            else:
                st.session_state.run_analysis = False

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
                    except Exception:
                        pass

                if st.button("🚀 Proses Batch", type="primary", use_container_width=True):
                    with st.spinner("Memproses..."):
                        uploaded.seek(0)
                        df, err = batch_processor.process_csv(uploaded)
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
            sentence = st.session_state.batch_selected_sentence
            st.markdown(f"## 🔎 Detail Analisis: *\"{sentence}\"*")
            result = run_cyk_cached(sentence)
            app_ui.render_analysis_results(
                result["words"], result["table"], result["is_valid"],
                cnf_viz, sentence, result["backpointers_viz"]
            )

    elif menu == "📊 Statistik":
        stats_manager.render_stats_dashboard(st.session_state.dark_mode)

    elif menu == "📚 Referensi":
        app_ui.render_grammar_expanders(RULES_CFG, st.session_state.dark_mode)


if __name__ == "__main__":
    main()