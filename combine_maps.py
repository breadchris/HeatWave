
import sys, os
from capstone import *

cap = Cs(CS_ARCH_X86, CS_MODE_64)
program = sys.argv[1]
elf = open(program, "r").read()
heat_logs = "heat_map_logs"

class HeatHit():
    def __init__(self, branch_addr):
        self.branch_addr = branch_addr
        self.result_addrs = []
        self.count = 0

    def add_result_addr(self, addr):
        if addr not in self.result_addrs:
            self.result_addrs.append(addr)
        self.count += 1

    def __str__(self):
        return "Count: %d, 0x%08x -> 0x%08x" % (self.count, branch_addr, target_addr)

    def __repr__(self):
        return self.__str__()

heat_hits = []
for root, dirs, files in os.walk(heat_logs):
    for file in files:
        trace_hits = open(os.path.join(root, file), "r").readlines()[0]
        trace_hits = eval(trace_hits)
        for hit in trace_hits:
            added_hit = False
            for heat_hit in heat_hits:
                if heat_hit.branch_addr == hit[0]:
                    heat_hit.add_result_addr(hit[1])
            if not added_hit:
                heat = HeatHit(hit[0])
                heat.add_result_addr(hit[1])
                heat_hits.append(heat)

for heat in hits:
    for i in cap.disasm(elf, heat.branch_addr):
        print("0x%x:\t%s\t%s" %(i.address, i.mnemonic, i.op_str))

