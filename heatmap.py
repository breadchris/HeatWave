import pin, sys, atexit, os
from time import gmtime, strftime

main_called = False
start_addr = 0
end_addr = 0
addr_map = []
directory = "heat_map_logs"
log_file = strftime("%Y_%m_%d_%H_%M_%S.heat", gmtime())
get_next_instruction = False
branch_addr = 0

if not os.path.exists(directory):
    os.makedirs(directory)

def log(s):
    print "[pin] " + s

def write_to_log(s):
    log_file.write(s)

def finish():
    log("Throwing the straight fuego into a log file")
    f = open(os.path.join(directory, log_file), "w")
    f.write(str(addr_map))
    f.close()

def gen_call_graph(ins_object):
    global main_called, start_addr, end_addr
    global addr_map, get_next_instruction
    global branch_addr

    if get_next_instruction:
        address = int(pin.INS_Address(ins_object))
        if address > start_addr and address < end_addr:
            log(" [target] 0x%08x: %s" % (address, pin.INS_Disassemble(ins_object)))
            addr_map.append((branch_addr, address))
        get_next_instruction = False

    if pin.INS_IsDirectBranch(ins_object):
        address = int(pin.INS_Address(ins_object))
        if address > start_addr and address < end_addr:
            log(" [branch] 0x%08x: %s" % (address, pin.INS_Disassemble(ins_object)))
            branch_addr = address
            get_next_instruction = True

def load_img(img_object):
    global start_addr, end_addr
    if pin.IMG_IsMainExecutable(img_object):
        start_addr = int(pin.IMG_LowAddress(img_object))
        end_addr = int(pin.IMG_HighAddress(img_object))
        log(hex(start_addr))

pin.INS_AddInstrumentFunction(gen_call_graph)
pin.IMG_AddInstrumentFunction(load_img)
pin.AddFiniFunction(finish, 0)
