import json
import os
import streamlit as st
import pandas as pd
import plotly.express as px

STATS_FILE = "usage_stats.json"

def load_stats():
    if not os.path.exists(STATS_FILE):
        return {"total_parsed": 0, "valid": 0, "invalid": 0, "history": []}
    try:
        with open(STATS_FILE, "r") as f:
            return json.load(f)
    except:
        return {"total_parsed": 0, "valid": 0, "invalid": 0, "history": []}

def update_stats(is_valid, sentence):
    stats = load_stats()
    stats["total_parsed"] += 1
    if is_valid:
        stats["valid"] += 1
    else:
        stats["invalid"] += 1
    
    # Simpan history singkat (max 50 terakhir)
    stats["history"].append({"sentence": sentence, "valid": is_valid})
    if len(stats["history"]) > 50:
        stats["history"].pop(0)
        
    with open(STATS_FILE, "w") as f:
        json.dump(stats, f)

def render_stats_dashboard(dark_mode=False):
    stats = load_stats()
    
    st.markdown("### 📊 Statistik Penggunaan")
    
    c1, c2, c3 = st.columns(3)
    c1.metric("Total Kalimat", stats["total_parsed"])
    c2.metric("Valid ✅", stats["valid"])
    c3.metric("Invalid ❌", stats["invalid"])
    
    # Chart
    if stats["total_parsed"] > 0:
        data = pd.DataFrame({
            "Status": ["Valid", "Invalid"],
            "Jumlah": [stats["valid"], stats["invalid"]]
        })
        fig = px.pie(data, values="Jumlah", names="Status", hole=0.4, 
                     color_discrete_sequence=['#34d399', '#f87171'])
        fig.update_layout(paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)")
        st.plotly_chart(fig, use_container_width=True)
    
    st.markdown("#### 📜 Riwayat Terakhir")
    if stats["history"]:
        df_hist = pd.DataFrame(stats["history"])
        df_hist = df_hist.iloc[::-1] # Reverse order
        st.dataframe(df_hist, use_container_width=True)