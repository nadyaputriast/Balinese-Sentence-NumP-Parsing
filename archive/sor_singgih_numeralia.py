from cfg_grammar import (
    NUMERALIA_SOR_SINGGIH,
    PRONOUN_SOR_SINGGIH,
    CLASSIFIER_METADATA,
    get_numeral_register,
    get_pronoun_register,
    is_classifier
)

NOUN_CATEGORY = {
    'human': ['guru', 'dosen', 'anak', 'sisya', 'balian', 'polisi', 'dokter', 'pianak', 'bapa', 'meme', 'tiang', 'ragane'],
    'animal': ['siap', 'bebek', 'celeng', 'macan', 'kucit', 'sampi', 'kambing', 'cicing'],
    'object': ['buku', 'baju', 'sepatu', 'meja', 'kursi', 'motor', 'mobil', 'umah'],
    'plant': ['punyan', 'bunga', 'don'],
    'fruit': ['biu', 'poh', 'nyuh', 'semangka']
}

CLASSIFIER_RULES = {
    'diri': ['human'],
    'ukud': ['animal'],
    'ekor': ['animal'],
    'bungkul': ['fruit', 'object'],
    'bidang': ['land'],
    'katih': ['object'], # benda panjang
    'pasang': ['object', 'human'] # benda berpasangan
}

# Re-export untuk backward compatibility
SOR_SINGGIH_NUMERALIA = NUMERALIA_SOR_SINGGIH
PRONOUN_REGISTER = PRONOUN_SOR_SINGGIH

def get_register(word):
    """
    Dapatkan register dari sebuah kata (numeralia atau pronoun).
    Returns: 'kasar', 'alus', 'madia', 'netral', atau None jika tidak ditemukan.
    """
    word_lower = word.lower()
    
    # Check numeralia
    num_register = get_numeral_register(word_lower)
    if num_register:
        return num_register
    
    # Check pronoun
    pron_register = get_pronoun_register(word_lower)
    if pron_register:
        return pron_register
    
    return None

def check_numeralia_consistency(words):
    """
    Cek konsistensi register numeralia dalam sebuah kalimat.
    Returns: {
        'is_consistent': bool,
        'numeralia_found': list,
        'pronoun_found': list,
        'registers_found': list,
        'inconsistencies': list,
        'suggestions': list
    }
    """
    numeralia_found = []
    pronoun_found = []
    
    # Scan kata-kata
    for i, word in enumerate(words):
        word_lower = word.lower()
        
        # Check numeralia
        if word_lower in NUMERALIA_SOR_SINGGIH:
            numeralia_found.append({
                'word': word,
                'position': i,
                'register': NUMERALIA_SOR_SINGGIH[word_lower]['register'],
                'data': NUMERALIA_SOR_SINGGIH[word_lower]
            })
        
        # Check pronoun
        if word_lower in PRONOUN_SOR_SINGGIH:
            pronoun_found.append({
                'word': word,
                'position': i,
                'register': PRONOUN_SOR_SINGGIH[word_lower]['register'],
                'data': PRONOUN_SOR_SINGGIH[word_lower]
            })
    
    # Analisis konsistensi
    registers = [n['register'] for n in numeralia_found if n['register'] != 'netral']
    pronoun_registers = [p['register'] for p in pronoun_found]
    
    inconsistencies = []
    suggestions = []
    
    # Rule 1: Jangan mixing kasar dan alus dalam numeralia
    if 'kasar' in registers and 'alus' in registers:
        inconsistencies.append({
            'type': 'numeralia_mixing',
            'message': 'Mixing numeralia kasar dan alus dalam satu kalimat',
            'severity': 'high'
        })
        
        # Generate suggestion
        if len([r for r in registers if r == 'kasar']) > len([r for r in registers if r == 'alus']):
            suggestions.append('Ubah semua numeralia menjadi basa kasar untuk konsistensi')
        else:
            suggestions.append('Ubah semua numeralia menjadi basa alus untuk konsistensi')
    
    # Rule 2: Cek kesesuaian pronoun dengan numeralia
    if pronoun_registers and registers:
        # Jika pronoun alus tapi numeralia kasar
        if 'alus' in pronoun_registers and 'kasar' in registers:
            inconsistencies.append({
                'type': 'pronoun_numeralia_mismatch',
                'message': 'Pronoun menggunakan basa alus tapi numeralia menggunakan basa kasar',
                'severity': 'medium'
            })
            suggestions.append('Sesuaikan register numeralia dengan pronoun (gunakan numeralia alus)')
        
        # Jika pronoun kasar tapi numeralia alus
        if 'kasar' in pronoun_registers and 'alus' in registers:
            inconsistencies.append({
                'type': 'pronoun_numeralia_mismatch',
                'message': 'Pronoun menggunakan basa kasar tapi numeralia menggunakan basa alus',
                'severity': 'low'
            })
    
    is_consistent = len(inconsistencies) == 0
    
    return {
        'is_consistent': is_consistent,
        'numeralia_found': numeralia_found,
        'pronoun_found': pronoun_found,
        'registers_found': list(set(registers)),
        'inconsistencies': inconsistencies,
        'suggestions': suggestions
    }

def get_alternative(word):
    """
    Dapatkan alternatif kata dengan register berbeda.
    """
    word_lower = word.lower()
    
    if word_lower in NUMERALIA_SOR_SINGGIH:
        data = NUMERALIA_SOR_SINGGIH[word_lower]
        alternatives = {}
        
        if 'alus' in data:
            alternatives['alus'] = data['alus']
        if 'kasar' in data:
            alternatives['kasar'] = data['kasar']
        
        return alternatives
    
    return {}

def format_suggestion(words, analysis):
    """
    Generate formatted suggestion untuk perbaikan.
    """
    if analysis['is_consistent']:
        return None
    
    suggestions = []
    
    # Untuk setiap numeralia yang bermasalah, berikan alternatif
    registers_found = analysis['registers_found']
    
    if 'kasar' in registers_found and 'alus' in registers_found:
        # Buat 2 versi: semua kasar dan semua alus
        words_kasar = words.copy()
        words_alus = words.copy()
        
        for num in analysis['numeralia_found']:
            if num['register'] != 'netral':
                alternatives = get_alternative(num['word'])
                
                if num['register'] == 'alus' and 'kasar' in alternatives:
                    words_kasar[num['position']] = alternatives['kasar'].split('/')[0]
                elif num['register'] == 'kasar' and 'alus' in alternatives:
                    words_alus[num['position']] = alternatives['alus']
        
        suggestions.append({
            'version': 'Versi Basa Kasar',
            'sentence': ' '.join(words_kasar)
        })
        suggestions.append({
            'version': 'Versi Basa Alus',
            'sentence': ' '.join(words_alus)
        })
    
    return suggestions

def validate_classifier_usage(numeral, classifier, noun=None):
    """
    Validasi apakah classifier cocok dengan noun.
    
    Args:
        numeral: kata numeralia
        classifier: kata classifier (diri, ekor, pasang, dll)
        noun: kata benda (optional)
    
    Returns:
        dict dengan validation result
    """
    if not is_classifier(classifier):
        return {
            'valid': False,
            'message': f"'{classifier}' bukan classifier yang valid"
        }
    
    classifier_info = CLASSIFIER_METADATA.get(classifier.lower(), {})
    
    # Jika ada noun, validasi kesesuaian
    if noun:
        usage = classifier_info.get('usage', '')
        
        # Simple validation (bisa diperluas)
        if classifier.lower() in ['diri'] and noun.lower() in ['sepatu', 'buku', 'motor']:
            return {
                'valid': False,
                'message': f"Classifier 'diri' untuk manusia, tidak cocok dengan '{noun}'",
                'suggestion': f"Gunakan classifier lain seperti 'pasang' (untuk {noun})"
            }
        
        if classifier.lower() in ['ekor', 'ukud'] and noun.lower() not in ['siap', 'celeng', 'macan', 'bebek']:
            return {
                'valid': False,
                'message': f"Classifier 'ekor/ukud' untuk hewan, tidak cocok dengan '{noun}'",
                'suggestion': f"Gunakan classifier yang sesuai untuk '{noun}'"
            }
    
    return {
        'valid': True,
        'message': f"Penggunaan classifier '{classifier}' sudah tepat",
        'info': classifier_info
    }