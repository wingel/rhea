#
# Copyright (c) 2006-2014 Christopher L. Felton
#


from myhdl import *

def m_sync_rst(clock, rsti, rsto):
    """
    """
    rsync = [Signal(bool(rsti.active)) for _ in range(2)]

    @always_seq(clock.posedge, reset=rsti)
    def rtl():        
        rsync[0].next = rsti
        rsync[1].next = rsync[0]
        rsto.next = rsync[1]

    return rtl


def m_sync_mbits(clock, reset, sigin, sigou):

    d1 = Signal(intbv(0)[len(sigou):])

    @always_seq(clock.posedge, reset=reset)
    def rtl():
        d1.next = sigin
        sigou.next = d1

    return rtl
