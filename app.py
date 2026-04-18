import streamlit as st
import pandas as pd
from simulator import MemorySimulator

st.title("TLB Performance Analyzer")

# Inputs
page_size = st.number_input("Page Size", value=256)
num_pages = st.number_input("Number of Pages", value=256)
num_frames = st.number_input("Number of Frames", value=128)
tlb_size = st.number_input("TLB Size", value=16)
num_accesses = st.number_input("Number of Memory Accesses", value=1000)
 # i was using here to run the simulation to perform the calculation and graphing the results using streamlit.

if st.button("Run Simulation"):

    sim = MemorySimulator(page_size, num_pages, num_frames)
    sim.tlb_size = tlb_size

    for _ in range(num_accesses):
        va = sim.generate_virtual_address()
        sim.translate_address(va)

    total_accesses = sim.tlb_hits + sim.tlb_misses
    hit_rate = sim.tlb_hits / total_accesses
    miss_rate = sim.tlb_misses / total_accesses

    TLB_TIME = 10
    MEMORY_TIME = 100

    emat = (hit_rate * (TLB_TIME + MEMORY_TIME)) + \
           ((1 - hit_rate) * (TLB_TIME + 2 * MEMORY_TIME))

    # 🔹 Results
    st.subheader("Results")
    st.write(f"Total Accesses: {total_accesses}")
    st.write(f"TLB Hits: {sim.tlb_hits}")
    st.write(f"TLB Misses: {sim.tlb_misses}")
    st.write(f"Hit Rate: {hit_rate:.2f}")
    st.write(f"Miss Rate: {miss_rate:.2f}")
    st.write(f"EMAT: {emat:.2f} ns")

    # 🔥 Graph Section
    data = {
        "Metric": ["Hit Rate", "Miss Rate"],
        "Value": [hit_rate, miss_rate]
    }

    df = pd.DataFrame(data)

    st.subheader("Performance Graph")
    st.bar_chart(df.set_index("Metric"))