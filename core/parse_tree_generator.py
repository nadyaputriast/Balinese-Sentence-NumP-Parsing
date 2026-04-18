import networkx as nx
import matplotlib
import matplotlib.pyplot as plt
from io import BytesIO

# Wajib untuk Streamlit agar tidak crash saat merender plot di beda thread
matplotlib.use('Agg')

def create_parse_tree(words, parse_table, grammar, backpointers, theme="standard"):
    G = nx.DiGraph()
    node_count = [0]
    pos = {}
    labels = {}
    depth_tracker = [0]  # track max depth

    DISPLAY_LABELS = {
        "X_NP_Conj": "NP+Conj",
        "X_NumP_Conj": "NumP+Conj",
        "X_AdjP_Conj": "AdjP+Conj",
        "X_VP_Conj": "VP+Conj",
        "X_PP_Conj": "PP+Conj",
        "X_K_Conj": "K+Conj",
    }

    def add_node(label, x, y):
        node_id = f"n{node_count[0]}"
        node_count[0] += 1
        G.add_node(node_id)
        pos[node_id] = (x, y)
        labels[node_id] = DISPLAY_LABELS.get(label, label)
        depth_tracker[0] = max(depth_tracker[0], abs(y))
        return node_id

    def build(symbol, i, j, y=0, parent=None, x_left=None, x_right=None):
        n = len(words)
        if x_left is None: x_left = 0.0
        if x_right is None: x_right = float(n - 1)
        
        x = (x_left + x_right) / 2.0

        node_id = add_node(symbol, x, y)
        if parent:
            G.add_edge(parent, node_id)

        if i >= len(backpointers) or j >= len(backpointers[i]) or symbol not in backpointers[i][j]:
            return node_id

        rule_body, split_point = backpointers[i][j][symbol]

        if rule_body[0] == 'terminal':
            leaf_id = add_node(rule_body[1], x, y - 1)
            G.add_edge(node_id, leaf_id)
            return node_id

        if len(rule_body) == 1:
            build(rule_body[0], i, j, y - 1, node_id, x_left, x_right)

        elif len(rule_body) == 2:
            k = split_point
            if k is not None and i <= k < j:
                # Bagi boundary proporsional berdasarkan jumlah kata
                total = j - i
                left_ratio = (k - i + 1) / total
                x_mid = x_left + (x_right - x_left) * left_ratio

                build(rule_body[0], i, k,   y - 1, node_id, x_left, x_mid)
                build(rule_body[1], k+1, j, y - 1, node_id, x_mid, x_right)

        return node_id

    n = len(words)
    try:
        if n > 0 and 'K' in parse_table[0][n-1]:
            build('K', 0, n-1, y=0)
        else:
            add_node('Parse Failed', 0, 0)
    except Exception as e:
        print(f"Error building tree: {e}")
        add_node('Parse Error', 0, 0)

    # Hitung total node dan kedalaman untuk sizing dinamis
    total_nodes = len(G.nodes())
    max_depth = depth_tracker[0]

    # Dynamic sizing — proporsional terhadap kompleksitas tree
    fig_width = max(8, min(n * 2.5, 30))# min 8, max 30
    fig_height = max(6, min(max_depth * 1.8, 20)) # min 6, max 20

    # Dynamic node size — makin banyak node makin kecil
    node_size = max(1200, min(3000, 3000 - total_nodes * 20))

    # Dynamic font size
    font_size = max(7, min(11, 11 - total_nodes // 10))

    fig, ax = plt.subplots(figsize=(fig_width, fig_height))

    # Node colors
    node_colors = []
    for node in G.nodes():
        label = labels[node]
        if label in ['K', 'K1', 'K2']:
            node_colors.append('#10b981')
        elif label in ['S', 'P', 'O', 'Pel', 'Ket']:
            node_colors.append('#6366f1')
        elif label.endswith('P') or '+Conj' in label:
            node_colors.append('#0ea5e9')
        elif label in ['Noun','Verb','Adj','Num','Adv','Prep','Det','Pronoun','PropNoun','Conj']:
            node_colors.append('#f59e0b')
        else:
            node_colors.append('#64748b')

    if len(G.nodes()) > 0:
        nx.draw_networkx_nodes(G, pos, ax=ax, node_size=node_size,
                               node_color=node_colors, edgecolors="#ffffff", linewidths=1.5)
        nx.draw_networkx_edges(G, pos, ax=ax, width=2.0,
                               edge_color="#cbd5e1", arrows=False)
        nx.draw_networkx_labels(G, pos, labels, font_size=font_size,
                                font_weight="bold", font_color="white",
                                font_family="sans-serif", ax=ax)

    ax.axis('off')
    plt.tight_layout()

    buf = BytesIO()
    plt.savefig(buf, format='png', transparent=True, dpi=150, bbox_inches='tight')
    plt.close(fig)
    buf.seek(0)
    return buf