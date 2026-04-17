import streamlit as st
import os
import json
import html
from pathlib import Path
from groq import Groq
from fpdf import FPDF
from core import create_parse_tree

# ============================================================
# Helper: Load Lexicon — cached, dipanggil langsung dari
#         session_state di main.py supaya tidak re-load
# ============================================================
@st.cache_data
def load_lexicon_data():
    json_path = Path(__file__).parent.parent / "scraping" / "balinese_lexicon.json"
    try:
        with open(json_path, "r", encoding="utf-8") as f:
            return json.load(f)
    except Exception:
        return {}

def _get_lexicon() -> dict:
    """Ambil lexicon dari session_state (sudah di-load di main.py)."""
    return st.session_state.get("lexicon_data", {})

# ============================================================
# AI Helper Functions & Guardrails
# ============================================================
def format_cell_content(cell_set):
    if not cell_set:
        return "∅"
    return "{" + ", ".join(sorted(cell_set)) + "}"

def get_word_meanings(words, lexicon_data):
    meanings = []
    for w in words:
        found = None
        for cat, entries in lexicon_data.items():
            if w in entries:
                found = entries[w]
                break
        meanings.append(f"'{w}' → '{found}'" if found else f"'{w}' → (arti tidak diketahui)")
    return ", ".join(meanings)

def get_ai_chat_response(user_message, chat_history, words, parse_table, is_valid, lexicon_data):
    groq_key = os.getenv('GROQ_API_KEY')
    if not groq_key:
        return "⚠️ API Key Groq tidak ditemukan."

    client = Groq(api_key=groq_key)
    n = len(words)

    table_summary = ""
    for length in range(1, n + 1):
        row_cells = [
            format_cell_content(parse_table[i][i + length - 1])
            for i in range(n - length + 1)
        ]
        table_summary += f"L{length}: " + " | ".join(row_cells) + "\n"

    word_context = get_word_meanings(words, lexicon_data)

    system_message = f"""Kamu adalah asisten pakar Linguistik Komputasi Bahasa Bali.

🚨 ATURAN SUPER KETAT:
1. P (Predikat) = NumP (Frasa Numeralia).
2. Pel (Pelengkap) = VP (Frasa Verba) / V (Verba) / AdjP.
3. JANGAN SOK TAHU: Jika user bertanya kenapa kata kerja (seperti majajal) masuknya ke Pel (Pelengkap) dan bukan Predikat, JAWAB DENGAN TEGAS: "Berdasarkan struktur tata bahasa (grammar) pada parser ini, predikat kalimat diisi oleh Frasa Numeralia, sedangkan Frasa Verba berfungsi sebagai Pelengkap (Pel)." 
4. JANGAN PERNAH membenarkan user jika mereka memaksa bahwa itu harusnya Predikat. Pertahankan grammar dari tabel CYK!
5. Gunakan format Bullet Points yang rapi.

Data Kalimat:
- Kalimat: {' '.join(words)}
- Arti: {word_context}
- Tabel CYK:
{table_summary}
"""

    messages = [{"role": "system", "content": system_message}] + chat_history + [{"role": "user", "content": user_message}]

    try:
        completion = client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=messages,
            temperature=0.1
        )
        return completion.choices[0].message.content
    except Exception as e:
        return f"Error: {str(e)}"

def get_ai_explanation_text(words, parse_table, is_valid, lexicon_data):
    groq_key = os.getenv('GROQ_API_KEY')
    if not groq_key:
        return "⚠️ API Key Groq tidak ditemukan."

    client = Groq(api_key=groq_key)
    n = len(words)

    # FIX 5: Bangun string dengan list join, bukan += berulang
    rows = []
    for length in range(1, n + 1):
        row_cells = []
        for i in range(n - length + 1):
            j = i + length - 1
            content = format_cell_content(parse_table[i][j])
            if content != "∅":
                gabungan_kata = " ".join(words[i:j + 1])
                row_cells.append(f"'{gabungan_kata}' → {content}")
        if row_cells:
            rows.append(f"Level {length}: " + " | ".join(row_cells))
    table_text = "\n".join(rows)

    word_context = get_word_meanings(words, lexicon_data)

    system_prompt = """Kamu adalah dosen Linguistik Komputasi Bahasa Bali yang bertugas menjelaskan langkah-langkah algoritma CYK kepada mahasiswa.

🚨 ATURAN MUTLAK (WAJIB DIPATUHI):
1. CARA MENJELASKAN: Jangan sekadar menyalin isi tabel. Ceritakan PROSESNYA. (Contoh yang benar: "Frasa 'duang ukud' (NumP) terbentuk dari gabungan kata 'duang' (Num) dan 'ukud' (Noun)").
2. ATURAN GRAMMAR KHUSUS: Predikat (P) pada sistem ini HANYA diisi oleh Frasa Numeralia (NumP). Frasa Verba (VP) / Verba (V) diklasifikasikan sebagai Pelengkap (Pel). JANGAN PERNAH menyalahkan aturan ini.
3. FOKUS: Hanya jelaskan kata atau frasa yang BERHASIL digabungkan (yang ada di tabel).
4. Gunakan bahasa yang edukatif, rapi, dan mudah dipahami.
"""

    user_prompt = f"""
Tolong jelaskan secara naratif langkah-langkah parsing CYK untuk kalimat: "{' '.join(words)}" (Status: {'VALID' if is_valid else 'INVALID'}).

Arti kata:
{word_context}

Data Tabel CYK yang Berhasil Terbentuk:
{table_text}

Instruksi Format Output (Gunakan Bullet Points):
1. **Level 1 (Analisis Leksikal):** Jelaskan kategori dasar setiap kata (misal: 'macan' adalah Noun/Kata Benda).
2. **Level Selanjutnya (Analisis Sintaksis):** Jelaskan bagaimana frasa yang lebih besar terbentuk dari gabungan kata/frasa di level sebelumnya berdasarkan data tabel di atas.
3. **Puncak Analisis:** Jelaskan konklusi akhirnya (apakah simbol 'K' / Kalimat utuh berhasil terbentuk di level akhir?).
"""

    try:
        completion = client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_prompt}
            ],
            temperature=0.2
        )
        return completion.choices[0].message.content
    except Exception as e:
        return f"Error: {str(e)}"

# ============================================================
# Modal / Pop-Up Chat & Dictionaries
# ============================================================
@st.dialog("💬 Tanya AI tentang kalimat ini", width="large")
def ai_chat_modal(words, table, is_valid, lexicon_data, sentence_str):
    st.markdown("""
        <style>
        [data-testid="stChatMessage"] {
            border-radius: 12px;
            padding: 0.8rem 1.2rem;
            margin-bottom: 0.8rem;
            background-color: rgba(255,255,255,0.03);
            border: 1px solid rgba(255,255,255,0.08);
        }
        </style>
    """, unsafe_allow_html=True)

    sentence_key = sentence_str.replace(" ", "_")
    chat_history_key = f"chat_history_only_{sentence_key}"

    if chat_history_key not in st.session_state:
        st.session_state[chat_history_key] = [
            {"role": "assistant", "content": f"Halo! Ada yang ingin ditanyakan terkait hasil *parsing* kalimat **{sentence_str}**?"}
        ]

    chat_container = st.container(height=500)

    with chat_container:
        for msg in st.session_state[chat_history_key]:
            with st.chat_message(msg["role"]):
                st.markdown(msg["content"])

    prompt = st.chat_input("Tanyakan sesuatu (misal: Kenapa majajal jadi Pelengkap?)...")

    if prompt:
        safe_prompt = html.escape(prompt.strip())[:1000]
        st.session_state[chat_history_key].append({"role": "user", "content": safe_prompt})
        with chat_container:
            with st.chat_message("user"):
                st.markdown(safe_prompt)
            with st.chat_message("assistant"):
                with st.spinner("Menganalisis..."):
                    response = get_ai_chat_response(
                        user_message=safe_prompt,
                        chat_history=st.session_state[chat_history_key][:-1],
                        words=words,
                        parse_table=table,
                        is_valid=is_valid,
                        lexicon_data=lexicon_data
                    )
                    st.markdown(response)
                    st.session_state[chat_history_key].append({"role": "assistant", "content": response})


# Kamus sederhana: hanya Bali, kategori, dan terjemahan Indonesia
@st.dialog("📚 Kamus", width="small")
def show_word_detail(word, category, lexicon_data):
    translation = "(Arti tidak ditemukan)"
    for cat_key, entries in lexicon_data.items():
        if word in entries:
            translation = entries[word]
            break

    st.markdown(f"""
        <div class="custom-card" style="text-align: center; padding: 1.2rem 0 1.2rem 0; margin-bottom: 1.2rem;">
            <h1 style="color: #38bdf8; margin-bottom: 0; font-size: 2.2rem; letter-spacing: 1px;">{word.capitalize()}</h1>
            <p style="color: #94a3b8; font-size: 1.05rem; margin-top: 0; font-style: italic;">{category}</p>
        </div>
        <div class="custom-card" style="background: none; border-left: 4px solid #10b981; margin-bottom: 1.5rem; text-align: left;">
            <div style="font-size: 0.98rem; color: #38bdf8; font-weight: 600; margin-bottom: 0.2rem;">🇮🇩 Terjemahan Indonesia:</div>
            <div style="font-size: 1.2rem; color: #10b981; font-weight: 700;">{translation.capitalize()}</div>
        </div>
    """, unsafe_allow_html=True)

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
            col_count = 1 + len(items) + (len(items) - 1 if len(items) > 0 else 0)
            cols = st.columns(col_count, vertical_alignment="center")
            curr = 0
            cols[curr].markdown("<div class='arrow'>&rarr;</div>", unsafe_allow_html=True); curr += 1
            for i, item in enumerate(items):
                if i > 0:
                    cols[curr].markdown("<div class='arrow'>+</div>", unsafe_allow_html=True); curr += 1
                if item in all_rules or item in lexical_data:
                    if cols[curr].button(item, key=f"mod_btn_{symbol}_{idx}_{i}_{item}"):
                        st.session_state["modal_symbol"] = item
                        st.rerun()
                else:
                    cols[curr].markdown(f"<div class='t-chip-static'>{item}</div>", unsafe_allow_html=True)
                curr += 1
            st.write("")
    elif symbol in lexical_data:
        st.markdown(f"**Contoh Kata ({len(lexical_data[symbol])}):**")
        words = sorted(lexical_data[symbol])
        html_words = "".join([f"<span class='vocab-chip'>{w}</span>" for w in words])
        st.markdown(f"<div class='vocab-grid'>{html_words}</div>", unsafe_allow_html=True)
    else:
        st.info("Simbol terminal dasar.")

# ============================================================
# UI Rendering Functions
# ============================================================
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

    # FIX 5: list join — jauh lebih cepat dari string +=
    rows = []
    for i in reversed(range(n)):
        cells = []
        for j in range(n - i):
            cell_set = parse_table[j][j + i]
            is_root = (i == n - 1)
            if is_root and 'K' in cell_set:
                style = "background-color: rgba(16, 185, 129, 0.2); color: #10b981; font-weight:bold; border: 2px solid #10b981;"
            else:
                style = ""
            content = ", ".join(f"<b>{sym}</b>" for sym in sorted(cell_set)) if cell_set else "∅"
            cells.append(f"<td style='{style}; min-width:100px; text-align:center;'>{content}</td>")
        # Padding kosong untuk kolom sisa
        cells.extend(["<td style='border:none; background:transparent;'></td>"] * i)
        rows.append(f"<tr>{''.join(cells)}</tr>")

    # Baris header kata
    word_cells = "".join(
        f"<td style='border-top: 2px solid #38bdf8; color: #38bdf8; font-weight:bold; text-align:center;'>{w}</td>"
        for w in words
    )
    rows.append(f"<tr>{word_cells}</tr>")

    html_table = f'<div style="overflow-x:auto;"><table class="cyk-table">{"".join(rows)}</table></div>'
    st.markdown(html_table, unsafe_allow_html=True)

    # Legenda
    used_syms: set = set()
    for i in range(n):
        for j in range(i, n):
            used_syms.update(parse_table[i][j])
    valid_legend_syms = sorted(s for s in used_syms if s in EXPLANATIONS)
    if valid_legend_syms:
        items = "".join(f"<li><b>{s}</b>: {EXPLANATIONS[s]}</li>" for s in valid_legend_syms)
        st.markdown(
            f"<div style='margin-top:1.5em;'><b>Legenda Simbol:</b><ul style='columns:2; font-size:13px;'>{items}</ul></div>",
            unsafe_allow_html=True
        )

def render_analysis_results(words, table, is_valid, cnf_grammar, sentence_str, backpointers):
    if is_valid:
        st.success(f"✅ Kalimat VALID: **{sentence_str}**")
    else:
        st.error(f"❌ Kalimat INVALID: **{sentence_str}**")

    col_table, col_tree = st.columns([1.2, 1])

    with col_table:
        render_parse_table(words, table, is_valid=is_valid)

    dot = None
    with col_tree:
        st.markdown("### 🌳 Visualisasi Tree")
        if is_valid:
            dot = create_parse_tree(words, table, cnf_grammar, backpointers)
            st.markdown('<div class="custom-card">', unsafe_allow_html=True)
            st.graphviz_chart(dot, use_container_width=True)
            st.markdown('</div>', unsafe_allow_html=True)
        else:
            st.warning("Tree tidak dapat dibentuk karena kalimat tidak valid.")

    st.divider()

    # FIX 3: Ambil lexicon dari session_state, bukan re-load
    lexicon_data = _get_lexicon()
    sentence_key = sentence_str.replace(" ", "_")
    expl_key = f"ai_expl_{sentence_key}"

    col1, col2 = st.columns(2)
    with col1:
        if st.button("📝 Buat Penjelasan Tabel (AI)", use_container_width=True, key=f"btn_expl_{sentence_key}"):
            with st.spinner("AI sedang merangkum tabel CYK..."):
                expl = get_ai_explanation_text(words, table, is_valid, lexicon_data)
                st.session_state[expl_key] = expl

    with col2:
        if st.button("💬 Tanya AI tentang kalimat ini", type="primary", use_container_width=True, key=f"btn_chat_{sentence_key}"):
            ai_chat_modal(words, table, is_valid, lexicon_data, sentence_str)

    if st.session_state.get(expl_key):
        with st.expander("📚 Penjelasan Langkah-Langkah CYK (Klik untuk menutup)", expanded=True):
            st.markdown(st.session_state[expl_key])

    st.divider()
    st.markdown("### 📄 Export Laporan ke PDF")

    with st.expander("⚙️ Atur Isi Laporan PDF"):
        c_opt1, c_opt2 = st.columns(2)
        with c_opt1:
            inc_expl = st.checkbox("Sertakan Penjelasan AI", value=bool(st.session_state.get(expl_key)), key=f"chk_expl_{sentence_key}")
            inc_table = st.checkbox("Sertakan Tabel CYK", value=True, key=f"chk_table_{sentence_key}")
        with c_opt2:
            inc_tree = st.checkbox("Sertakan Visualisasi Pohon", value=is_valid, disabled=not is_valid, key=f"chk_tree_{sentence_key}")

        if st.button("🛠️ Generate & Preview PDF", use_container_width=True, key=f"btn_pdf_{sentence_key}"):
            with st.spinner("Menyusun dokumen PDF..."):
                current_expl = st.session_state.get(expl_key, "")
                pdf_bytes = generate_pdf_report(
                    sentence_str, is_valid,
                    current_expl if inc_expl else "",
                    inc_table, inc_tree, words, table, dot
                )
                st.download_button(
                    label="📥 Download PDF Sekarang",
                    data=bytes(pdf_bytes),
                    file_name=f"Analisis_{sentence_key}.pdf",
                    mime="application/pdf",
                    use_container_width=True,
                    key=f"dl_pdf_{sentence_key}"
                )

# ============================================================
# Grammar Reference & Explanations
# ============================================================
EXPLANATIONS = {
    "K": "Kalimat Utuh (keseluruhan kalimat)",
    "K1": "Kalimat Inti (bagian utama: Subjek + Predikat, inti makna kalimat)",
    "K2": "Kalimat Pelengkap (bagian tambahan, misal keterangan/waktu/tempat)",
    "S": "Subjek (pelaku/yang dibicarakan)",
    "P": "Predikat (kata kerja/aksi)",
    "O": "Objek (yang dikenai aksi)",
    "Pel": "Pelengkap (penjelas tambahan)",
    "Ket": "Keterangan (waktu/tempat/cara)",
    "NP": "Frasa Nomina (kelompok kata benda)",
    "NumP": "Frasa Numeralia (kelompok kata bilangan)",
    "VP": "Frasa Verba (kelompok kata kerja)",
    "AdjP": "Frasa Adjektiva (kelompok kata sifat)",
    "PP": "Frasa Preposisi (kelompok kata depan)",
    "Noun": "Kata Benda",
    "Verb": "Kata Kerja",
    "Adj": "Kata Sifat",
    "Num": "Bilangan",
    "Adv": "Keterangan",
    "Prep": "Kata Depan",
    "Pronoun": "Kata Ganti",
    "PropNoun": "Nama Diri",
    "Det": "Kata Penunjuk"
}

def render_grammar_expanders(rules_cfg, dark_mode=False):
    st.markdown("<h2 style='margin-bottom: 1.5rem;'>📚 Referensi Tata Bahasa</h2>", unsafe_allow_html=True)
    structural_rules = {}
    lexical_categories = {}

    for head, bodies in rules_cfg.items():
        is_lexical = False
        words = []
        for body in bodies:
            if isinstance(body, list) and len(body) == 1 and isinstance(body[0], str) and body[0].islower():
                is_lexical = True
                words.append(body[0])
            elif isinstance(body, str) and body.islower():
                is_lexical = True
                words.append(body)
        if is_lexical:
            lexical_categories[head] = words
        else:
            structural_rules[head] = bodies

    if st.session_state.get("is_dialog_open"):
        main_rule_dialog(structural_rules, lexical_categories)

    tab1, tab2 = st.tabs(["🔀 Pola Struktur (Rules)", "📖 Kamus Kata (A-Z)"])

    with tab1:
        st.markdown('<div class="custom-card">', unsafe_allow_html=True)
        st.info("💡 **Tip:** Klik simbol berwarna biru (misal: `K1`) di dalam rumus untuk melihat detailnya.")
        c1, c2 = st.columns([4, 1], vertical_alignment="bottom")
        with c1:
            search_rule = st.text_input("Cari Pola", key="s_rule", placeholder="Contoh: NP")
        with c2:
            st.button("🔍 Cari", key="b_s_rule", use_container_width=True)
        st.markdown("---")

        priority = ["K", "K1", "K2", "S", "P", "O", "Pel", "Ket", "NP", "NumP", "VP", "AdjP", "PP"]
        sorted_keys = sorted(structural_rules.keys(), key=lambda x: priority.index(x) if x in priority else 99)

        for nt in sorted_keys:
            desc = EXPLANATIONS.get(nt, "Aturan Produksi")
            if search_rule.lower() and (search_rule.lower() not in nt.lower() and search_rule.lower() not in desc.lower()):
                continue
            with st.expander(f"**{nt}** — {desc}"):
                for idx, prod in enumerate(structural_rules[nt]):
                    items = prod if isinstance(prod, list) else [prod]
                    elements = [('static_lhs', nt, desc), ('arrow', '→', '')]
                    for i, item in enumerate(items):
                        if i > 0:
                            elements.append(('plus', '+', ''))
                        tooltip = EXPLANATIONS.get(item, "")
                        etype = 'btn' if item[0].isupper() else 'static_t'
                        elements.append((etype, item, tooltip))

                    ratio_map = {'static_lhs': 1.2, 'arrow': 0.4, 'plus': 0.4, 'btn': 1.5, 'static_t': 1.5}
                    col_ratios = [ratio_map[e[0]] for e in elements]
                    cols = st.columns(col_ratios, vertical_alignment="center")

                    for col_idx, (c, (etype, val, tip)) in enumerate(zip(cols, elements)):
                        if etype == 'static_lhs':
                            c.markdown(f"<div class='nt-chip-static'>{val}</div>", unsafe_allow_html=True)
                        elif etype == 'arrow':
                            c.markdown("<div class='arrow'>&rarr;</div>", unsafe_allow_html=True)
                        elif etype == 'plus':
                            c.markdown("<div class='arrow'>+</div>", unsafe_allow_html=True)
                        elif etype == 'static_t':
                            c.markdown(f"<div class='t-chip-static'>{val}</div>", unsafe_allow_html=True)
                        elif etype == 'btn':
                            key_id = f"inl_btn_{nt}_{idx}_{val}_{col_idx}"
                            if c.button(val, key=key_id, help=tip):
                                st.session_state["modal_symbol"] = val
                                st.session_state["is_dialog_open"] = True
                                st.rerun()
                    st.write("")
        st.markdown('</div>', unsafe_allow_html=True)

    with tab2:
        # FIX 3: Gunakan lexicon dari session_state
        lexicon_data = _get_lexicon()

        st.markdown('<div class="custom-card">', unsafe_allow_html=True)
        c1, c2 = st.columns([4, 1], vertical_alignment="bottom")
        with c1:
            search_vocab = st.text_input("Cari Kata", key="s_vocab")
        with c2:
            st.button("🔍 Cari", key="b_s_vocab", use_container_width=True)
        st.markdown("---")

        friendly_cat_names = {
            "Noun": "Kata Benda", "Verb": "Kata Kerja", "Adj": "Kata Sifat",
            "Num": "Bilangan", "Adv": "Keterangan", "Prep": "Preposisi",
            "Pronoun": "Kata Ganti", "PropNoun": "Nama Diri", "Det": "Penunjuk"
        }

        sorted_cats = sorted(lexical_categories.keys(), key=lambda x: friendly_cat_names.get(x, x))
        for cat in sorted_cats:
            words_list = sorted(lexical_categories[cat])
            if search_vocab:
                words_list = [w for w in words_list if search_vocab.lower() in w.lower()]
            if not words_list:
                continue

            with st.expander(f"📂 {friendly_cat_names.get(cat, cat)} ({len(words_list)})"):
                grouped = {}
                for w in words_list:
                    grouped.setdefault(w[0].upper(), []).append(w)

                for letter in sorted(grouped.keys()):
                    st.markdown(
                        f"<h4 style='margin-top: 1rem; color: #38bdf8; border-bottom: 1px solid rgba(255,255,255,0.1); padding-bottom: 0.5rem;'>{letter}</h4>",
                        unsafe_allow_html=True
                    )
                    words_in_letter = grouped[letter]
                    chunk_size = 4
                    for i in range(0, len(words_in_letter), chunk_size):
                        cols = st.columns(chunk_size)
                        for j, w in enumerate(words_in_letter[i:i + chunk_size]):
                            with cols[j]:
                                if st.button(w, key=f"vocab_{cat}_{w}_{i}_{j}", use_container_width=True):
                                    show_word_detail(w, friendly_cat_names.get(cat, cat), lexicon_data)
        st.markdown('</div>', unsafe_allow_html=True)


def generate_pdf_report(sentence, is_valid, explanation, include_table, include_tree, words, table, dot_obj=None):
    import io
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", "B", 16)

    pdf.cell(0, 10, "Laporan Analisis Struktur Kalimat", ln=True, align='C')
    pdf.ln(5)

    pdf.set_font("Arial", "B", 12)
    pdf.cell(0, 10, f"Kalimat: {sentence}", ln=True)
    status_text = "VALID" if is_valid else "INVALID"
    if is_valid:
        pdf.set_text_color(16, 185, 129)
    else:
        pdf.set_text_color(220, 38, 38)
    pdf.cell(0, 10, f"Status: {status_text}", ln=True)
    pdf.set_text_color(0, 0, 0)
    pdf.ln(5)

    if explanation:
        pdf.set_font("Arial", "B", 12)
        pdf.cell(0, 10, "Analisis Algoritma CYK:", ln=True)
        pdf.set_font("Arial", "", 10)
        pdf.multi_cell(0, 5, explanation.replace('*', ''))
        pdf.ln(10)

    if include_table:
        pdf.set_font("Arial", "B", 12)
        pdf.cell(0, 10, "Tabel Parsing CYK:", ln=True)
        pdf.set_font("Courier", "", 8)
        n = len(words)
        for i in reversed(range(n)):
            row_content = []
            for j in range(n - i):
                cell = table[j][j + i]
                content = "{" + ",".join(sorted(cell)) + "}" if cell else "{}"
                row_content.append(content.ljust(15))
            pdf.cell(0, 5, "".join(row_content), ln=True)
        pdf.ln(10)

    if include_tree and is_valid and dot_obj:
        pdf.set_font("Arial", "B", 12)
        pdf.cell(0, 10, "Visualisasi Pohon Sintaksis:", ln=True)
        try:
            img_bytes = dot_obj.pipe(format='png')
            img_stream = io.BytesIO(img_bytes)
            pdf.image(img_stream, x=10, w=180)
        except Exception:
            pdf.set_font("Arial", "I", 10)
            pdf.cell(0, 10, "(Gagal merender gambar: Pastikan Graphviz terinstal di sistem)", ln=True)

    return pdf.output()