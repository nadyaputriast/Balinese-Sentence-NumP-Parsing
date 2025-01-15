import graphviz

def create_parse_tree(words, parse_table, grammar):
    """Create parse tree visualization with complete derivation steps."""
    dot = graphviz.Digraph(comment='Parse Tree')
    dot.attr(rankdir='TB')
    node_count = 0

    def add_node(symbol, pos_info=""):
        nonlocal node_count
        node_id = f"node_{node_count}"
        label = f"{symbol} {pos_info}" if pos_info else symbol
        dot.node(node_id, label)
        node_count += 1
        return node_id

    def get_terminal_derivation(word, pos):
        """Get complete derivation chain for a terminal."""
        derivation = []
        for head, bodies in grammar.items():
            for body in bodies:
                if isinstance(body, str) and body.lower() == word.lower():
                    derivation.append(head)
                    for parent_head, parent_bodies in grammar.items():
                        for parent_body in parent_bodies:
                            if isinstance(parent_body, list) and len(parent_body) == 1 and parent_body[0] == head:
                                derivation.append(parent_head)
        return list(reversed(derivation))

    def build_tree(symbol, i, j, parent_id=None):
        """Build tree showing all derivation steps."""
        current_id = add_node(symbol, f"({i+1},{j+1})")
        
        if parent_id:
            dot.edge(parent_id, current_id)

        if i == j:
            derivation = get_terminal_derivation(words[i], i)
            prev_id = current_id
            
            for category in derivation:
                node_id = add_node(category, f"({i+1},{j+1})")
                dot.edge(prev_id, node_id)
                prev_id = node_id
            
            word_id = add_node(words[i])
            dot.edge(prev_id, word_id)
            return

        for k in range(i, j):
            for head, bodies in grammar.items():
                if head != symbol:
                    continue
                for body in bodies:
                    if not isinstance(body, list) or len(body) != 2:
                        continue
                    B, C = body
                    if B in parse_table[i][k] and C in parse_table[k+1][j]:
                        build_tree(B, i, k, current_id)
                        build_tree(C, k+1, j, current_id)
                        return

    if 'K' in parse_table[0][len(words)-1]:
        build_tree('K', 0, len(words)-1)
    
    return dot