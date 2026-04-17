"""
CYK (Cocke-Younger-Kasami) Parsing Algorithm

Bottom-up parsing algorithm that works with grammars in
Chomsky Normal Form using dynamic programming.
"""


def cyk_algorithm(grammar, words):
    """
    Parse a sentence using the CYK algorithm.

    Args:
        grammar: Grammar in CNF format (dictionary)
        words: List of words to parse

    Returns:
        Tuple (is_valid, parse_table, backpointers):
            - is_valid: Boolean indicating if sentence is grammatically valid
            - parse_table: 2D table showing parsing process
            - backpointers: 2D table storing derivation info for tree reconstruction
    """
    n = len(words)
    # Initialize parse table
    cyk_table = [[set() for _ in range(n)] for _ in range(n)]

    # Initialize backpointers table
    # backpointers[i][j][symbol] = (production_body, split_point)
    # production_body: list of symbols (length 1 for unary/terminal, length 2 for binary)
    # split_point: integer split index for binary rules; None for unary/terminal
    backpointers = [[{} for _ in range(n)] for _ in range(n)]

    # Step 1: Fill diagonal with terminal rules (single words)
    for i in range(n):
        word = words[i]
        for head, bodies in grammar.items():
            for body in bodies:
                if len(body) == 1 and body[0] == word:
                    cyk_table[i][i].add(head)
                    backpointers[i][i][head] = (['terminal', word], None)

        # Unary closure
        added = True
        while added:
            added = False
            current_symbols = list(cyk_table[i][i])
            for head, bodies in grammar.items():
                for body in bodies:
                    if len(body) == 1 and body[0] in current_symbols:
                        if head not in cyk_table[i][i]:
                            cyk_table[i][i].add(head)
                            backpointers[i][i][head] = ([body[0]], None)
                            added = True

    # Step 2: Binary rules
    for length in range(2, n + 1):
        for i in range(n - length + 1):
            j = i + length - 1

            # Binary rules
            for k in range(i, j):
                for head, bodies in grammar.items():
                    for body in bodies:
                        if len(body) == 2:
                            B, C = body
                            if B in cyk_table[i][k] and C in cyk_table[k+1][j]:
                                # ✅ PRIORITASKAN BINARY BACKPOINTER
                                if head not in cyk_table[i][j]:
                                    cyk_table[i][j].add(head)
                                    backpointers[i][j][head] = ([B, C], k)
                                else:
                                    # Jika sudah ada, ganti jika yang lama unary (split None)
                                    old_body, old_split = backpointers[i][j][head]
                                    if old_split is None:
                                        backpointers[i][j][head] = ([B, C], k)

            # Unary closure (hanya tambahkan jika belum ada)
            added = True
            while added:
                added = False
                current_symbols = list(cyk_table[i][j])
                for head, bodies in grammar.items():
                    for body in bodies:
                        if len(body) == 1 and body[0] in current_symbols:
                            if head not in cyk_table[i][j]:
                                cyk_table[i][j].add(head)
                                backpointers[i][j][head] = ([body[0]], None)
                                added = True
                            # ❗️ Jangan timpa backpointer biner dengan unary

    is_valid = 'K' in cyk_table[0][n-1]
    return is_valid, cyk_table, backpointers


def format_cell_content(cell_set):
    """Format parse table cell content for display."""
    if not cell_set:
        return "∅"
    return "{" + ", ".join(sorted(cell_set)) + "}"
