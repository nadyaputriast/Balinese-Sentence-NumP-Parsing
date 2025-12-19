"""
Sor Singgih (Register System) Module

This module contains metadata and helper functions for handling
the Balinese language register system (sor singgih), particularly
for numerals (numeralia) and pronouns.

Register levels:
- Kasar/Andap: Low/informal register
- Madia: Middle register
- Alus/Singgih: High/polite register
- Netral: Neutral (usable in all contexts)
"""

# Metadata Sor Singgih untuk Numeralia
NUMERALIA_SOR_SINGGIH = {
    # Basa Kasar/Andap (Low/Informal Register)
    'besik': {'register': 'kasar', 'meaning': '1', 'alus': 'asiki'},
    'siki': {'register': 'kasar', 'meaning': '1', 'alus': 'asiki'},
    'dua': {'register': 'kasar', 'meaning': '2', 'alus': 'kalih'},
    'duang': {'register': 'kasar', 'meaning': '2', 'alus': 'kalih'},
    'dadua': {'register': 'kasar', 'meaning': '2', 'alus': 'kalih'},
    'dadue': {'register': 'kasar', 'meaning': '2', 'alus': 'kalih'},
    'telung': {'register': 'kasar', 'meaning': '3', 'alus': 'tiga'},
    'papat': {'register': 'kasar', 'meaning': '4', 'alus': 'sekawan'},
    'pat': {'register': 'kasar', 'meaning': '4', 'alus': 'sekawan'},
    'limang': {'register': 'kasar', 'meaning': '5', 'alus': 'panca'},
    'lelima': {'register': 'kasar', 'meaning': '5', 'alus': 'panca'},
    'lalima': {'register': 'kasar', 'meaning': '5', 'alus': 'panca'},
    'nem': {'register': 'kasar', 'meaning': '6', 'alus': 'enem'},
    'pitung': {'register': 'kasar', 'meaning': '7', 'alus': 'pitu'},
    'kutus': {'register': 'kasar', 'meaning': '8', 'alus': 'akutus'},
    'sia': {'register': 'kasar', 'meaning': '9', 'alus': 'asanga'},
    'sanga': {'register': 'kasar', 'meaning': '9', 'alus': 'asanga'},
    'dasa': {'register': 'kasar', 'meaning': '10', 'alus': 'adasa'},
    'satus': {'register': 'kasar', 'meaning': '100', 'alus': 'aatus'},
    'atus': {'register': 'kasar', 'meaning': '100', 'alus': 'aatus'},
    'satak': {'register': 'kasar', 'meaning': '100', 'alus': 'aatus'},
    'sewu': {'register': 'kasar', 'meaning': '1000', 'alus': 'asiu'},
    'siu': {'register': 'kasar', 'meaning': '1000', 'alus': 'asiu'},
    
    # Basa Alus/Singgih (High/Polite Register)
    'asiki': {'register': 'alus', 'meaning': '1', 'kasar': 'besik/siki'},
    'kalih': {'register': 'alus', 'meaning': '2', 'kasar': 'duang/dua'},
    'sekawan': {'register': 'alus', 'meaning': '4', 'kasar': 'papat/pat'},
    'panca': {'register': 'alus', 'meaning': '5', 'kasar': 'limang/lima'},
    'enem': {'register': 'alus', 'meaning': '6', 'kasar': 'nem'},
    'akutus': {'register': 'alus', 'meaning': '8', 'kasar': 'kutus'},
    'asanga': {'register': 'alus', 'meaning': '9', 'kasar': 'sanga/sia'},
    'adasa': {'register': 'alus', 'meaning': '10', 'kasar': 'dasa'},
    'aatus': {'register': 'alus', 'meaning': '100', 'kasar': 'satus'},
    'asiu': {'register': 'alus', 'meaning': '1000', 'kasar': 'sewu/siu'},
    
    # Netral (Neutral - usable in all registers)
    'tiga': {'register': 'netral', 'meaning': '3'},
    'tigang': {'register': 'netral', 'meaning': '3'},
    'lima': {'register': 'netral', 'meaning': '5'},
    'pitu': {'register': 'netral', 'meaning': '7'},
    'ulu': {'register': 'netral', 'meaning': '9'},
    'roras': {'register': 'netral', 'meaning': '12'},
    'solas': {'register': 'netral', 'meaning': '13'},
    'telulas': {'register': 'netral', 'meaning': '14'},
    'limolas': {'register': 'netral', 'meaning': '15'},
    'pitulas': {'register': 'netral', 'meaning': '17'},
    'plekutus': {'register': 'netral', 'meaning': '18'},
    'siangolas': {'register': 'netral', 'meaning': '19'},
    'likur': {'register': 'netral', 'meaning': '20'},
    'salikur': {'register': 'netral', 'meaning': '21'},
    'selae': {'register': 'netral', 'meaning': '25'},
    'pasaur': {'register': 'netral', 'meaning': '35'},
    'setiman': {'register': 'netral', 'meaning': '50'},
    'seket': {'register': 'netral', 'meaning': '50'},
    'benang': {'register': 'netral', 'meaning': '80'},
    'karobelah': {'register': 'netral', 'meaning': '200'},
    'lebak': {'register': 'netral', 'meaning': '200'},
    'samas': {'register': 'netral', 'meaning': '400'},
    'domas': {'register': 'netral', 'meaning': '500'},
    'bangsit': {'register': 'netral', 'meaning': '800'},
    'ribuan': {'register': 'netral', 'meaning': 'thousands'},
    'kapertama': {'register': 'netral', 'meaning': 'pertama'},
    'kaping': {'register': 'netral', 'meaning': 'ke-'},
    'adiri': {'register': 'netral', 'meaning': 'sendiri'},
    'aparo': {'register': 'netral', 'meaning': '½'},
    'paro': {'register': 'netral', 'meaning': '½'},
    'ping': {'register': 'netral', 'meaning': 'kali'},
    'alaksa': {'register': 'netral', 'meaning': '100,000'},
    'aketi': {'register': 'netral', 'meaning': '10,000,000'},
    'ayutia': {'register': 'netral', 'meaning': '1,000,000'},
    'abungkul': {'register': 'netral', 'meaning': 'sebungkul'},
    'akatih': {'register': 'netral', 'meaning': 'sekatih'},
    'ayu': {'register': 'netral', 'meaning': 'seayu'},
    'sepaa': {'register': 'netral', 'meaning': 'seperempat'},
}

# Metadata Sor Singgih untuk Pronoun
PRONOUN_SOR_SINGGIH = {
    # Orang Pertama (1st Person)
    'tiang': {'register': 'alus', 'meaning': 'saya', 'person': '1st'},
    'tiange': {'register': 'alus', 'meaning': 'saya', 'person': '1st'},
    'titiang': {'register': 'alus', 'meaning': 'saya (sangat alus)', 'person': '1st'},
    'icang': {'register': 'kasar', 'meaning': 'saya', 'person': '1st'},
    'cang': {'register': 'kasar', 'meaning': 'saya', 'person': '1st'},
    'iang': {'register': 'kasar', 'meaning': 'saya', 'person': '1st'},
    'awakne': {'register': 'kasar', 'meaning': 'saya', 'person': '1st'},
    'dewek': {'register': 'kasar', 'meaning': 'saya', 'person': '1st'},
    'iraga': {'register': 'madia', 'meaning': 'kita/kami', 'person': '1st-plural'},
    'iragane': {'register': 'madia', 'meaning': 'kita/kami', 'person': '1st-plural'},
    
    # Orang Kedua (2nd Person)
    'cai': {'register': 'kasar', 'meaning': 'kamu', 'person': '2nd'},
    'ci': {'register': 'kasar', 'meaning': 'kamu', 'person': '2nd'},
    'iba': {'register': 'kasar', 'meaning': 'kamu', 'person': '2nd'},
    'ragane': {'register': 'madia', 'meaning': 'kamu', 'person': '2nd'},
    'ragan-ragane': {'register': 'madia', 'meaning': 'kamu', 'person': '2nd'},
    'jerone': {'register': 'alus', 'meaning': 'beliau', 'person': '2nd'},
    'ida': {'register': 'alus', 'meaning': 'beliau', 'person': '2nd'},
    'idane': {'register': 'alus', 'meaning': 'beliau', 'person': '2nd'},
    'dane': {'register': 'alus', 'meaning': 'dia/beliau', 'person': '2nd/3rd'},
    'cokor': {'register': 'alus', 'meaning': 'beliau', 'person': '2nd'},
    
    # Orang Ketiga (3rd Person)
    'ia': {'register': 'kasar', 'meaning': 'dia', 'person': '3rd'},
    'ikane': {'register': 'kasar', 'meaning': 'dia', 'person': '3rd'},
    'ipun': {'register': 'alus', 'meaning': 'dia/beliau', 'person': '3rd'},
    'ipune': {'register': 'alus', 'meaning': 'dia/beliau', 'person': '3rd'},
    'ipuna': {'register': 'alus', 'meaning': 'dia/beliau', 'person': '3rd'},
    'ipun-ipun': {'register': 'alus', 'meaning': 'mereka', 'person': '3rd-plural'},
}

# Metadata untuk Classifier (Kata Bantu Bilangan)
CLASSIFIER_METADATA = {
    'diri': {'meaning': 'classifier untuk orang', 'usage': 'manusia'},
    'ekor': {'meaning': 'classifier untuk hewan', 'usage': 'hewan'},
    'ukud': {'meaning': 'classifier untuk hewan (ekor)', 'usage': 'hewan'},
    'pasang': {'meaning': 'classifier untuk berpasangan', 'usage': 'benda berpasangan'},
    'lusin': {'meaning': 'classifier untuk lusin (12)', 'usage': 'satuan komersial'},
    'hektar': {'meaning': 'classifier untuk luas tanah', 'usage': 'tanah'},
    'tingkat': {'meaning': 'classifier untuk tingkat/lantai', 'usage': 'bangunan'},
    'batang': {'meaning': 'classifier untuk benda panjang', 'usage': 'benda panjang'},
}


def get_all_numerals():
    """
    Get all numeral words.
    
    Returns:
        List of all numeral words from NUMERALIA_SOR_SINGGIH
    """
    return list(NUMERALIA_SOR_SINGGIH.keys())


def get_all_pronouns():
    """
    Get all pronoun words.
    
    Returns:
        List of all pronoun words from PRONOUN_SOR_SINGGIH
    """
    return list(PRONOUN_SOR_SINGGIH.keys())


def get_numeral_register(word):
    """
    Get the register level of a numeral.
    
    Args:
        word: The numeral word to check
        
    Returns:
        String: 'kasar', 'alus', 'netral', or None if not found
    """
    return NUMERALIA_SOR_SINGGIH.get(word.lower(), {}).get('register', None)


def get_pronoun_register(word):
    """
    Get the register level of a pronoun.
    
    Args:
        word: The pronoun word to check
        
    Returns:
        String: 'kasar', 'alus', 'madia', or None if not found
    """
    return PRONOUN_SOR_SINGGIH.get(word.lower(), {}).get('register', None)


def is_classifier(word):
    """
    Check if a word is a classifier.
    
    Args:
        word: The word to check
        
    Returns:
        Boolean: True if word is a classifier, False otherwise
    """
    return word.lower() in CLASSIFIER_METADATA


def get_register(word):
    """
    Get register of a word (works for both numerals and pronouns).
    
    Args:
        word: The word to check
        
    Returns:
        String: Register level or None if not found
    """
    word_lower = word.lower()
    
    # Check in numerals
    num_register = get_numeral_register(word_lower)
    if num_register:
        return num_register
    
    # Check in pronouns
    pron_register = get_pronoun_register(word_lower)
    if pron_register:
        return pron_register
    
    return None
