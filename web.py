import pandas as pd
import streamlit as st
from cfg_grammar import RULES_CFG
from cnf import convert_to_cnf, remove_epsilon_productions, remove_unit_productions
from cyk import cyk_algorithm, format_cell_content
from parse_tree import create_parse_tree

def main():
    # Set page config
    st.set_page_config(
        page_title="Parsing Kalimat Bahasa Bali Berpredikat Frasa Numeralia",
        page_icon="🏝️",
        layout="wide"
    )

    # Custom CSS
    st.markdown("""
        <style>
        .body {
            background-color: white !important;
        }
        .main {
            padding: 1rem;
        }
        .stTitle {
            color: #1E3A8A;
            font-size: 5rem !important;
            margin-bottom: 1rem !important;
            text-align: center !important;
        }
        .stButton>button {
            width: 100%;
            background-color: #1E3A8A;
            color: white;
            padding: 0.75rem;
            border-radius: 0.5rem;
            border: none;
            font-weight: bold;
        }
        .stButton>button:hover {
            background-color: #1E40AF;
        }
        .dataframe {
            width: 100%;
            font-size: 0.9rem;
            border-collapse: collapse;
        }
        .dataframe td, .dataframe th {
            padding: 0.75rem;
            border: 1px solid #000;
            text-align: center;
        }
        .dataframe td:empty {
            border: none;
        }
        .parse-tree-title {
            text-align: center;
            color: #1E3A8A;
            margin-top: 2rem;
            margin-bottom: 1rem;
        }
        .parse-tree-container {
            display: flex;
            justify-content: center;
            align-items: center;
            width: 100%;
        }
        .parse-tree-container > div {
            display: flex;
            justify-content: center;
            align-items: center;
        }
        .main-title {
            text-align: center;
            color: #1E3A8A;
            font-size: 2.5rem;
            margin-bottom: 2rem;
        }
        </style>
    """, unsafe_allow_html=True)

    # Header section with centered title
    st.markdown("""
        <h1 class="main-title">Parsing Kalimat Bahasa Bali Berpredikat Frasa Numeralia</h1>
        <h3 style='font-size: 2rem; color: #555; text-align: center'>Dibuat oleh Kelompok 5 Kelas D</h3>
        <p style='font-size: 1.1rem; color: #4B5563; margin-bottom: 2rem; text-align: justify;'>
        Website ini dapat digunakan untuk memvalidasi apakah suatu kalimat dengan predikat frasa numeralia valid 
        atau tidak. Frasa numeralia merupakan kelompok kata yang menunjukkan bilangan atau jumlah tertentu. Frasa 
        ini sering digunakan untuk memberikan informasi tentang kuantitas, seperti angka, urutan, atau jumlah benda. 
        <i>Nah</i>, kira-kira ada gak sih suatu kalimat yang predikatnya itu pakai frasa numeralia? Kalau masih 
        bingung kira-kira seperti apa aturannya, bisa dilihat <i>expander</i> di bawah ini ya!
        </p>
    """, unsafe_allow_html=True)

    grammar_keys = ["K", "K1", "K2", "S", "NP", "P", "NumP", "Pel", "AdjP", "VP", "Ket", "PP"]
    vocab_keys = ["PropNoun", "Pronoun", "Noun", "Adj", "Num", "V", "Prep", "Adv", "Det"]

    with st.expander("📚 Lihat Aturan Tata Bahasa", expanded=False):
        st.markdown("""
            <h3 style='color: #1E3A8A; margin-bottom: 1rem;'>Aturan-aturan Tata Bahasa</h3>
        """, unsafe_allow_html=True)
        for lhs in grammar_keys:
            rhs_list = RULES_CFG.get(lhs, [])
            st.markdown(f"""
                <div style='background-color: white; padding: 0.75rem; border-radius: 0.5rem; margin-bottom: 0.5rem;'>
                    <code style='font-size: 1rem;'>{lhs} → {' | '.join([' '.join(rhs) for rhs in rhs_list])}</code>
                </div>
            """, unsafe_allow_html=True)
      
    with st.expander("📚 Lihat Vocabulary Bahasa Bali", expanded=False):
        st.markdown("""
            <h3 style='color: #1E3A8A; margin-bottom: 1rem;'>Aturan-aturan Tata Bahasa</h3>
        """, unsafe_allow_html=True)
        for lhs in vocab_keys:
            rhs_list = RULES_CFG.get(lhs, [])
            st.markdown(f"""
                <div style='background-color: white; padding: 0.75rem; border-radius: 0.5rem; margin-bottom: 0.5rem;'>
                    <code style='font-size: 1rem;'>{lhs}: {', '.join([' '.join(rhs) for rhs in rhs_list])}</code>
                </div>
            """, unsafe_allow_html=True)
                  
    # Input section with card-like styling
    st.markdown("""
        <h2 style='color: #1E3A8A; margin-top: 2rem; margin-bottom: 1rem;'>Input Kalimat</h2>
    """, unsafe_allow_html=True)
    
    st.markdown("""
        <div style='background-color: #FEF3C7; padding: 1rem; border-radius: 0.5rem; margin-bottom: 1rem;'>
            ⚠️ Pastikan kalimat yang dimasukkan:
            <ul>
                <li>tidak mengandung typo,</li>
                <li>tidak menggunakan tanda baca (kecuali tanda hubung, jika diperlukan).</li>
            </ul>
        </div>
    """, unsafe_allow_html=True)

    sentence = st.text_input("", placeholder="Masukkan kalimat dalam Bahasa Bali...")
    sentence = sentence.lower()
    
    if st.button("Periksa Kalimat"):
        if sentence:
            words = sentence.strip().split()
            
            with st.spinner("🔍 Memproses kalimat..."):
                cnf = convert_to_cnf(remove_unit_productions(remove_epsilon_productions(RULES_CFG)))
                is_valid, parse_table = cyk_algorithm(cnf, words)
                
                # Display parse table with improved styling
                st.markdown("""
                    <h2 style='color: #1E3A8A; margin-top: 2rem; margin-bottom: 1rem; text-align: center;'>Tabel Filling</h2>
                """, unsafe_allow_html=True)
                
                display_table = []
                n = len(words)
                for i in range(n + 1):
                    display_table.append([""] * n)
                display_table[n] = words.copy()
                for i in range(n):
                    for j in range(n - i):
                        display_table[n-1-i][j] = format_cell_content(parse_table[j][j + i])

                df = pd.DataFrame(display_table)
                st.write(df.to_html(index=False, header=False, classes='dataframe'), unsafe_allow_html=True)
                
                def extract_proper_nouns(grammar):
                    proper_nouns = set()
                    for noun_list in grammar.get("PropNoun", []):  # Ambil value dari key "PropNoun"
                        if noun_list and isinstance(noun_list, list):  # Pastikan nilainya adalah list
                            proper_nouns.add(noun_list[0])  # Ambil elemen pertama dari list
                    return proper_nouns

                proper_nouns = extract_proper_nouns(RULES_CFG)

                def format_propnoun(sentence):
                    words = sentence.split()
                    formatted_words = []

                    for word in words:
                        if word in proper_nouns:  # Jika kata ada dalam daftar proper noun
                            formatted_words.append(word.capitalize())  # Ubah huruf pertama menjadi kapital
                        else:
                            formatted_words.append(word)

                    return " ".join(formatted_words)
             
                formatting_sentence = sentence.capitalize()
                formatting_sentence = format_propnoun(formatting_sentence)
                
                if is_valid:
                    st.markdown(f"""
                        <div style='background-color: #DEF7EC; color: #03543F; padding: 1rem; border-radius: 0.5rem; margin: 2rem 0; text-align: center;'>
                            ✅ Kalimat <strong>"{formatting_sentence}."</strong> VALID menurut tata bahasa Bali
                        </div>
                    """, unsafe_allow_html=True)
                    
                    st.markdown("""
                        <h2 class='parse-tree-title'>Pohon Parsing</h2>
                    """, unsafe_allow_html=True)
                    
                    # Wrap the graphviz chart in a centered container
                    st.markdown("<div class='parse-tree-container'>", unsafe_allow_html=True)
                    dot = create_parse_tree(words, parse_table, cnf)
                    st.graphviz_chart(dot)
                    st.markdown("</div>", unsafe_allow_html=True)
                else:
                    st.markdown(f"""
                        <div style='background-color: #FDE2E2; color: #9B1C1C; padding: 1rem; border-radius: 0.5rem; margin: 2rem 0; text-align: center;'>
                            ❌ Kalimat <strong>"{formatting_sentence}."</strong> TIDAK VALID menurut tata bahasa Bali
                        </div>
                    """, unsafe_allow_html=True)
                    
if __name__ == "__main__":
    main()