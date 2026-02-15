import streamlit as st
import pandas as pd
import plotly.express as px
import miner_logic
import numpy as np

# --- Page Config ---
st.set_page_config(
    page_title="BlockCraft Pro",
    page_icon="🧱",
    layout="wide",
    initial_sidebar_state="expanded"
)

# --- Custom Styling (Dark Mode + Bitcoin Theme) ---
st.markdown("""
<style>
    /* Global Background & Font */
    .stApp {
        background-color: #0E1117;
        font-family: 'Inter', sans-serif;
    }
    
    /* Headers */
    h1, h2, h3 {
        color: #F7931A !important;
        font-weight: 700;
    }
    h1 {
        text-shadow: 0px 0px 10px rgba(247, 147, 26, 0.3);
    }
    
    /* Metrics Cards */
    div[data-testid="stMetric"] {
        background-color: #161B22;
        border: 1px solid #30363D;
        padding: 15px;
        border-radius: 10px;
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.3);
    }
    div[data-testid="stMetricLabel"] {
        color: #8B949E;
    }
    div[data-testid="stMetricValue"] {
        color: #E6EDF3;
    }
    
    /* Buttons */
    .stButton>button {
        background: linear-gradient(90deg, #F7931A 0%, #FFB04E 100%);
        color: #000;
        border: none;
        border-radius: 8px;
        font-weight: bold;
        transition: all 0.3s ease;
    }
    .stButton>button:hover {
        transform: scale(1.02);
        box-shadow: 0 0 15px rgba(247, 147, 26, 0.5);
    }
    
    /* Expander */
    .streamlit-expanderHeader {
        background-color: #161B22;
        border-radius: 5px;
    }
</style>
""", unsafe_allow_html=True)

# --- Header ---
col1, col2 = st.columns([1, 6])
with col1:
    st.image("https://upload.wikimedia.org/wikipedia/commons/4/46/Bitcoin.svg", width=80)
with col2:
    st.title("BlockCraft Pro: Strategic Mining Visualizer")
    st.caption("Demonstrating the power of **Child-Pays-For-Parent (CPFP)** logic in Bitcoin mining.")

# --- Session State ---
if 'mempool' not in st.session_state:
    st.session_state.mempool = None
if 'battle_results' not in st.session_state:
    st.session_state.battle_results = None

# --- Sidebar Controls ---
with st.sidebar:
    st.header("⚙️ Mining Setup")
    
    mempool_size = st.slider("Mempool Size (Tx Count)", 500, 5000, 2000, help="Number of transactions to simulate in the mempool.")
    
    if st.button("🔄 Generate New Mempool", type="primary"):
        with st.status("Simulating network activity...", expanded=True) as status:
            st.write("Creating transactions...")
            st.session_state.mempool = miner_logic.generate_mempool(mempool_size)
            st.session_state.battle_results = None
            st.write("Building dependency graphs...")
            status.update(label="Mempool Ready!", state="complete", expanded=False)
            
    st.divider()
    
    st.subheader("🐋 Whale Injection")
    st.info("Simulate a **CPFP** scenario: A high-fee child stuck behind a low-fee parent.")
    
    if st.button("💉 Inject Whale Transaction"):
        if st.session_state.mempool is not None:
            # Create a localized CPFP scenario
            df = st.session_state.mempool
            df['rate'] = df['fee'] / df['weight']
            # Find low fee candidates
            low_fee_candidates = df[df['rate'] < 2.0]
            
            if not low_fee_candidates.empty:
                parent = low_fee_candidates.sample(1).iloc[0]
                parent_id = parent['txid']
            else:
                parent = df.sample(1).iloc[0]
                parent_id = parent['txid']
                
            # Create Whale Child
            whale_tx = {
                "txid": f"WHALE_{np.random.randint(1000,9999)}",
                "fee": 5_000_000, # Massive Fee (5M sats = 0.05 BTC)
                "weight": 5000,
                "parents": parent_id
            }
            
            st.session_state.mempool = pd.concat([df, pd.DataFrame([whale_tx])], ignore_index=True)
            st.session_state.battle_results = None 
            st.toast(f"Whale Injected! Parent: {parent_id[:8]}...", icon="🐋")
        else:
            st.error("Generate mempool first.")
            
    st.divider()
    
    st.subheader("🧹 Dust Filter")
    dust_threshold = st.slider("Filter Dust (< N sats/wu)", 0.0, 5.0, 1.0, 0.1, help="Exclude transactions with very low fee rates.")

# --- Main Dashboard ---

if st.session_state.mempool is not None:
    # Logic: Filter & Display
    df_display = st.session_state.mempool.copy()
    df_display['fee_rate'] = df_display['fee'] / df_display['weight']
    
    df_filtered = df_display[df_display['fee_rate'] >= dust_threshold].copy()
    
    # Top Level Stats
    c1, c2, c3 = st.columns(3)
    c1.metric("Mempool Transactions", f"{len(df_filtered):,}", help="Transactions valid for mining")
    c2.metric("Total Weight", f"{df_filtered['weight'].sum():,} wu")
    c3.metric("Total Potential Fees", f"{df_filtered['fee'].sum()/1e8:.4f} BTC")
    
    st.divider()
    
    if st.button("⚔️ START MINING BATTLE", use_container_width=True):
        with st.spinner("Running Mining Algorithms..."):
            # 1. Naive Greedy
            greedy_txs, greedy_fees, greedy_weight = miner_logic.solve_greedy(df_filtered)
            
            # 2. CPFP Smart
            cpfp_txs, cpfp_fees, cpfp_weight, cpfp_block_df = miner_logic.solve_cpfp(df_filtered)
            
            st.session_state.battle_results = {
                "greedy": {"fees": greedy_fees, "weight": greedy_weight, "count": len(greedy_txs)},
                "cpfp": {"fees": cpfp_fees, "weight": cpfp_weight, "count": len(cpfp_txs), "df": cpfp_block_df}
            }
            
    # --- Results View ---
    if st.session_state.battle_results:
        res = st.session_state.battle_results
        
        st.markdown("### 🏆 Battle Results")
        
        col1, col2 = st.columns(2)
        
        # Naive Column
        with col1:
            st.markdown("#### 🤡 Naive Greedy")
            st.caption("Sorts by individual fee rate. Misses high-fee children.")
            st.metric("Total Fees", f"{res['greedy']['fees']:,} sats")
            st.metric("Block Weight", f"{res['greedy']['weight']:,} wu")
            st.progress(res['greedy']['weight'] / 4000000)
            
        # CPFP Column
        with col2:
            st.markdown("#### 🧠 Smart CPFP")
            st.caption("Mines 'Packages' (Ancestors + Descendants).")
            delta = res['cpfp']['fees'] - res['greedy']['fees']
            
            color = "normal" if delta >= 0 else "inverse"
            st.metric("Total Fees", f"{res['cpfp']['fees']:,} sats", delta=f"+{delta:,} sats", delta_color=color)
            st.metric("Block Weight", f"{res['cpfp']['weight']:,} wu")
            st.progress(res['cpfp']['weight'] / 4000000)

        st.markdown("---")
        
        # --- Visualization ---
        st.subheader("📦 Block Visualization")
        
        tab1, tab2 = st.tabs(["TreeMap (CPFP)", "Profit Comparison"])
        
        with tab1:
            st.caption("Visualizing the *Smart Block*. Transactions grouped by **Family Clusters**. Large Green blocks = High Value.")
            
            block_df = res['cpfp']['df']
            # Hierarchy
            block_df['cluster_id'] = block_df['parents'].apply(lambda x: x.split(';')[0] if x else "Independent Base")
            
            # Better Color Scale
            fig = px.treemap(
                block_df,
                path=[px.Constant("Mined Block"), 'cluster_id', 'txid'],
                values='weight',
                color='fee_rate',
                color_continuous_scale='Spectral_r', # Red to Blue/Green
                range_color=[1, 100], # Cap color scale for better contrast
                title='Transaction Weight vs Fee Rate',
                hover_data={
                    'fee': ':.0f',
                    'weight': ':.0f',
                    'fee_rate': ':.2f',
                    'cluster_id': True,
                    'txid': False
                }
            )
            
            fig.update_layout(
                margin=dict(t=30, l=10, r=10, b=10),
                paper_bgcolor='#0E1117',
                font=dict(color='#E6EDF3'),
                hoverlabel=dict(bgcolor="#161B22", bordercolor="#30363D"),
                coloraxis_colorbar=dict(title="Fee Rate (sats/wu)")
            )
            fig.update_traces(
                marker=dict(line=dict(width=0.5, color='#0E1117')),
                textinfo="label+value"
            )
            
            st.plotly_chart(fig, use_container_width=True)
            
        with tab2:
            chart_data = pd.DataFrame([
                {"Algorithm": "Naive Greedy", "Fees (BTC)": res['greedy']['fees']/1e8},
                {"Algorithm": "Smart CPFP", "Fees (BTC)": res['cpfp']['fees']/1e8}
            ])
            
            bar_fig = px.bar(
                chart_data, 
                x="Algorithm", 
                y="Fees (BTC)", 
                color="Algorithm",
                color_discrete_map={"Naive Greedy": "#EF553B", "Smart CPFP": "#00CC96"},
                text_auto='.4f'
            )
            bar_fig.update_layout(
                paper_bgcolor='#0E1117',
                plot_bgcolor='#0E1117',
                font=dict(color='#E6EDF3'),
                yaxis=dict(showgrid=True, gridcolor='#30363D')
            )
            st.plotly_chart(bar_fig, use_container_width=True)

else:
    st.info("👈 Please **Generate a Mempool** from the sidebar to begin.")
    
    # Placeholder Intro
    st.markdown("""
    ### Welcome to BlockCraft Pro
    
    This tool simulates the internal logic of a Bitcoin Mining Node.
    
    **Why is this hard?**
    - Miners want to maximize fees.
    - Transactions have dependencies (Child depends on Parent).
    - Sometimes a **rich child** is stuck behind a **poor parent**.
    - A Naive miner ignores the poor parent. A Smart miner (CPFP) calculates the **combined** profit.
    
    **Instructions:**
    1. Generate a Mempool.
    2. (Optional) Inject a "Whale" scenario.
    3. Click **Battle Mode** to see who wins.
    """)
