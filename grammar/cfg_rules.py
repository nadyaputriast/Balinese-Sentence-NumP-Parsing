import json
import os
import sys

# 1. Path Configuration and Loader Lexicon
def get_lexicon_path():
    """Giving the absolute path to the lexicon file, which is located in the parent directory's 'scraping' folder."""
    base_dir = os.path.dirname(os.path.abspath(__file__))
    return os.path.join(base_dir, "..", "scraping", "balinese_lexicon.json")

def load_lexicon():
    """
    Reads the JSON file and returns a dictionary of terminal rules.
    Result format: {'Noun': [['word1'], ['word2']], ...}
    """
    json_path = get_lexicon_path()
    try:
        with open(json_path, "r", encoding="utf-8") as f:
            data = json.load(f)
    except FileNotFoundError:
        sys.stderr.write(f"ERROR: Lexicon file is not found at {json_path}\n")
        return {}
    except json.JSONDecodeError as e:
        sys.stderr.write(f"ERROR: JSON format invalid: {e}\n")
        return {}

    # List of Categorical Lexicon that use in CFG
    lexical_categories = [
        "PropNoun", "Pronoun", "Adv", "Det", "Noun",
        "Num", "V", "Prep", "Adj", "Conj"
    ]

    rules = {}
    for cat in lexical_categories:
        if cat in data:
            # For each Balinese word (key), convert it into a single-element list
            rules[cat] = [[word] for word in data[cat].keys()]
        else:
            sys.stderr.write(f"WARNING: Category '{cat}' is not found in the JSON file.\n")
            rules[cat] = []
    return rules

# 2. Syntax Rules: Non-Terminal Rules (Kategori Sintaksis)
SYNTAX_RULES = {
    "K":  [["K1"], ["K1", "K2"], ["K1", "Pel"], ["K1", "Ket"], ["X_K_Conj", "K"]],
    "K1": [["S", "P"]],
    "K2": [["Pel", "Ket"]],
    "S":  [["NP"]],
    "P":  [["NumP"]],
    "Pel": [["AdjP"], ["VP"]],
    "Ket": [["PP"]],
    "NP": [
        ["Noun"], ["NumP", "NP"], ["NP", "NP"],
        ["NP", "PropNoun"], ["NP", "Pronoun"],
        ["Pronoun"], ["PropNoun"],
        ["Adv", "NP"], ["NP", "Det"], ["Det", "NP"],
        ["NP", "AdjP"], ["NP", "Adv"],
        ["X_NP_Conj", "NP"]
    ],
    "NumP": [
        ["Num"], ["NumP", "NP"], ["NumP", "NumP"],
        ["X_NumP_Conj", "NumP"]
    ],
    "AdjP": [
        ["Adj"], ["AdjP", "AdjP"], ["AdjP", "Adv"], ["Adv", "AdjP"],
        ["X_AdjP_Conj", "AdjP"]
    ],
    "VP": [
        ["V"], ["VP", "NP"], ["VP", "AdjP"], ["VP", "NumP"], ["Adv", "VP"],
        ["X_VP_Conj", "VP"]
    ],
    "PP": [
        ["Prep", "NP"], ["Prep", "AdjP"], ["Prep", "NumP"], ["Prep", "Adv"],
        ["X_PP_Conj", "PP"]
    ],

    # Intermediate symbols untuk koordinasi
    "X_NP_Conj": [["NP", "Conj"]],
    "X_NumP_Conj": [["NumP", "Conj"]],
    "X_AdjP_Conj": [["AdjP", "Conj"]],
    "X_VP_Conj": [["VP", "Conj"]],
    "X_PP_Conj": [["PP", "Conj"]],
    "X_K_Conj": [["K", "Conj"]],
}

# 3. Merge and Export
LEXICON_RULES = load_lexicon()

# Merge syntax + lexicon rules into a single dictionary for CFG processing
RULES_CFG = {**SYNTAX_RULES, **LEXICON_RULES}
# 4. Optional: Helper Function for Validation
def validate_cfg():
    """Checks if all lexical categories have at least one entry."""
    missing = [cat for cat, words in LEXICON_RULES.items() if not words]
    if missing:
        sys.stderr.write(f"WARNING: The following categories are empty: {', '.join(missing)}\n")
    else:
        print("✅ CFG is ready for use.")