"""
CNF (Chomsky Normal Form) Converter

Converts Context-Free Grammar to Chomsky Normal Form,
which is required for the CYK parsing algorithm.
"""

from itertools import combinations


def get_terminals(grammar):
    """
    Extract all terminal symbols from the grammar.
    
    Args:
        grammar: Dictionary representing the CFG
        
    Returns:
        Set of terminal symbols
    """
    terminals = set()
    for productions in grammar.values():
        for production in productions:
            for symbol in production:
                if symbol not in grammar:
                    terminals.add(symbol)
    return terminals


def remove_epsilon_productions(cfg):
    """
    Remove epsilon (empty) productions from the grammar.
    
    Args:
        cfg: Context-Free Grammar dictionary
        
    Returns:
        Modified grammar without epsilon productions
    """
    nullable = set()
    
    # Find nullable symbols (symbols that can derive empty string)
    changed = True
    while changed:
        changed = False
        for head, bodies in cfg.items():
            if head not in nullable:
                for body in bodies:
                    if len(body) == 0 or all(symbol in nullable for symbol in body):
                        nullable.add(head)
                        changed = True
                        break
    
    # Generate new rules without epsilon productions
    new_cfg = {}
    for head, bodies in cfg.items():
        new_bodies = set()
        for body in bodies:
            if body:  # Skip empty productions
                # Find positions of nullable symbols
                indices = [i for i, symbol in enumerate(body) if symbol in nullable]
                # Generate all combinations of removing nullable symbols
                for r in range(len(indices) + 1):
                    for subset in combinations(indices, r):
                        new_body = tuple(sym for i, sym in enumerate(body) if i not in subset)
                        if new_body:  # Only add non-empty productions
                            new_bodies.add(new_body)
        new_cfg[head] = [list(body) for body in new_bodies]
    
    return new_cfg


def remove_unit_productions(cfg):
    """
    Remove unit productions (A -> B) from the grammar.
    
    Args:
        cfg: Context-Free Grammar dictionary
        
    Returns:
        Modified grammar without unit productions
    """
    # Get all unit pairs (A -> B where B is non-terminal)
    unit_pairs = set()
    for head, bodies in cfg.items():
        for body in bodies:
            if len(body) == 1 and body[0] in cfg:
                unit_pairs.add((head, body[0]))
    
    # Add transitive unit pairs (if A -> B and B -> C, then A -> C)
    changed = True
    while changed:
        changed = False
        for a, b in list(unit_pairs):
            for c in [p[1] for p in unit_pairs if p[0] == b]:
                if (a, c) not in unit_pairs:
                    unit_pairs.add((a, c))
                    changed = True
    
    # Create new grammar without unit productions
    new_cfg = {head: [] for head in cfg}
    for head, bodies in cfg.items():
        # Add non-unit productions
        for body in bodies:
            if len(body) != 1 or (len(body) == 1 and body[0] not in cfg):
                new_cfg[head].append(body)
        
        # Add productions from unit pairs
        for pair in unit_pairs:
            if pair[0] == head:
                for body in cfg[pair[1]]:
                    if len(body) != 1 or (len(body) == 1 and body[0] not in cfg):
                        if body not in new_cfg[head]:
                            new_cfg[head].append(body)
    
    return new_cfg


def convert_to_cnf(cfg):
    """
    Convert grammar to Chomsky Normal Form (CNF).
    
    CNF requires all productions be in one of two forms:
    1. A -> BC (two non-terminals)
    2. A -> a (single terminal)
    
    Args:
        cfg: Context-Free Grammar dictionary
        
    Returns:
        Grammar in Chomsky Normal Form
    """
    # Step 1: Replace terminals in multi-symbol productions
    new_cfg = {}
    terminal_rules = {}
    counter = 0
    
    for head, bodies in cfg.items():
        new_cfg[head] = []
        for body in bodies:
            new_body = []
            for symbol in body:
                if symbol not in cfg and len(body) > 1:
                    # Create new non-terminal for this terminal
                    terminal_name = f"T{symbol}"
                    if terminal_name not in terminal_rules:
                        terminal_rules[terminal_name] = [[symbol]]
                    new_body.append(terminal_name)
                else:
                    new_body.append(symbol)
            new_cfg[head].append(new_body)
    
    # Add terminal rules to grammar
    new_cfg.update(terminal_rules)
    
    # Step 2: Break down long productions (more than 2 symbols)
    final_cfg = {}
    for head in new_cfg:
        final_cfg[head] = []
    
    for head, bodies in new_cfg.items():
        for body in bodies:
            if len(body) <= 2:
                # Already in CNF form
                final_cfg[head].append(body)
            else:
                # Break: A -> B C D becomes A -> B X1, X1 -> C D
                current_head = head
                remaining_body = body[:]
                
                while len(remaining_body) > 2:
                    new_head = f"X{counter}"
                    counter += 1
                    final_cfg[current_head].append([remaining_body[0], new_head])
                    if new_head not in final_cfg:
                        final_cfg[new_head] = []
                    current_head = new_head
                    remaining_body = remaining_body[1:]
                
                final_cfg[current_head].append(remaining_body)
    
    return final_cfg
