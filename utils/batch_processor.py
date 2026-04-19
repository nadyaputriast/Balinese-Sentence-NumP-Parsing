import pandas as pd
import streamlit as st
from core import cyk_algorithm, convert_to_cnf, remove_epsilon_productions, remove_unit_productions
from grammar import RULES_CFG

def process_csv(uploaded_file):
    try:
        df = pd.read_csv(uploaded_file, sep='\t')
        df.columns = df.columns.str.strip()
        
        if "kalimat" not in df.columns:
            return None, "File CSV harus memiliki kolom bernama 'kalimat'"
        
        df['kalimat_utuh'] = df.apply(lambda row: ' '.join(row.dropna().astype(str)), axis=1)
        
        # Prepare Grammar once
        cfg_cleaned = remove_epsilon_productions(RULES_CFG)
        cfg_cleaned = remove_unit_productions(cfg_cleaned)
        cnf_grammar = convert_to_cnf(cfg_cleaned)
        
        results = []
        progress_bar = st.progress(0)
        
        for i, row in df.iterrows():
            sentence = str(row['kalimat_utuh']).lower()
            
            # Bersihkan tanda baca sederhana
            sentence = sentence.replace(".", "").replace(",", "").replace("?", "").strip()
            words = sentence.split()
            
            # Pengecekan jika ternyata barisnya kosong setelah dibersihkan
            if not words:
                results.append("INVALID")
            else:
                is_valid, _, _ = cyk_algorithm(cnf_grammar, words)
                results.append("VALID" if is_valid else "INVALID")
                
            progress_bar.progress((i + 1) / len(df))
            
        df['status'] = results
        
        df_final = df[['kalimat_utuh', 'status']].rename(columns={'kalimat_utuh': 'kalimat'})
        
        return df_final, None
        
    except Exception as e:
        return None, str(e)