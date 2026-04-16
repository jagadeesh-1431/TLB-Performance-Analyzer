from simulator import MemorySimulator

# Configuration
PAGE_SIZE = 256
NUM_PAGES = 256
NUM_FRAMES = 128

sim = MemorySimulator(PAGE_SIZE, NUM_PAGES, NUM_FRAMES)

# 🔥 Increase accesses for meaningful results
for i in range(1000):
    va = sim.generate_virtual_address()
    page, frame, offset, pa, status = sim.translate_address(va)

# 🔥 PERFORMANCE CALCULATION
total_accesses = sim.tlb_hits + sim.tlb_misses

hit_rate = sim.tlb_hits / total_accesses
miss_rate = sim.tlb_misses / total_accesses

TLB_TIME = 10
MEMORY_TIME = 100

emat = (hit_rate * (TLB_TIME + MEMORY_TIME)) + \
       ((1 - hit_rate) * (TLB_TIME + 2 * MEMORY_TIME))

# 🔥 FINAL OUTPUT
print("\n===== PERFORMANCE =====")
print(f"Total Accesses: {total_accesses}")
print(f"TLB Hits: {sim.tlb_hits}")
print(f"TLB Misses: {sim.tlb_misses}")
print(f"Hit Rate: {hit_rate:.2f}")
print(f"Miss Rate: {miss_rate:.2f}")
print(f"EMAT: {emat:.2f} ns")