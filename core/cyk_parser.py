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
        Tuple (is_valid, parse_table):
            - is_valid: Boolean indicating if sentence is grammatically valid
            - parse_table: 2D table showing parsing process
    """
    n = len(words)
    # Initialize parse table
    # cyk_table[i][j] contains non-terminals that can derive words[i..j]
    cyk_table = [[set() for j in range(n)] for i in range(n)]
    
    # Step 1: Fill diagonal with terminal rules (single words)
    for i in range(n):
        word = words[i]
        for head, bodies in grammar.items():
            for body in bodies:
                if len(body) == 1 and body[0] == word:
                    cyk_table[i][i].add(head)
    
    # Step 2: Fill remaining cells using binary rules
    # Process by increasing substring length
    for length in range(2, n + 1):  # Length of substring
        for i in range(n - length + 1):  # Starting position
            j = i + length - 1  # Ending position
            
            # Try all possible split points
            for k in range(i, j):
                # Check all binary rules A -> B C
                for head, bodies in grammar.items():
                    for body in bodies:
                        if len(body) == 2:
                            B, C = body
                            # If B derives words[i..k] and C derives words[k+1..j]
                            # Then head can derive words[i..j]
                            if B in cyk_table[i][k] and C in cyk_table[k+1][j]:
                                cyk_table[i][j].add(head)
    
    # Check if start symbol 'K' (Kalimat) is in top-right cell
    is_valid = 'K' in cyk_table[0][n-1]
    
    return is_valid, cyk_table


def format_cell_content(cell_set):
    """
    Format parse table cell content for display.
    
    Args:
        cell_set: Set of non-terminals in a cell
        
    Returns:
        Formatted string representation
    """
    if not cell_set:
        return "∅"  # Empty set symbol
    return "{" + ", ".join(sorted(cell_set)) + "}"
