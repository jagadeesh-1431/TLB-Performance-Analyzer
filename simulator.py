import random

class MemorySimulator:
    def __init__(self, page_size, num_pages, num_frames):
        self.page_size = page_size
        self.num_pages = num_pages
        self.num_frames = num_frames

        # Page Table (simple mapping)
        self.page_table = [i % num_frames for i in range(num_pages)]

        # TLB
        self.tlb_size = 16
        self.tlb = []

        self.tlb_hits = 0
        self.tlb_misses = 0

    # 🔥 Locality-based address generation
    def generate_virtual_address(self):
        base = random.randint(0, 50)
        return base * self.page_size + random.randint(0, self.page_size - 1)

    def get_page_number(self, virtual_address):
        return virtual_address // self.page_size

    def get_offset(self, virtual_address):
        return virtual_address % self.page_size

    def search_tlb(self, page_number):
        for page, frame in self.tlb:
            if page == page_number:
                return frame
        return -1

    def update_tlb(self, page_number, frame_number):
        if len(self.tlb) >= self.tlb_size:
            self.tlb.pop(0)  # FIFO removal
        self.tlb.append((page_number, frame_number))

    def translate_address(self, virtual_address):
        page_number = self.get_page_number(virtual_address)
        offset = self.get_offset(virtual_address)

        frame_number = self.search_tlb(page_number)

        if frame_number != -1:
            self.tlb_hits += 1
            status = "TLB HIT"
        else:
            self.tlb_misses += 1
            frame_number = self.page_table[page_number]
            self.update_tlb(page_number, frame_number)
            status = "TLB MISS"

        physical_address = frame_number * self.page_size + offset
        return page_number, frame_number, offset, physical_address, status
