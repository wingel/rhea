
from random import randint

import myhdl
from myhdl import Signal, intbv, instance, delay
from myhdl.conversion import verify

from rhea.system import Signals
from rhea.cores.fifo.fifo_mem import fifo_mem


@myhdl.block
def bench_conversion_fifomem():
    nloops = 100
    w = width = 8
    wmax = 2 ** width

    # random data and addresses for test
    rand_data = tuple([randint(0, wmax - 1) for _ in range(nloops)])
    rand_addr = tuple([randint(0, wmax - 1) for _ in range(nloops)])

    clock, write, read = Signals(bool(0), 3)
    write_data, write_addr, read_data, read_addr = Signals(intbv(0)[w:0], 4)
    wad = Signal(write_data.val)

    tbdut = fifo_mem(clock, write, write_data, write_addr,
                     clock, read, read_data, read_addr, wad)

    @instance
    def tbclkw():
        clock.next = False
        while True:
            clock.next = not clock
            yield delay(5)

    @instance
    def tbstim():
        print("start sim")
        yield delay(10)

        for ii in range(nloops):
            write.next = True
            write_data.next = rand_data[ii]
            write_addr.next = rand_addr[ii]
            read_addr.next = wad
            yield clock.posedge
            write.next = False
            for jj in range(3):
                print("%d %d %d %d" % (
                    write_addr, write_data, read_addr, read_data))
                yield clock.posedge

        write.next = True
        for ii in range(nloops):
            write_data.next = rand_data[ii]
            write_addr.next = rand_addr[ii]
            read_addr.next = rand_addr[ii]
            yield clock.posedge
            print("%d %d %d %d" % (
                write_addr, write_data, read_addr, read_data))
        write.next = True
        yield clock.posedge

        print("end sim")

    return myhdl.instances()


def test_fifomem_conversion_verilog():
    verify.simulator = 'iverilog'
    inst = bench_conversion_fifomem()
    inst.convert(hdl='Verilog', directory=None)
    assert inst.verify_convert() == 0


def test_fifomem_conversion_vhdl():
    verify.simulator = 'ghdl'
    inst = bench_conversion_fifomem()
    inst.convert(hdl='VHDL', directory=None)
    assert inst.verify_convert() == 0


