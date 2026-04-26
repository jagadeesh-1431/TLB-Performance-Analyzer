import streamlit as st
import pandas as pd
import plotly.express as px
from simulator import MemorySimulator

# Page Configuration
st.set_page_config(
    page_title="TLB Performance Analyzer",
    page_icon=" ",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for Premium Look
st.markdown("""
    <style>
    .main {
        background-color: #0e1117;
    }
    .stButton>button {
        width: 100%;
        border-radius: 8px;
        height: 3em;
        background: linear-gradient(90deg, #ff4b4b 0%, #ff8a8a 100%);
        color: white;
        font-weight: bold;
        border: none;
        transition: 0.3s;
        box-shadow: 0 4px 15px rgba(255, 75, 75, 0.3);
    }
    .stButton>button:hover {
        background: linear-gradient(90deg, #ff2b2b 0%, #ff6b6b 100%);
        transform: translateY(-2px);
        box-shadow: 0 6px 20px rgba(255, 75, 75, 0.4);
        border: none;
        color: white;
    }
    div[data-testid="stMetricValue"] {
        font-size: 2rem;
        font-weight: 700;
        color: #00CC96;
    }
    div[data-testid="stMetricDelta"] {
        font-size: 1rem;
    }
    .reportview-container .main .block-container {
        padding-top: 2rem;
    }
    </style>
    """, unsafe_allow_html=True)

st.title(" TLB Performance Analyzer")
st.markdown("Analyze and simulate Translation Lookaside Buffer performance in real-time with high-precision metrics.")

# Sidebar Inputs
with st.sidebar:
    st.header("⚙️ Simulation Settings")
    st.info("Adjust the parameters below to simulate different memory architectures.")
    
    page_size = st.number_input("Page Size (Bytes)", value=256, step=64, help="Size of each memory page.")
    num_pages = st.number_input("Number of Pages", value=256, step=64, help="Total number of virtual pages.")
    num_frames = st.number_input("Number of Frames", value=128, step=32, help="Total number of physical memory frames.")
    tlb_size = st.number_input("TLB Size (Entries)", value=16, step=4, help="Number of entries the TLB can hold.")
    num_accesses = st.number_input("Memory Accesses", value=1000, step=100, help="Total number of memory requests to simulate.")
    
    st.divider()
    run_sim = st.button(" Run Simulation")
    st.caption("Simulation uses FIFO replacement policy and locality-aware address generation.")

# Simulation Logic
if run_sim:
    sim = MemorySimulator(page_size, num_pages, num_frames)
    sim.tlb_size = tlb_size

    # Simulation Progress
    progress_bar = st.progress(0)
    # Using a placeholder for status updates
    status_text = st.empty()
    
    for i in range(num_accesses):
        va = sim.generate_virtual_address()
        sim.translate_address(va)
        if i % max(1, (num_accesses // 20)) == 0:
            progress_bar.progress(i / num_accesses)
            status_text.text(f"Processing access {i}/{num_accesses}...")
            
    progress_bar.progress(100)
    status_text.text("Simulation Complete!")

    total_accesses = sim.tlb_hits + sim.tlb_misses
    hit_rate = sim.tlb_hits / total_accesses
    miss_rate = sim.tlb_misses / total_accesses

    # Performance Constants
    TLB_TIME = 10
    MEMORY_TIME = 100

    emat = (hit_rate * (TLB_TIME + MEMORY_TIME)) + \
           ((1 - hit_rate) * (TLB_TIME + 2 * MEMORY_TIME))

    # 🔹 Results Display
    st.subheader("📊 Performance Analytics")
    
    m_col1, m_col2, m_col3, m_col4 = st.columns(4)
    with m_col1:
        st.metric("Total Accesses", f"{total_accesses:,}")
    with m_col2:
        st.metric("TLB Hits", f"{sim.tlb_hits:,}", f"{hit_rate:.1%}")
    with m_col3:
        st.metric("TLB Misses", f"{sim.tlb_misses:,}", f"-{miss_rate:.1%}", delta_color="inverse")
    with m_col4:
        st.metric("EMAT", f"{emat:.2f} ns", delta=f"{emat - 110:.2f} ns", delta_color="inverse", help="Effective Memory Access Time. Lower is better.")

    st.divider()

    # 🔥 Visualizations
    viz_col1, viz_col2 = st.columns([1, 1])

    with viz_col1:
        st.subheader("🎯 Hit vs Miss Distribution")
        fig_pie = px.pie(
            names=["Hits", "Misses"],
            values=[sim.tlb_hits, sim.tlb_misses],
            hole=0.5,
            color_discrete_sequence=["#00CC96", "#EF553B"],
            template="plotly_dark"
        )
        fig_pie.update_layout(
            showlegend=True, 
            margin=dict(t=0, b=0, l=0, r=0),
            paper_bgcolor='rgba(0,0,0,0)', 
            plot_bgcolor='rgba(0,0,0,0)'
        )
        st.plotly_chart(fig_pie, use_container_width=True)

    with viz_col2:
        st.subheader("📈 Performance Breakdown")
        data = {
            "Metric": ["Hit Rate", "Miss Rate"],
            "Percentage": [hit_rate * 100, miss_rate * 100]
        }
        df = pd.DataFrame(data)
        fig_bar = px.bar(
            df, x="Metric", y="Percentage",
            color="Metric",
            color_discrete_map={"Hit Rate": "#00CC96", "Miss Rate": "#EF553B"},
            text_auto=".1f",
            template="plotly_dark"
        )
        fig_bar.update_layout(
            yaxis_title="Percentage (%)",
            showlegend=False,
            margin=dict(t=0, b=0, l=0, r=0),
            paper_bgcolor='rgba(0,0,0,0)', 
            plot_bgcolor='rgba(0,0,0,0)'
        )
        st.plotly_chart(fig_bar, use_container_width=True)

    st.success(f"Simulation completed with a hit rate of {hit_rate:.2%}")
else:
    # Initial state
    st.info("👈 Configure the simulation parameters in the sidebar and click 'Run Simulation' to see the results.")
    
    # Adding some educational context
    with st.expander("What is TLB?"):
        st.write("""
            A **Translation Lookaside Buffer (TLB)** is a hardware cache used to speed up virtual-to-physical address translation. 
            When a program accesses memory, the CPU first checks the TLB. 
            - **TLB Hit**: The translation is found in the cache, saving a slow trip to main memory (Page Table).
            - **TLB Miss**: The translation must be fetched from the Page Table in RAM, which takes significantly more time.
        """)