#
# Copyright (c) 2006-2014 Christopher L. Felton
# See the licence file in the top directory
#

from math import ceil, log

import myhdl
from myhdl import Signal, modbv, intbv, always_comb, always

from rhea.system import Signals


@myhdl.block
def fifo_mem_generic(clock_w, write, write_data, write_addr,
                     clock_r, read, read_data, read_addr, write_addr_delayed):
    """ Memory module used by FIFOs
    The write data takes two `clock_w` clock cycles to be latched 
    into the memory array and one `clock_r` clock cycle to be latched
    into `read_data`.

    Arguments:
       clock_w: write clock
       write: write enable
       write_data: write data bus
       write_addr: write address bus
       clock_r: read clock
       read_data: read data bus
       read_addr: read address bus
       write_addr_delayed: the write data takes multiple clock cycles
           before it is available in the memory (pipelines before and
           and after the memory array).  This is a delayed version of
           the write_addr that matches the write_data delay.

    Parameters:
        mem_size (int): number of item entries in the memory.
    """
    
    assert len(write_addr) == len(read_addr)
    addrsize = len(write_addr)
    memsize = 2**len(write_addr)
    assert len(write_data) == len(read_data)
    datasize = len(write_data)

    # create the list-of-signals to represent the memory array
    mem = Signals(intbv(0)[datasize:0], memsize)

    addr_w = Signal(modbv(0)[addrsize:])
    addr_wd = Signal(modbv(0)[addrsize:])
    addr_r = Signal(modbv(0)[addrsize:])
    din = Signal(intbv(0)[datasize:])
    dout = Signal(intbv(0)[datasize:])
    wr = Signal(bool(0))

    @always_comb
    def beh_dataout():
        read_data.next = dout

    @always_comb
    def beh_read_next():
        if read:
            addr_r.next = read_addr+1
        else:
            addr_r.next = read_addr

    @always(clock_r.posedge)
    def beh_mem_read():
        # output is registered, this is fifo memory on read assume
        # incrementing to the next address, get the next address
        dout.next = mem[addr_r]

    @always(clock_w.posedge)
    def beh_write_capture():
        # inputs are registered
        wr.next = write
        addr_w.next = write_addr
        din.next = write_data

    @always(clock_w.posedge)
    def beh_mem_write():
        if wr:
            mem[addr_w].next = din

    @always(clock_r.posedge)
    def beh_write_address_delayed():
        addr_wd.next = write_addr
        write_addr_delayed.next = addr_wd

    return myhdl.instances()
