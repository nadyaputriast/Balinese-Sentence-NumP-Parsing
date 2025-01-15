def cyk_algorithm(grammar, words):
    n = len(words)
    # Initialize parse table
    cyk_table = [[set() for j in range(n)] for i in range(n)]
    
    # Fill terminal rules
    for i in range(n):
        word = words[i]
        for head, bodies in grammar.items():
            for body in bodies:
                if len(body) == 1 and body[0] == word:
                    cyk_table[i][i].add(head)
    
    # Fill in parse table
    for length in range(2, n + 1):
        for i in range(n - length + 1):
            j = i + length - 1
            for k in range(i, j):
                for head, bodies in grammar.items():
                    for body in bodies:
                        if len(body) == 2:
                            B, C = body
                            if B in cyk_table[i][k] and C in cyk_table[k+1][j]:
                                cyk_table[i][j].add(head)
    return 'K' in cyk_table[0][n-1], cyk_table

def format_cell_content(cell_set):
    """Format the cell content for display."""
    if not cell_set:
        return "∅"
    return "{" + ", ".join(sorted(cell_set)) + "}"