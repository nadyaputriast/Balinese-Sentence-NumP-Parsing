from itertools import combinations

def get_terminals(grammar):
    """Extract all terminal symbols from the grammar."""
    terminals = set()
    for productions in grammar.values():
        for production in productions:
            for symbol in production:
                if symbol not in grammar:
                    terminals.add(symbol)
    return terminals

def remove_epsilon_productions(cfg):
    """Remove epsilon productions from the grammar."""
    nullable = set()
    
    # Find nullable symbols
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
    
    # Generate new rules
    new_cfg = {}
    for head, bodies in cfg.items():
        new_bodies = set()
        for body in bodies:
            if body:  # Skip empty productions
                indices = [i for i, symbol in enumerate(body) if symbol in nullable]
                for r in range(len(indices) + 1):
                    for subset in combinations(indices, r):
                        new_body = tuple(sym for i, sym in enumerate(body) if i not in subset)
                        if new_body:  # Only add non-empty productions
                            new_bodies.add(new_body)
        new_cfg[head] = [list(body) for body in new_bodies]
    return new_cfg

def remove_unit_productions(cfg):
    """Remove unit productions from the grammar."""
    # Get all unit pairs
    unit_pairs = set()
    for head, bodies in cfg.items():
        for body in bodies:
            if len(body) == 1 and body[0] in cfg:
                unit_pairs.add((head, body[0]))
    
    # Add transitive unit pairs
    changed = True
    while changed:
        changed = False
        for a, b in list(unit_pairs):
            for c in [p[1] for p in unit_pairs if p[0] == b]:
                if (a, c) not in unit_pairs:
                    unit_pairs.add((a, c))
                    changed = True
    
    # Create new grammar
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

def remove_useless_productions(cfg):
    """Remove useless productions from the grammar."""
    # Cari simbol yang menghasilkan terminal
    generating = set()
    changed = True
    while changed:
        changed = False
        for head, bodies in cfg.items():
            if head not in generating:
                for body in bodies:
                    if all(symbol in generating or symbol not in cfg for symbol in body):
                        generating.add(head)
                        changed = True
                        break
    
    # Cari simbol yang dapat dijangkau dari simbol awal
    reachable = set()
    to_process = {'S'}  # Asumsikan 'S' adalah simbol awal
    while to_process:
        symbol = to_process.pop()
        reachable.add(symbol)
        if symbol in cfg:
            for body in cfg[symbol]:
                for sym in body:
                    if sym not in reachable and sym in cfg:
                        to_process.add(sym)
    
    # Buang simbol yang tidak berguna
    new_cfg = {head: [] for head in cfg if head in generating and head in reachable}
    for head in new_cfg:
        for body in cfg[head]:
            if all(symbol in generating and symbol in reachable for symbol in body):
                new_cfg[head].append(body)
    
    return new_cfg

def convert_to_binary(cfg):
    """Transform grammar to binary form."""
    new_cfg = {}
    terminal_rules = {}
    counter = 0
    
    for head, bodies in cfg.items():
        new_cfg[head] = []
        for body in bodies:
            new_body = []
            for symbol in body:
                if symbol not in cfg and len(body) > 1:
                    terminal_name = f"T{symbol}"
                    if terminal_name not in terminal_rules:
                        terminal_rules[terminal_name] = [[symbol]]
                    new_body.append(terminal_name)
                else:
                    new_body.append(symbol)
            new_cfg[head].append(new_body)
    
    # Tambahkan aturan terminal ke grammar
    new_cfg.update(terminal_rules)
    
    # Ubah aturan panjang menjadi biner
    final_cfg = {head: [] for head in new_cfg}
    for head, bodies in new_cfg.items():
        for body in bodies:
            if len(body) <= 2:
                final_cfg[head].append(body)
            else:
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

def convert_to_cnf(cfg):
    """Convert grammar to Chomsky Normal Form."""
    cfg = remove_epsilon_productions(cfg)
    cfg = remove_unit_productions(cfg)
    cfg = remove_useless_productions(cfg)
    cfg = convert_to_binary(cfg)
    return cfg