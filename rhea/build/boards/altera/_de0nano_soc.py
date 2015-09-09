#
# Copyright (c) 2015 Christopher L. Felton
#

from ..._fpga import _fpga
from ...toolflow import Quartus


class DE0NanoSOC(_fpga):
    vendor = 'altera'
    family = 'Cyclone V'
    device = '5CSEMA4U23C6'
    speed = '6'
    _name = 'de0nano_soc'

    default_clocks = {
        'clock': dict(frequency=50e6, pins=('V11',))
    }

    default_resets = {
        'reset': dict(active=0, async=True, pins=('AH16',))
    }
    
    default_ports = {
        'led': dict(pins=('W15', 'AA24', 'V16', 'V15'
                          'AF26', 'AE26', 'Y16', 'AA23',)),
        'key': dict(pins=('AH17')),
        'sw': dict(pins=('L10', 'L9', 'H5', 'H6')),
        
        # bi-directional GPIO, naming slightly different than the
        # reference manual and schematics.  The GPIO are not separated
        # into GPIO_0 and GPIO_1
        # @todo: finish the GPIO pins
        'gpio': dict(pins=('V12', 'AF7', 'W12', 'AF8', 'Y8', 'AB4',
                           'W8', 'Y4', 'Y5', 'U11', 'T8', 'T12')),
    }

    def get_flow(self):
        return Quartus(brd=self)
