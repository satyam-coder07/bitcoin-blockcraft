import pandas as pd
import numpy as np
import random
import secrets
import networkx as nx

MAX_BLOCK_WEIGHT = 4_000_000

def generate_mempool(n=2000):
    """
    Generates a mempool with specific 'God Tier' scenarios:
    - Normal transactions.
    - 'Family Clusters': Low-fee parent -> High-fee child (CPFP bait).
    """
    data = []
    txids = [secrets.token_hex(32) for _ in range(n)]
    
    # 1. create a mapping for fast lookups if needed, or just iterate
    # We will build data row by row
    
    for i, txid in enumerate(txids):
        # Default random values
        weight = int(np.random.gamma(shape=2, scale=200)) # Skewed distribution for realistic sizes
        weight = max(200, min(weight, 400000)) # Clamp
        
        # Scenario: "Family Cluster" (10% chance)
        # We manually force a parent-child relationship for CPFP demonstration
        is_child = False
        parents = []
        
        # If we are in the last 90% of txs, we can pick a parent from the first 10%
        # to ensure the parent appears "earlier" or just pick any existing
        if i > 50 and random.random() < 0.10: 
            # This is a Child. Let's find a Parent.
            # Pick a recent previous tx to be the parent
            parent_idx = i - random.randint(1, 20)
            parent_txid = txids[parent_idx]
            parents = [parent_txid]
            is_child = True
            
            # Crucial: Make Child High Fee, ensure Parent was Low Fee?
            # actually we can't easily modify the *already created* parent's fee here without a map.
            # detailed approach below.
        
        # Better approach: Generate base stats, then link and adjust fees.
        pass

    # RESTART generation with better structure
    data = []
    
    # We'll create objects first
    tx_objects = []
    for _ in range(n):
        tx_objects.append({
            "txid": secrets.token_hex(32),
            "weight": max(200, int(np.random.gamma(2, 200))),
            "fee": 0, # Placeholder
            "parents": [],
            "is_cpfp_child": False
        })
        
    # Now link and assign fees
    for i, tx in enumerate(tx_objects):
        # 5% chance to be a "Whale Child" (CPFP scenario)
        if i > 0 and random.random() < 0.05:
            # Pick a parent
            parent = tx_objects[i - random.randint(1, min(i, 50))]
            tx["parents"] = [parent["txid"]]
            tx["is_cpfp_child"] = True
            
            # Scenario: Parent is Low Fee (Dust-ish), Child is Massive Fee
            # Modify PARENT
            parent["fee"] = int(parent["weight"] * 1.0) # 1 sat/wu (Low)
            # Modify CHILD
            tx["fee"] = int(tx["weight"] * 50.0) # 50 sat/wu (Huge)
        else:
            # Normal random fee
            # Log-normal distribution for fees looks realistic
            fee_rate = np.random.lognormal(mean=2, sigma=1) # geometric mean ~7 sat/wu
            tx["fee"] = int(tx["weight"] * fee_rate)
            
    # Convert to DataFrame
    final_data = []
    for tx in tx_objects:
        final_data.append({
            "txid": tx["txid"],
            "fee": tx["fee"],
            "weight": tx["weight"],
            "parents": ";".join(tx["parents"])
        })
        
    return pd.DataFrame(final_data)

def build_graph(df):
    G = nx.DiGraph()
    # Create lookup
    tx_map = {row.txid: row for row in df.itertuples()}
    
    for row in df.itertuples():
        G.add_node(row.txid, fee=row.fee, weight=row.weight)
        if pd.notna(row.parents) and row.parents:
            for p in row.parents.split(';'):
                if p in tx_map:
                    G.add_edge(p, row.txid) # Parent -> Child
    return G

def solve_greedy(df):
    """
    Naive Miner: Sorts by Fee Rate. 
    Problem: Fails to mine high-fee children if their low-fee parents are far down the list.
    Realistically, a miner can't mine a child without the parent.
    So a Naive Miner iterates the sorted list:
    - If Parent is already mined -> Mine Child.
    - If Parent NOT mined -> SKIP Child (Lost Opportunity!).
    """
    df = df.copy()
    df['fee_rate'] = df['fee'] / df['weight']
    # Sort descending by fee rate
    df_sorted = df.sort_values('fee_rate', ascending=False)
    
    mined_txs = set()
    total_fee = 0
    total_weight = 0
    block_txs = []
    
    # Fast lookup for parents
    # We need to check if parents are in 'mined_txs'
    # But we need O(1) parent lookup.
    tx_parents = {row.txid: set(row.parents.split(';')) if row.parents else set() for row in df.itertuples()}
    # Filter empty strings from parents
    tx_parents = {k: {p for p in v if p} for k, v in tx_parents.items()}

    for row in df_sorted.itertuples():
        if total_weight + row.weight > MAX_BLOCK_WEIGHT:
            continue
            
        # Check dependencies
        parents = tx_parents[row.txid]
        if parents.issubset(mined_txs):
            # Safe to mine
            mined_txs.add(row.txid)
            block_txs.append(row.txid)
            total_fee += row.fee
            total_weight += row.weight
        else:
            # Naive miner SKIPS this high value transaction because parents aren't ready
            # This is where CPFP beats Greedy
            pass
            
    return block_txs, total_fee, total_weight

def solve_cpfp(df):
    """
    Smart Miner: Calculates 'Effective Fee Rate' of (Tx + Ancestors).
    """
    G = build_graph(df)
    
    mined_txs = set()
    total_fee = 0
    total_weight = 0
    block_txs = []
    
    # We simulate the pool. 
    # Valid candidates are nodes with in_degree 0 (parents mined) relative to current pool?
    # No, CPFP looks at "Packages".
    # Approach: 
    # Calculate best implementation of "Ancestor Set Mining"
    
    # Copy graph to be destructive
    pool_G = G.copy()
    
    while total_weight < MAX_BLOCK_WEIGHT:
        # Find best candidate package
        # Optimized for demo:
        # Iterate all nodes. Calculate (Self + Unmined Ancestors) stats.
        
        candidates = []
        nodes = list(pool_G.nodes())
        
        if not nodes:
            break
            
        # Optimization: Just look at a random sample or top fee-rate nodes if N is huge?
        # N=2000 is small enough for full scan? 
        # N=2000, calculating ancestors for each is O(N*Depth). 
        # Depth is small (1-2 parents). 
        # Should be fast.
        
        best_package = None
        best_rate = -1
        
        for tx in nodes:
            ancestors = nx.ancestors(pool_G, tx) | {tx}
            
            pkg_fee = sum(pool_G.nodes[a]['fee'] for a in ancestors)
            pkg_weight = sum(pool_G.nodes[a]['weight'] for a in ancestors)
            
            if total_weight + pkg_weight > MAX_BLOCK_WEIGHT:
                continue
                
            rate = pkg_fee / pkg_weight
            if rate > best_rate:
                best_rate = rate
                best_package = ancestors
        
        if not best_package:
            break
            
        # Mine the package
        # Topological sort to ensure order
        sorted_pkg = list(nx.topological_sort(pool_G.subgraph(best_package)))
        
        for tx in sorted_pkg:
            mined_txs.add(tx)
            block_txs.append(tx)
            total_fee += pool_G.nodes[tx]['fee']
            total_weight += pool_G.nodes[tx]['weight']
            pool_G.remove_node(tx)
            
    return block_txs, total_fee, total_weight, df[df['txid'].isin(mined_txs)].copy()
