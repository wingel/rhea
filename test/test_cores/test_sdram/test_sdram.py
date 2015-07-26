
from __future__ import division
from __future__ import print_function

import sys
import os
import argparse
from argparse import Namespace
from array import array
from random import randint

import pytest

from myhdl import *

# resuse some of the interfaces
import rhea
from rhea.system import Clock
from rhea.system import Reset
from rhea.system import Global
from rhea.system import Wishbone

from rhea.cores.sdram import SDRAMInterface
from rhea.cores.sdram import sdram_sdr_controller
from rhea.models.sdram import SDRAMModel
from rhea.models.sdram import sdram_controller_model


@pytest.mark.xfail
def test_sdram(args):
    
    clock = Clock(0, frequency=50e6)
    reset = Reset(0, active=0, async=False)

    # interfaces to the modules
    glbl = Global(clock=clock, reset=reset)
    ixbus = Wishbone(glbl=glbl, data_width=32, address_width=32)
    exbus = SDRAMInterface(clock)

    # Models
    sdram = SDRAMModel(exbus)   # model driven by model :)

    max_addr = 2048   # @todo: add actual SDRAM memory size limit
    max_data = 2**32  # @todo: add actual databus width

    def _test_stim():
        """
        This test exercises a SDRAM controller ...
        """

        tbmdl_sdm = sdram.process()
        tbmdl_ctl = sdram_controller_model(exbus, ixbus)

        # test currently only exercises the models, insert a second
        # SDRAMInterface to test an actual controller
        #tbdut = sdram_sdr_controller(ibus, exbus)
        tbclk = clock.gen(hticks=10000)

        @instance
        def tbstim():
            reset.next = reset.active
            yield delay(18000)
            reset.next = not reset.active

            # test a bunch of random addresses
            try:
                for ii in range(10):
                    addr = randint(0, max_addr)
                    data = randint(0, max_data)
                    print("invoke internal bus write {:08X} -> {:08X}".format(addr, data))
                    yield ixbus.write(addr, data)
                    print("invoke internal bus read  {:08X} -> {:08X}".format(addr, data))
                    yield ixbus.read(addr)
                    print("check read data")
                    read_data = ixbus.get_read_data()
                    print(read_data, data)
                    assert read_data == data, "{:08X} != {:08X}".format(read_data, data)

                for ii in range(10):
                    yield delay(1000)

            except AssertionError as err:
                # if test check fails about let the simulation run more cycles,
                # useful for debug
                yield delay(20000)
                raise err

            raise StopSimulation

        return tbclk, tbstim, tbmdl_sdm, tbmdl_ctl

    if os.path.isfile('vcd/_test.vcd'):
        os.remove('vcd/_test.vcd')

    traceSignals.timescale = '1ps'
    traceSignals.name = 'vcd/_test'
    Simulation(traceSignals(_test_stim)).run()


if __name__ == '__main__':
    test_sdram(Namespace())
