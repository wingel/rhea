#
# Copyright (c) 2006-2014 Christopher L. Felton
# See the licence file in the top directory
#

from math import ceil, log
import myhdl
from myhdl import Signal, intbv, always_comb, always

from rhea.system import Signals


@myhdl.block
def fifo_mem_generic(clock_w, write, write_data, write_addr,
                     clock_r, read_data, read_addr):
    """ Memory module used by FIFOs
    The write data takes two `clock_w` clock cycles to be latched 
    into the memory array and one `clock_r` clock cycle to be latched
    into `read_data`.

    Arguments:
       clock_w: write clock
       write: write enable
       write_data: write
       write_addr: write address
       clock_r: read clock
       read_data: read data
       read_addr: read address

    Parameters:
        mem_size (int): number of item entries in the memory.
    """
    
    assert len(write_addr) == len(read_addr)
    addrsize = 2**len(write_addr)
    assert len(write_data) == len(read_data)
    datasize = len(write_data)

    # create the list-of-signals to represent the memory array
    mem = Signals(intbv(0)[datasize:0], addrsize)

    addr_w = Signal(intbv(0)[addrsize:])
    din = Signal(intbv(0)[datasize:])
    dout = Signal(intbv(0)[datasize:])
    wr = Signal(bool(0))

    @always_comb
    def beh_dataout():
        read_data.next = dout

    @always(clock_r.posedge)
    def beh_read():
        dout.next = mem[int(read_addr)]

    @always(clock_w.posedge)
    def beh_write_capture():
        wr.next = write
        addr_w.next = write_addr
        din.next = write_data

    @always(clock_w.posedge)
    def beh_mem():
        if wr:
            mem[int(addr_w)].next = din

    return myhdl.instances()
