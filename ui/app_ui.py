import streamlit as st
import os
from openai import OpenAI
from core import create_parse_tree # Import create_parse_tree disini biar rapi

# --- HELPER FUNCTIONS ---

def format_cell_content(cell_set):
    if not cell_set: return "∅"
    return "{" + ", ".join(sorted(cell_set)) + "}"

def get_ai_explanation_text(words, parse_table, is_valid):
    api_key = os.getenv('OPENAI_API_KEY')
    if not api_key: return "⚠️ OpenAI API key tidak ditemukan."
    try:
        client = OpenAI(api_key=api_key)
        n = len(words)
        table_text = ""
        for i in range(n):
            row_cells = [format_cell_content(parse_table[j][j + i]) for j in range(n - i)]
            table_text += f"Row {i+1}: " + " | ".join(row_cells) + "\n"
        
        prompt = f"""
        Jelaskan Tabel CYK kalimat: "{' '.join(words)}" ({'VALID' if is_valid else 'INVALID'}).
        Bahasa santai. Data: {table_text}
        """
        response = client.chat.completions.create(
            model="gpt-4o-mini", messages=[{"role": "user", "content": prompt}], temperature=0.7, max_tokens=250
        )
        return response.choices[0].message.content
    except Exception as e: return f"Error AI: {str(e)}"

# --- MAIN UI RENDER FUNCTIONS ---

def render_header(dark_mode=False):
    st.markdown("""
        <div style="text-align: center; margin: 2rem 0 3rem 0;">
            <h1 style="font-size: 2.5rem; margin-bottom: 0.5rem;">Balinese Parser</h1>
            <p style="opacity: 0.7; max-width: 600px; margin: 0 auto;">
                Analisis struktur kalimat Bahasa Bali berpredikat <b>Frasa Numeralia</b>.
            </p>
        </div>
    """, unsafe_allow_html=True)

def render_parse_table(words, parse_table, dark_mode=False, is_valid=None):
    st.markdown("### 🧬 Tabel Parsing CYK")
    n = len(words)
    html = '<div style="overflow-x:auto;"><table class="cyk-table">'
    for i in range(n):
        html += "<tr>"
        for j in range(n):
            if j < n - i:
                cell_set = parse_table[j][j+i]
                style = "background-color: rgba(16, 185, 129, 0.2); color: #10b981; font-weight:bold;" if i == n-1 and 'K' in cell_set else ""
                html += f"<td style='{style}'>{format_cell_content(cell_set)}</td>"
            else: html += "<td style='border:none; background:transparent;'></td>"
        html += "</tr>"
    html += "<tr>" + "".join([f"<td style='border-top: 2px solid #38bdf8; color: #38bdf8; font-weight:bold;'>{w}</td>" for w in words]) + "</tr></table></div>"
    st.markdown(html, unsafe_allow_html=True)

# --- REUSABLE RESULT VIEW (UTAMA & BATCH) ---
def render_analysis_results(words, table, is_valid, cnf_grammar, sentence_str):
    """
    Menampilkan Layout Hasil Analisis (Tabel Kiri, Tree Kanan)
    Dipakai di Halaman Utama dan Modal Batch.
    """
    # 1. Status Banner
    if is_valid:
        st.success(f"✅ Kalimat VALID: **{sentence_str}**")
    else:
        st.error(f"❌ Kalimat INVALID: **{sentence_str}**")

    # 2. Dua Kolom: Tabel & Tree
    col_table, col_tree = st.columns([1.2, 1])
    
    # --- KIRI: TABEL ---
    with col_table:
        render_parse_table(words, table, is_valid=is_valid)
        
        # AI Explanation
        if st.button("🤖 Jelaskan dengan AI", key=f"btn_ai_{hash(sentence_str)}"): # Key unik biar ga bentrok
            if not os.getenv("OPENAI_API_KEY"):
                 st.error("Error: API Key belum terbaca! Cek file .env")
            else:
                with st.spinner("AI sedang berpikir..."):
                    expl = get_ai_explanation_text(words, table, is_valid)
                    st.info(expl)

    # --- KANAN: TREE ---
    with col_tree:
        st.markdown("### 🌳 Visualisasi Tree")
        if is_valid:
            dot = create_parse_tree(words, table, cnf_grammar)
            st.markdown('<div class="custom-card">', unsafe_allow_html=True)
            st.graphviz_chart(dot, use_container_width=True)
            st.markdown('</div>', unsafe_allow_html=True)
        else:
            st.warning("Tree tidak dapat dibentuk karena kalimat tidak valid.")


# --- INTERACTIVE MODAL & GRAMMAR (SAMA SEPERTI SEBELUMNYA) ---
EXPLANATIONS = {
    "K": "Kalimat Utuh", "K1": "Kalimat Inti", "K2": "Kalimat Pelengkap",
    "S": "Subjek", "P": "Predikat", "O": "Objek", "Pel": "Pelengkap", "Ket": "Keterangan",
    "NP": "Frasa Nomina (Benda)", "NumP": "Frasa Numeralia (Bilangan)",
    "VP": "Frasa Verba (Kerja)", "AdjP": "Frasa Adjektiva (Sifat)", "PP": "Frasa Preposisi",
    "Noun": "Kata Benda", "Verb": "Kata Kerja", "Adj": "Kata Sifat", "Num": "Bilangan", 
    "Adv": "Keterangan", "Prep": "Kata Depan", "Pronoun": "Kata Ganti", 
    "PropNoun": "Nama Diri", "Det": "Kata Penunjuk"
}

@st.dialog("🔎 Detail Aturan")
def main_rule_dialog(all_rules, lexical_data):
    symbol = st.session_state.get("modal_symbol", "K")
    desc = EXPLANATIONS.get(symbol, "Simbol Tata Bahasa")
    
    st.subheader(f"{symbol}")
    st.caption(f"💡 {desc}")
    st.divider()

    if symbol in all_rules:
        st.markdown("**Aturan Pembentuk:**")
        for idx, prod in enumerate(all_rules[symbol]):
            items = prod if isinstance(prod, list) else [prod]
            col_count = 1 + len(items) + (len(items)-1 if len(items)>0 else 0)
            cols = st.columns(col_count, vertical_alignment="center")
            curr = 0
            cols[curr].markdown("<div class='arrow'>&rarr;</div>", unsafe_allow_html=True); curr+=1
            for i, item in enumerate(items):
                if i > 0: cols[curr].markdown("<div class='arrow'>+</div>", unsafe_allow_html=True); curr+=1
                if item in all_rules or item in lexical_data:
                    if cols[curr].button(item, key=f"mod_btn_{symbol}_{idx}_{i}_{item}"):
                        st.session_state["modal_symbol"] = item; st.rerun()
                else:
                    cols[curr].markdown(f"<div class='t-chip-static'>{item}</div>", unsafe_allow_html=True)
                curr+=1
            st.write("")

    elif symbol in lexical_data:
        st.markdown(f"**Contoh Kata ({len(lexical_data[symbol])}):**")
        words = sorted(lexical_data[symbol])
        html_words = "".join([f"<span class='vocab-chip'>{w}</span>" for w in words])
        st.markdown(f"<div class='vocab-grid'>{html_words}</div>", unsafe_allow_html=True)
    else: st.info("Simbol terminal dasar.")

def render_grammar_expanders(rules_cfg, dark_mode=False):
    st.markdown("<h2 style='margin-bottom: 1.5rem;'>📚 Referensi Tata Bahasa</h2>", unsafe_allow_html=True)
    structural_rules = {}
    lexical_categories = {}
    for head, bodies in rules_cfg.items():
        is_lexical = False
        words = []
        for body in bodies:
            if isinstance(body, list) and len(body) == 1 and isinstance(body[0], str) and body[0].islower():
                is_lexical = True; words.append(body[0])
            elif isinstance(body, str) and body.islower():
                is_lexical = True; words.append(body)
        if is_lexical: lexical_categories[head] = words
        else: structural_rules[head] = bodies

    if st.session_state.get("is_dialog_open"):
        main_rule_dialog(structural_rules, lexical_categories)

    tab1, tab2 = st.tabs(["🔀 Pola Struktur (Rules)", "📖 Kamus Kata (A-Z)"])
    with tab1:
        st.markdown('<div class="custom-card">', unsafe_allow_html=True)
        st.info("💡 **Tip:** Klik simbol berwarna biru (misal: `K1`) di dalam rumus untuk melihat detailnya.")
        c1, c2 = st.columns([4, 1], vertical_alignment="bottom")
        with c1: search_rule = st.text_input("Cari Pola", key="s_rule", placeholder="Contoh: NP")
        with c2: st.button("🔍 Cari", key="b_s_rule", use_container_width=True)
        st.markdown("---")
        priority = ["K", "K1", "K2", "S", "P", "O", "Pel", "Ket", "NP", "NumP", "VP", "AdjP", "PP"]
        sorted_keys = sorted(structural_rules.keys(), key=lambda x: priority.index(x) if x in priority else 99)
        for nt in sorted_keys:
            desc = EXPLANATIONS.get(nt, "Aturan Produksi")
            if search_rule.lower() and (search_rule.lower() not in nt.lower() and search_rule.lower() not in desc.lower()): continue
            with st.expander(f"**{nt}** — {desc}"):
                for idx, prod in enumerate(structural_rules[nt]):
                    items = prod if isinstance(prod, list) else [prod]
                    elements = [] 
                    elements.append(('static_lhs', nt, desc)) 
                    elements.append(('arrow', '→', ''))       
                    for i, item in enumerate(items):
                        if i > 0: elements.append(('plus', '+', ''))
                        tooltip = EXPLANATIONS.get(item, "")
                        if item[0].isupper(): elements.append(('btn', item, tooltip))
                        else: elements.append(('static_t', item, tooltip))
                    col_ratios = []
                    for etype, _, _ in elements:
                        if etype == 'static_lhs': col_ratios.append(1.2)
                        elif etype in ['arrow', 'plus']: col_ratios.append(0.4)
                        elif etype == 'btn': col_ratios.append(1.5)
                        else: col_ratios.append(1.5)
                    cols = st.columns(col_ratios, vertical_alignment="center")
                    for col_idx, (c, (etype, val, tip)) in enumerate(zip(cols, elements)):
                        if etype == 'static_lhs': c.markdown(f"<div class='nt-chip-static'>{val}</div>", unsafe_allow_html=True)
                        elif etype == 'arrow': c.markdown("<div class='arrow'>&rarr;</div>", unsafe_allow_html=True)
                        elif etype == 'plus': c.markdown("<div class='arrow'>+</div>", unsafe_allow_html=True)
                        elif etype == 'static_t': c.markdown(f"<div class='t-chip-static'>{val}</div>", unsafe_allow_html=True)
                        elif etype == 'btn':
                            key_id = f"inl_btn_{nt}_{idx}_{val}_{col_idx}"
                            if c.button(val, key=key_id, help=tip):
                                st.session_state["modal_symbol"] = val; st.session_state["is_dialog_open"] = True; st.rerun()
                    st.write("") 
        st.markdown('</div>', unsafe_allow_html=True)
    with tab2:
        st.markdown('<div class="custom-card">', unsafe_allow_html=True)
        c1, c2 = st.columns([4, 1], vertical_alignment="bottom")
        with c1: search_vocab = st.text_input("Cari Kata", key="s_vocab")
        with c2: st.button("🔍 Cari", key="b_s_vocab", use_container_width=True)
        st.markdown("---")
        friendly_cat_names = { "Noun": "Kata Benda", "Verb": "Kata Kerja", "Adj": "Kata Sifat", "Num": "Bilangan", "Adv": "Keterangan", "Prep": "Preposisi", "Pronoun": "Kata Ganti", "PropNoun": "Nama Diri", "Det": "Penunjuk"}
        sorted_cats = sorted(lexical_categories.keys(), key=lambda x: friendly_cat_names.get(x, x))
        for cat in sorted_cats:
            words = sorted(lexical_categories[cat])
            if search_vocab: words = [w for w in words if search_vocab.lower() in w.lower()]
            if not words: continue
            with st.expander(f"📂 {friendly_cat_names.get(cat, cat)} ({len(words)})"):
                grouped = {}
                for w in words: grouped.setdefault(w[0].upper(), []).append(w)
                for letter in sorted(grouped.keys()):
                    st.markdown(f"<div class='letter-header'>{letter}</div>", unsafe_allow_html=True)
                    chips = "".join([f"<span class='vocab-chip'>{w}</span>" for w in grouped[letter]])
                    st.markdown(f"<div class='vocab-grid'>{chips}</div>", unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)