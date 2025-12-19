import pandas as pd
import streamlit as st
from core import cyk_algorithm, convert_to_cnf, remove_epsilon_productions, remove_unit_productions
from grammar import RULES_CFG

def process_csv(uploaded_file):
    try:
        df = pd.read_csv(uploaded_file)
        if "kalimat" not in df.columns:
            return None, "File CSV harus memiliki kolom bernama 'kalimat'"
        
        # Prepare Grammar once
        cfg_cleaned = remove_epsilon_productions(RULES_CFG)
        cfg_cleaned = remove_unit_productions(cfg_cleaned)
        cnf_grammar = convert_to_cnf(cfg_cleaned)
        
        results = []
        progress_bar = st.progress(0)
        
        for i, row in df.iterrows():
            sentence = str(row['kalimat']).lower()
            # Bersihkan tanda baca sederhana
            sentence = sentence.replace(".", "").replace(",", "").replace("?", "").strip()
            words = sentence.split()
            
            is_valid, _ = cyk_algorithm(cnf_grammar, words)
            results.append("VALID" if is_valid else "INVALID")
            progress_bar.progress((i + 1) / len(df))
            
        df['status'] = results
        return df, None
        
    except Exception as e:
        return None, str(e)