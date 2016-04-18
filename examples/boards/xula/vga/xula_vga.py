
from myhdl import ResetSignal, always

from rhea.system import Global
from rhea.cores.video import VGA, VideoMemory
from rhea.cores.video import vga_sync, color_bars


def xula_vga(

    # ~~~[PORTS]~~~
    vselect,
    hsync, vsync, 
    red, green, blue,
    clock,
    reset=None,

    # ~~~~[PARAMETERS]~~~~
    resolution=(640, 480,),
    color_depth=(3, 4, 3,),
    refresh_rate=60,
    line_rate=31250):

    # stub out reset if needed
    if reset is None:
        reset = ResetSignal(0, active=0, async=False)

        @always(clock.posedge)
        def reset_stub():
            reset.next = not reset.active
    else:
        reset_stub = None

    # create the system-level signals, overwrite clock, reset
    glbl = Global(clock=clock, reset=reset)

    # VGA interface
    vga = VGA(hsync=hsync, vsync=vsync, 
              red=red, green=green, blue=blue,
              color_depth=color_depth)

    # video memory interface
    vmem = VideoMemory(color_depth=color_depth)
        
    # instances of modules
    bar_inst = color_bars(glbl, vmem, resolution=resolution,
                          color_depth=color_depth)

    vga_inst = vga_sync(glbl, vga, vmem, resolution=resolution,
                        refresh_rate=refresh_rate, line_rate=line_rate)

    return bar_inst, vga_inst, reset_stub

#
# def convert(color_depth=(10, 10, 10,)):
#     """ convert the vgasys to verilog
#     """
#     clock = Clock(0, frequency=50e6)
#     reset = Reset(0, active=0, async=False)
#     vselect = Signal(bool(0))
#
#     hsync = Signal(bool(0))
#     vsync = Signal(bool(0))
#     cd = color_depth
#     red = Signal(intbv(0)[cd[0]:])
#     green = Signal(intbv(0)[cd[1]:])
#     blue = Signal(intbv(0)[cd[2]:])
#     pxlen = Signal(bool(0))
#     active = Signal(bool(0))
#
#     toVerilog.timescale = '1ns/1ns'
#     toVerilog(mm_vgasys, clock, reset, vselect,
#               hsync, vsync, red, green, blue,
#               pxlen, active)
#
#     toVHDL(mm_vgasys, clock, reset, vselect,
#            hsync, vsync, red, green, blue,
#            pxlen, active)
#
#
# if __name__ == '__main__':
#     convert()
