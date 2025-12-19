"""
Report Generator

Generates comprehensive parsing reports with input, CYK table, and parse tree.
Supports HTML and downloadable formats.
"""

import pandas as pd
from datetime import datetime
import base64
from io import BytesIO


def format_cell_content(cell_set):
    """Format parse table cell content for display."""
    if not cell_set:
        return "∅"
    return "{" + ", ".join(sorted(cell_set)) + "}"


def generate_cyk_table_html(words, parse_table, dark_mode=False):
    """
    Generate HTML representation of CYK parse table.
    
    Args:
        words: List of words in the sentence
        parse_table: CYK parse table
        dark_mode: Whether to use dark mode styling
        
    Returns:
        HTML string of the formatted table
    """
    n = len(words)
    display_table = [[""] * n for _ in range(n + 1)]
    display_table[n] = words.copy()
    
    for i in range(n):
        for j in range(n - i):
            display_table[n-1-i][j] = format_cell_content(parse_table[j][j + i])
    
    # Create styled HTML table
    bg_color = "#1e293b" if dark_mode else "#f9fafb"
    border_color = "#334155" if dark_mode else "#e5e7eb"
    text_color = "#e2e8f0" if dark_mode else "#1f2937"
    
    html = f"""
    <table style="width: 100%; border-collapse: collapse; margin: 1rem 0;">
    """
    
    for i, row in enumerate(display_table):
        html += "<tr>"
        for j, cell in enumerate(row):
            if i == n:  # Word row
                html += f"""<td style="padding: 0.75rem; border: 2px solid {border_color}; 
                           text-align: center; background-color: {bg_color}; color: {text_color};
                           font-weight: bold;">{cell}</td>"""
            elif cell:
                html += f"""<td style="padding: 0.75rem; border: 1px solid {border_color}; 
                           text-align: center; background-color: {bg_color}; color: {text_color};">{cell}</td>"""
            else:
                html += f"""<td style="border: none;"></td>"""
        html += "</tr>\n"
    
    html += "</table>"
    return html


def generate_sor_singgih_html(words, sor_singgih_analysis, pronoun_dict, dark_mode=False):
    """
    Generate HTML for sor singgih analysis.
    
    Args:
        words: List of words
        sor_singgih_analysis: Analysis result
        pronoun_dict: Dictionary of pronouns
        dark_mode: Whether to use dark mode
        
    Returns:
        HTML string
    """
    if not (sor_singgih_analysis['numeralia_found'] or sor_singgih_analysis['pronoun_found']):
        return "<p>Tidak ada numeralia yang terdeteksi dalam kalimat ini.</p>"
    
    # Color coding
    colored_words = []
    for i, word in enumerate(words):
        word_lower = word.lower()
        num_info = next((n for n in sor_singgih_analysis['numeralia_found'] if n['position'] == i), None)
        
        if num_info:
            reg = num_info['register']
            if reg == 'kasar':
                color = "#fee2e2" if not dark_mode else "#7f1d1d"
                colored_words.append(f'<span style="background-color: {color}; padding: 2px 6px; border-radius: 4px;">{word}</span>')
            elif reg == 'alus':
                color = "#dbeafe" if not dark_mode else "#1e40af"
                colored_words.append(f'<span style="background-color: {color}; padding: 2px 6px; border-radius: 4px;">{word}</span>')
            else:
                color = "#f3f4f6" if not dark_mode else "#4b5563"
                colored_words.append(f'<span style="background-color: {color}; padding: 2px 6px; border-radius: 4px;">{word}</span>')
        elif word_lower in pronoun_dict:
            reg = pronoun_dict[word_lower]['register']
            if reg == 'kasar':
                color = "#fee2e2" if not dark_mode else "#7f1d1d"
            elif reg == 'alus':
                color = "#dbeafe" if not dark_mode else "#1e40af"
            elif reg == 'madia':
                color = "#fef3c7" if not dark_mode else "#92400e"
            else:
                color = "transparent"
            colored_words.append(f'<span style="background-color: {color}; padding: 2px 6px; border-radius: 4px;">{word}</span>')
        else:
            colored_words.append(word)
    
    html = f"""
    <div style="margin: 1rem 0;">
        <p><strong>Kalimat dengan Color Coding:</strong></p>
        <p style="font-size: 1.1rem; margin: 0.5rem 0;">{' '.join(colored_words)}</p>
        <p style="font-size: 0.85rem;">
            <span style="background-color: #fee2e2; padding: 2px 6px; border-radius: 4px;">Kasar</span>
            <span style="background-color: #dbeafe; padding: 2px 6px; border-radius: 4px;">Alus</span>
            <span style="background-color: #fef3c7; padding: 2px 6px; border-radius: 4px;">Madia</span>
            <span style="background-color: #f3f4f6; padding: 2px 6px; border-radius: 4px;">Netral</span>
        </p>
    </div>
    """
    
    # Numeralia table
    if sor_singgih_analysis['numeralia_found']:
        html += "<p><strong>Numeralia yang ditemukan:</strong></p>"
        html += "<table style='width: 100%; border-collapse: collapse; margin: 1rem 0;'>"
        html += "<tr><th style='border: 1px solid #ddd; padding: 8px;'>Kata</th><th style='border: 1px solid #ddd; padding: 8px;'>Register</th><th style='border: 1px solid #ddd; padding: 8px;'>Arti</th><th style='border: 1px solid #ddd; padding: 8px;'>Alternatif</th></tr>"
        
        for num in sor_singgih_analysis['numeralia_found']:
            alternatives = []
            if 'alus' in num['data']: alternatives.append(f"Alus: {num['data']['alus']}")
            if 'kasar' in num['data']: alternatives.append(f"Kasar: {num['data']['kasar']}")
            
            html += f"<tr><td style='border: 1px solid #ddd; padding: 8px;'>{num['word']}</td>"
            html += f"<td style='border: 1px solid #ddd; padding: 8px;'>{num['register'].upper()}</td>"
            html += f"<td style='border: 1px solid #ddd; padding: 8px;'>{num['data'].get('meaning', '-')}</td>"
            html += f"<td style='border: 1px solid #ddd; padding: 8px;'>{', '.join(alternatives) if alternatives else '-'}</td></tr>"
        
        html += "</table>"
    
    # Consistency
    if sor_singgih_analysis['is_consistent']:
        html += "<div style='background-color: #d1fae5; padding: 1rem; border-radius: 0.5rem; margin: 1rem 0;'>"
        html += "<p>✅ <strong>Konsistensi Sor Singgih: BAIK</strong></p>"
        html += "</div>"
    else:
        for inc in sor_singgih_analysis['inconsistencies']:
            html += f"<div style='background-color: #fef3c7; padding: 1rem; border-radius: 0.5rem; margin: 0.5rem 0;'>"
            html += f"<p>⚠️ <strong>{inc['message']}</strong></p>"
            html += "</div>"
    
    return html


def generate_full_report_html(
    sentence,
    words,
    parse_table,
    is_valid,
    sor_singgih_analysis=None,
    pronoun_dict=None,
    dark_mode=False
):
    """
    Generate complete HTML report for parsing results.
    
    Args:
        sentence: Input sentence
        words: List of words
        parse_table: CYK parse table
        is_valid: Whether sentence is valid
        sor_singgih_analysis: Sor singgih analysis (optional)
        pronoun_dict: Pronoun dictionary (optional)
        dark_mode: Use dark mode styling
        
    Returns:
        Complete HTML report string
    """
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    
    bg_color = "#0f172a" if dark_mode else "#ffffff"
    text_color = "#e2e8f0" if dark_mode else "#1f2937"
    primary_color = "#60a5fa" if dark_mode else "#1e40af"
    
    html = f"""
    <!DOCTYPE html>
    <html lang="id">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>Laporan Parsing - {sentence}</title>
        <style>
            body {{
                font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
                background-color: {bg_color};
                color: {text_color};
                padding: 2rem;
                max-width: 1200px;
                margin: 0 auto;
            }}
            h1, h2, h3 {{
                color: {primary_color};
            }}
            .header {{
                text-align: center;
                border-bottom: 3px solid {primary_color};
                padding-bottom: 1rem;
                margin-bottom: 2rem;
            }}
            .section {{
                margin: 2rem 0;
                padding: 1.5rem;
                background-color: {"#1e293b" if dark_mode else "#f9fafb"};
                border-radius: 0.5rem;
                border: 1px solid {"#334155" if dark_mode else "#e5e7eb"};
            }}
            .valid {{
                background-color: #d1fae5;
                color: #065f46;
                padding: 1rem;
                border-radius: 0.5rem;
                text-align: center;
                font-weight: bold;
                border: 2px solid #10b981;
            }}
            .invalid {{
                background-color: #fee2e2;
                color: #991b1b;
                padding: 1rem;
                border-radius: 0.5rem;
                text-align: center;
                font-weight: bold;
                border: 2px solid #dc2626;
            }}
            .timestamp {{
                text-align: center;
                color: {"#94a3b8" if dark_mode else "#6b7280"};
                font-size: 0.9rem;
                margin-top: 1rem;
            }}
            @media print {{
                body {{ padding: 1rem; }}
                .no-print {{ display: none; }}
            }}
        </style>
    </head>
    <body>
        <div class="header">
            <h1>🏝️ Laporan Parsing Kalimat Bahasa Bali</h1>
            <p class="timestamp">Dibuat: {timestamp}</p>
        </div>
        
        <div class="section">
            <h2>📝 Input Kalimat</h2>
            <p style="font-size: 1.2rem; text-align: center;"><strong>"{sentence.capitalize()}."</strong></p>
            <p>Jumlah kata: <strong>{len(words)}</strong></p>
            <p>Kata-kata: {', '.join(words)}</p>
        </div>
        
        <div class="section">
            <h2>✅ Hasil Validasi</h2>
            <div class="{'valid' if is_valid else 'invalid'}">
                {'✅ KALIMAT VALID' if is_valid else '❌ KALIMAT TIDAK VALID'}
            </div>
        </div>
    """
    
    # Add sor singgih analysis if available
    if sor_singgih_analysis and pronoun_dict:
        html += f"""
        <div class="section">
            <h2>🎭 Analisis Sor Singgih</h2>
            {generate_sor_singgih_html(words, sor_singgih_analysis, pronoun_dict, dark_mode)}
        </div>
        """
    
    # Add CYK table
    html += f"""
        <div class="section">
            <h2>📊 Tabel Filling (CYK Algorithm)</h2>
            <p>Tabel berikut menunjukkan proses parsing bottom-up menggunakan algoritma CYK:</p>
            {generate_cyk_table_html(words, parse_table, dark_mode)}
        </div>
    """
    
    html += """
        <div class="section no-print">
            <p style="text-align: center; color: #6b7280;">
                <small>Laporan ini dibuat oleh Balinese Sentence Parser</small>
            </p>
        </div>
    </body>
    </html>
    """
    
    return html


def generate_download_link(html_content, filename="parsing_report.html"):
    """
    Generate download link for HTML report.
    
    Args:
        html_content: HTML string to download
        filename: Filename for download
        
    Returns:
        Base64 encoded download link
    """
    b64 = base64.b64encode(html_content.encode()).decode()
    return f'<a href="data:text/html;base64,{b64}" download="{filename}" style="text-decoration: none; background-color: #3b82f6; color: white; padding: 0.75rem 1.5rem; border-radius: 0.5rem; display: inline-block; font-weight: bold;">📥 Download Laporan HTML</a>'
