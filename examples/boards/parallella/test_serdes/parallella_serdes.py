
from __future__ import print_function
from __future__ import division

import argparse
from pprint import pprint

from myhdl import Signal, intbv

from rhea.system import Global, Clock, Reset
from rhea.cores.misc import io_stub
from rhea.cores.comm import prbs_generate
from rhea.cores.comm import prbs_check

from rhea.vendor import Vendor
from rhea.vendor import input_diff_buffer
from rhea.vendor import output_diff_buffer
from rhea.vendor import device_serdes_input
from rhea.vendor import device_serdes_output

from rhea.build import get_board


def parallella_serdes(clock, reset,
                      # porcupine board breakout
                      serial_tx_p, serial_tx_n,
                      serial_rx_p, serial_rx_n,):
    
    nbanks = len(serial_tx_p)
    assert (len(serial_tx_p) == len(serial_tx_n) ==
            len(serial_rx_p) == len(serial_rx_n) )

    glbl = Global(clock, reset)

    # signal interface to the prbs generate / check
    locked = [Signal(bool(0)) for _ in range(nbanks)]
    inject_error = [Signal(bool(0)) for _ in range(nbanks)]
    word_count = [Signal(intbv(0)[64:]) for _ in range(nbanks)]
    error_count = [Signal(intbv(0)[64:]) for _ in range(nbanks)]
    prbsi = [Signal(intbv(0)[1:]) for _ in range(nbanks)]
    prbso = [Signal(intbv(0)[1:]) for _ in range(nbanks)]
    
    insts = []
    for bank in range(nbanks):
        gi = input_diff_buffer(serial_rx_p[bank],
                               serial_rx_n[bank],
                               prbsi[bank])
        go = input_diff_buffer(prbso,
                               serial_tx_p[bank],
                               serial_tx_n[bank])
        
        gg = prbs_generate(glbl, prbso[bank], inject_error[bank],
                           order=23)
        gc = prbs_check(glbl, prbsi[bank], locked[bank],
                        word_count[bank], error_count[bank],
                        order=23)

        for gg in (gi, go, gg, gc):
            insts.append(gg)

    return insts


def build(args):
    # @todo: use parallella board, use an ISE support board for now ...
    brd = get_board('parallella')
    # @todo: temporary for existing board
    brd.add_reset('reset', active=1, async=True, pins=('T15',))
    brd.add_port_name('serial_tx_p', 'gpio_p', slice(0, 6))
    brd.add_port_name('serial_tx_n', 'gpio_p', slice(0, 6))
    brd.add_port_name('serial_rx_p', 'gpio_p', slice(6, 12))
    brd.add_port_name('serial_rx_n', 'gpio_p', slice(6, 12))

    flow = brd.get_flow(parallella_serdes)
    flow.run()
    info = flow.get_utilization()
    pprint(info)

def cliparse():
    parser = argparse.ArgumentParser()
    args = parser.parse_args()
    return args


def main():
    args = cliparse()
    build(args)


if __name__ == '__main__':
    main()
