
from rhea.system import Global
from rhea.cores.video import VGA
from rhea.cores.video import VideoMemory
from rhea.cores.video import vga_sync
from rhea.cores.video import color_bars


def zybo_vga(
    # Ports
    led, btn, vga_red, vga_grn, vga_blu,
    vga_hsync, vga_vsync, clock, reset=None,
    # Parameters
    resolution=(640, 480), color_depth=(5, 6, 5),
    refresh_rate=60, line_rate=31250):
    """
    This is a VGA example for the Digilent Zybo board.

    Arguments (ports):
        led: the Zybo 4 LEDs
        btn: the Zybo 4 buttons
        vga_red: red bits
        vga_grn: green bits
        vga_blu: blue bits
        vga_hsync: horizontal sync
        vga_vsync: vertical sync

    Parameters:
        resolution: the monitor desired resolution
        color_depth: the number of bits per color
        refresh_rate: the monitor refresh rate
        line_rate: the monitor line rate

    """

    glbl = Global(clock=clock, reset=reset)

    # VGA interface
    vga = VGA(hsync=vga_hsync, vsync=vga_vsync,
              red=vga_red, green=vga_grn, blue=vga_blu,
              color_depth=color_depth)

    # video memory interface
    vmem = VideoMemory(color_depth=color_depth)

    # rhea.core instances
    bar_inst = color_bars(glbl, vmem, resolution=resolution,
                          color_depth=color_depth)
    vga_inst = vga_sync(glbl, vga, vmem, resolution=resolution,
                        refresh_rate=refresh_rate, line_rate=line_rate)

    return bar_inst, vga_inst
