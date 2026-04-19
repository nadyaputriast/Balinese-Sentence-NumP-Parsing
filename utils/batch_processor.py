import pandas as pd
import streamlit as st
import unicodedata
from core import cyk_algorithm, convert_to_cnf, remove_epsilon_productions, remove_unit_productions
from grammar import RULES_CFG
from utils import stats_manager

def process_file(uploaded_file, kamus_dasar, stemmer_func):
    try:
        nama_file = uploaded_file.name.lower()
        
        if nama_file.endswith('.csv'):
            df = pd.read_csv(uploaded_file, sep='\t') 
        elif nama_file.endswith('.xlsx') or nama_file.endswith('.xls'):
            df = pd.read_excel(uploaded_file)
        else:
            return None, "Format file tidak didukung. Harap upload CSV atau Excel."

        df.columns = df.columns.str.strip()
        
        if "kalimat" not in df.columns:
            return None, "File harus memiliki kolom bernama 'kalimat'"
        
        df['kalimat_utuh'] = df.apply(lambda row: ' '.join(row.dropna().astype(str)), axis=1)
        
        # Prepare Grammar once
        cfg_cleaned = remove_epsilon_productions(RULES_CFG)
        cfg_cleaned = remove_unit_productions(cfg_cleaned)
        cnf_grammar = convert_to_cnf(cfg_cleaned)
        
        results = []
        batch_stats_data = []
        progress_bar = st.progress(0)
        
        for i, row in df.iterrows():
            sentence_raw = str(row['kalimat_utuh']).lower().strip()
            sentence_normalized = unicodedata.normalize('NFKD', sentence_raw).encode('ASCII', 'ignore').decode('utf-8')
            sentence_final, _ = stemmer_func(sentence_normalized, kamus_dasar)
            
            words = sentence_final.split()
            
            if not words:
                results.append("INVALID")
            else:
                is_valid, _, _ = cyk_algorithm(cnf_grammar, words)
                results.append("VALID" if is_valid else "INVALID")
                
            progress_bar.progress((i + 1) / len(df))
            
        df['status'] = results
        df_final = df[['kalimat_utuh', 'status']].rename(columns={'kalimat_utuh': 'kalimat'})
        
        stats_manager.update_stats_batch(batch_stats_data)
        
        return df_final, None
        
    except Exception as e:
        return None, str(e)