"""
Sor Singgih Consistency Checker

This module provides functions to check and validate the consistency
of register usage (sor singgih) in Balinese sentences, particularly
for numerals and pronouns.
"""

from .sor_singgih import (
    NUMERALIA_SOR_SINGGIH,
    PRONOUN_SOR_SINGGIH,
    CLASSIFIER_METADATA,
    get_numeral_register,
    get_pronoun_register,
    is_classifier,
    get_register
)

# Noun categories for classifier validation
NOUN_CATEGORY = {
    'human': ['guru', 'dosen', 'anak', 'sisya', 'balian', 'polisi', 'dokter', 
              'pianak', 'bapa', 'meme', 'tiang', 'ragane'],
    'animal': ['siap', 'bebek', 'celeng', 'macan', 'kucit', 'sampi', 'kambing', 'cicing'],
    'object': ['buku', 'baju', 'sepatu', 'meja', 'kursi', 'motor', 'mobil', 'umah'],
    'plant': ['punyan', 'bunga', 'don'],
    'fruit': ['biu', 'poh', 'nyuh', 'semangka']
}

# Classifier usage rules
CLASSIFIER_RULES = {
    'diri': ['human'],
    'ukud': ['animal'],
    'ekor': ['animal'],
    'bungkul': ['fruit', 'object'],
    'bidang': ['land'],
    'katih': ['object'],  # benda panjang
    'pasang': ['object', 'human']  # benda berpasangan
}

# Re-export untuk backward compatibility
SOR_SINGGIH_NUMERALIA = NUMERALIA_SOR_SINGGIH
PRONOUN_REGISTER = PRONOUN_SOR_SINGGIH


def check_numeralia_consistency(words):
    """
    Check consistency of register usage in numerals within a sentence.
    
    Args:
        words: List of words in the sentence
        
    Returns:
        Dict containing:
            - is_consistent: Boolean
            - numeralia_found: List of found numerals with metadata
            - pronoun_found: List of found pronouns with metadata
            - registers_found: List of unique registers used
            - inconsistencies: List of inconsistency details
            - suggestions: List of suggestions for fixing inconsistencies
    """
    numeralia_found = []
    pronoun_found = []
    
    # Scan words for numerals and pronouns
    for i, word in enumerate(words):
        word_lower = word.lower()
        
        # Check if word is a numeral
        if word_lower in NUMERALIA_SOR_SINGGIH:
            numeralia_found.append({
                'word': word,
                'position': i,
                'register': NUMERALIA_SOR_SINGGIH[word_lower]['register'],
                'data': NUMERALIA_SOR_SINGGIH[word_lower]
            })
        
        # Check if word is a pronoun
        if word_lower in PRONOUN_SOR_SINGGIH:
            pronoun_found.append({
                'word': word,
                'position': i,
                'register': PRONOUN_SOR_SINGGIH[word_lower]['register'],
                'data': PRONOUN_SOR_SINGGIH[word_lower]
            })
    
    # Analyze consistency
    registers = [n['register'] for n in numeralia_found if n['register'] != 'netral']
    pronoun_registers = [p['register'] for p in pronoun_found]
    
    inconsistencies = []
    suggestions = []
    
    # Rule 1: Don't mix kasar and alus numerals in one sentence
    if 'kasar' in registers and 'alus' in registers:
        inconsistencies.append({
            'type': 'numeralia_mixing',
            'message': 'Mixing numeralia kasar dan alus dalam satu kalimat',
            'severity': 'high'
        })
        
        # Generate suggestion based on majority
        if len([r for r in registers if r == 'kasar']) > len([r for r in registers if r == 'alus']):
            suggestions.append('Ubah semua numeralia menjadi basa kasar untuk konsistensi')
        else:
            suggestions.append('Ubah semua numeralia menjadi basa alus untuk konsistensi')
    
    # Rule 2: Check pronoun-numeral register agreement
    if pronoun_registers and registers:
        # If pronoun is alus but numeral is kasar
        if 'alus' in pronoun_registers and 'kasar' in registers:
            inconsistencies.append({
                'type': 'pronoun_numeralia_mismatch',
                'message': 'Pronoun menggunakan basa alus tapi numeralia menggunakan basa kasar',
                'severity': 'medium'
            })
            suggestions.append('Sesuaikan register numeralia dengan pronoun (gunakan numeralia alus)')
        
        # If pronoun is kasar but numeral is alus
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
    Get alternative forms of a word in different registers.
    
    Args:
        word: The word to find alternatives for
        
    Returns:
        Dict with alternative forms (e.g., {'alus': 'asiki', 'kasar': 'besik'})
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
    Generate formatted suggestions for fixing register inconsistencies.
    
    Args:
        words: List of words in the sentence
        analysis: Analysis result from check_numeralia_consistency
        
    Returns:
        List of suggestion dicts with version name and corrected sentence
    """
    if analysis['is_consistent']:
        return None
    
    suggestions = []
    registers_found = analysis['registers_found']
    
    # If mixing kasar and alus, create both versions
    if 'kasar' in registers_found and 'alus' in registers_found:
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
    Validate if a classifier is appropriate for the given noun.
    
    Args:
        numeral: The numeral word
        classifier: The classifier word (diri, ekor, pasang, dll)
        noun: The noun word (optional)
    
    Returns:
        Dict with validation result and message
    """
    if not is_classifier(classifier):
        return {
            'valid': False,
            'message': f"'{classifier}' bukan classifier yang valid"
        }
    
    classifier_info = CLASSIFIER_METADATA.get(classifier.lower(), {})
    
    # If noun is provided, validate appropriateness
    if noun:
        usage = classifier_info.get('usage', '')
        
        # Simple validation (can be expanded)
        if classifier.lower() == 'diri' and noun.lower() in ['sepatu', 'buku', 'motor']:
            return {
                'valid': False,
                'message': f"Classifier 'diri' untuk manusia, tidak cocok dengan '{noun}'"
            }
        
        if classifier.lower() in ['ekor', 'ukud'] and noun.lower() not in NOUN_CATEGORY.get('animal', []):
            return {
                'valid': False,
                'message': f"Classifier '{classifier}' untuk hewan, tidak cocok dengan '{noun}'"
            }
    
    return {
        'valid': True,
        'message': f"Classifier '{classifier}' valid",
        'info': classifier_info
    }
