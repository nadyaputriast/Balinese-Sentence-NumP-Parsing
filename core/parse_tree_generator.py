import graphviz

def create_parse_tree(words, parse_table, grammar, backpointers, theme="standard"):
    dot = graphviz.Digraph(comment='Parse Tree')
    dot.attr(rankdir='TB')
    dot.attr('node', shape='rect', fontname="Helvetica", style='solid', color='black')
    dot.attr('edge', color='black')

    node_count = 0

    def add_node(symbol, is_terminal=False):
        nonlocal node_count
        node_id = f"node_{node_count}"
        node_count += 1
        if is_terminal:
            dot.node(node_id, symbol, style='filled', fillcolor='#f1f5f9', fontname='Consolas')
        else:
            dot.node(node_id, symbol)
        return node_id

    def build_tree(symbol, i, j, parent_id=None):
        current_id = add_node(symbol, is_terminal=False)
        if parent_id:
            dot.edge(parent_id, current_id)

        if symbol not in backpointers[i][j]:
            if i == j:
                word_id = add_node(words[i], is_terminal=True)
                dot.edge(current_id, word_id)
            return current_id

        rule_body, split_point = backpointers[i][j][symbol]

        if len(rule_body) == 2 and rule_body[0] == 'terminal':
            word = rule_body[1]
            word_id = add_node(word, is_terminal=True)
            dot.edge(current_id, word_id)
        elif len(rule_body) == 1:
            B = rule_body[0]
            build_tree(B, i, j, current_id)
        elif len(rule_body) == 2:
            B, C = rule_body
            k = split_point
            build_tree(B, i, k, current_id)
            build_tree(C, k+1, j, current_id)

        return current_id

    n = len(words)
    if 'K' in parse_table[0][n-1]:
        build_tree('K', 0, n-1)
    else:
        error_id = add_node("Parse Failed", is_terminal=False)
        dot.node(error_id, "Parse Failed", style='filled', fillcolor='#fee2e2', color='#dc2626')

    return dot