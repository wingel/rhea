
# Copyright (c) 2014 Christopher L. Felton
#

from math import log, fmod, ceil

import pytest

import myhdl
from myhdl import Signal, intbv, modbv, always_comb, always_seq

from rhea.system import Signals, FIFOBus
from .fifo_mem import fifo_mem_generic


@myhdl.block
def fifo_sync(clock, reset, fbus, size=128):
    """ Synchronous FIFO
    This block is a basic synchronous FIFO.  In many cases it is
    better to use the `fifo_fast` synchronous FIFO (lower resources).
    
    This FIFO uses a "read acknowledge", the read data is available
    on the read data bus before the read strobe is active.  When the
    read signal is set it is acknowledging the data has been read
    and the next FIFO item will be available on the bus.

    Arguments:
        clock: system clock
        reset: system reset
        fbus (FIFOBus): FIFO bus interface

    Example write and read timing:
    
        clock:           /-\_/-\_/-\_/-\_/-\_/-\_/-\_/-\_/-\_/-\_
        fbus.write:      _/---\_______/-----------\___________
        fbus.wrtie_data: -|D1 |-------|D2 |D3 |D4 |
        fbus.read:       _____________/---\__
        fbus.read_data:           |D1    |
        fbus.empty:      ---------\______/--

    Example usage:
        fifobus = FIFOBus(width=16)
        fifo_inst = fifo_sync(glbl, fbus, size=128)
        
    """

    fifosize = size

    if fmod(log(fifosize, 2), 1) != 0:
        asz = int(ceil(log(fifosize, 2)))
        fifosize = 2**asz
        print("@W: fifo_sync only supports power of 2 size")
        print("    forcing size (depth) to %d instread of %d" % (fifosize, fbus.size))

    wptr = Signal(modbv(0, min=0, max=fifosize))
    rptr = Signal(modbv(0, min=0, max=fifosize))
    vld = Signal(False)

    # generic memory model, this memory uses two registers on 
    # the input and one on the output, it takes three clock 
    # cycles for write data to appear on the read.
    fifomem_inst = fifo_mem_generic(
        clock, fbus.write, fbus.write_data, wptr,
        clock, fbus.read_data, rptr,
    )

    # @todo: almost full and almost empty flags
    read = fbus.read
    write = fbus.write
    # takes 3 clock cycles for the write data to be available 
    # on the read port.
    empty1, empty2 = Signal(bool(1)), Signal(bool(1))
    wptr1, wptr2 = Signals(modbv(0, min=0, max=fifosize), 2)

    @always_seq(clock.posedge, reset=reset)
    def beh_fifo():
        # empty is delayed one on writes, in some cases 
        # this default is overwritten below.
        empty2.next = empty1
        fbus.empty.next = empty2

        if fbus.clear:
            wptr.next = 0
            wptr1.next = 0
            wptr2.next = 0
            rptr.next = 0
            fbus.full.next = False
            fbus.empty.next = True
            # empty1.next = True
            # empty2.next = True

        elif read and not write:
            fbus.full.next = False
            if not fbus.empty:
                rptr.next = rptr + 1

        elif write and not read:
            empty1.next = False
            if not fbus.full:
                wptr.next = wptr + 1

        elif write and read:
            wptr.next = wptr + 1
            rptr.next = rptr + 1

        if rptr == (wptr2-1):
            # empty1.next = True
            # empty2.next = True
            fbus.empty.next = True

        if wptr2 == (rptr-1):
            fbus.full.next = True
            

        wptr1.next = wptr
        wptr2.next = wptr1


    @always_comb
    def beh_assign():
        fbus.read_valid.next = fbus.read and not fbus.empty
                
    # @todo: add an option to remove counters
    #        the counters add extra checks and will assert
    #        (fail in simulation) if a write occurs when 
    #        full, some applications are ok with dropping 
    #        data on full writes or empty reads, in those 
    #        rare cases provide a means to disable the 
    #        counters.
    nvacant = Signal(intbv(fifosize, min=-0, max=fifosize+1))  
    ntenant = Signal(intbv(0, min=-0, max=fifosize+1))  
    
    @always_seq(clock.posedge, reset=reset)
    def dbg_occupancy():
        if fbus.clear:
            nvacant.next = fifosize   # the number of empty slots
            ntenant.next = 0          # the number of full slots
        else:
            v = int(nvacant)
            f = int(ntenant)
            
            if fbus.read_valid:
                v = v + 1
                f = f - 1
            if fbus.write:
                v = v -1 
                f = f + 1

            nvacant.next = v
            ntenant.next = f

    # the FIFOBus count references the local signal
    fbus.count = ntenant

    # @todo: will need to replace myhdl.instances with the
    #        conditional collection of inst/gens (see above)
    return myhdl.instances()


# attached a generic fifo bus object to the module
fifo_sync.fbus_intf = FIFOBus