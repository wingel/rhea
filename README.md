**NOTE** the following is a work-in-progress (WIP) and has not reached
a minor release point.  If you happen to come across this public repository
feel free to try it out and contribute.  This repository will
be unstable until the first minor release 0.1. 
 
minnesota (`mn`)
================

The minnesota python package is a collection of HDL cores written 
in MyHDL.  The "mn" package is dependent on the myhdl package.  
The myhdl package can be retrieved from http://www.myhdl.org

Some of the [examples](https://github.com/cfelton/minnesota/tree/master/examples) 
have an additional dependency, the [gizflow](https://github.com/cfelton/gizflo) package.
The gizflo package is used to manage different development boards and 
simplify the FPGA tool flow.  See the FPGA compile templates 
in the [examples directory](https://github.com/cfelton/minnesota/tree/master/examples) for 
varioius boards.


**IMPORTANT NOTE** this repository is under development and is using
features from a development version of MyHDL (0.9dev).  If you 
wish to try out this package get 
[the development myhdl](https://github.com/jandecaluwe/myhdl)  (you will 
need to clone it and install the source).  The first 
*mn* release will not occur until myhdl 0.9 is released (probably much
later).

This code/package is licensed user the LGPL license.  This allows 
anyone to use the package in their projects with no limitations but
if the code in the mn package is modified those modifications need to
be made available to the public (not the code the cores are used 
in).  Questions and other license options email me.

The following are the definition of some terms used in this README :


   * cores : the building blocks of a system.  Also, know as IP
     (intellectual property).

   * system : the digital design being implement, synonymous with 
     system-on-a-chip, not using the term system-on-a-chip (SoC) 
     because SoC it is typically reserved for systems that contains 
     a CPU.  In this document and the example the **system** can be
     a SoC or other complex digital design.

   * register : collection of bits that retain state. 

   * register file : collection of same-sized registers, a register
     file is organized into read-write entities and read-only entities.
     A register-file is a programming/configuration interface to a 
     core.

   * csr: control and status register.  This term is commonly used for
     the memory-mapped interface to the cores.


getting started
-------------------
To get started with the latest version (repo version) checkout out the
code and run setup in *develop* mode.
 

```
  # get the required python packages, myhdl, gizflo,
  # and the latest minnesota package.
  >> git clone https://github.com/jandecaluwe/myhdl
  >> sudo python setup.py install
  >> cd ..
  
  # see www.myhdl.org for information on myhdl, the *mn* package 
  # requires a 0.9 feature -interfaces-.  After 0.9 is release the
  # official myhdl releases should be used.  Refer to the myhdl
  # mailing-list for more information.

  # FPGA build and misc HDL tools
  >> hg clone https://githumb.com/cfelton/gizflo
  >> cd gizflo
  >> sudo python setup.py install 
  >> cd ..

  >> git clone https://github.com/cfelton/minnesota
  >> cd minnesota
  # requires setuptools
  >> python setup.py develop

  # verify the tests run (if not, post a comment)
  >> cd test
  >> py.test

  # try to compile one of the examples 
  # (requires FPGA tools installed and gizflo)
  >> cd ../examples/boards/nexys/fpgalink
  >> python test_fpgalink.py
  >> python compile_fpgalink.py
```

<!-- move to the docs
system (Infrastructure)
-----------------------

In the "mn" package, the sub-packages that are not cores or example
systems are tools to build systems.


### regfile
The register file objects provide simple methods to define registers
via Python dicts or Register objects.  From these definitions the 
registers in a peripheral are created and connected to a memory-mapped
bus (e.g. wishbone, avalon, etc). 


#### Defining a Register File

A register file definition is a Python `dictionary` that contains 
`Register` objects and the keys are the register names.

```python
regdef = {
    # --register 0--
    'reg0': Register('reg0', 0x0018, 8, 'rw', 0),
    'reg1': Register('reg1', 0x0032, 8, 'rw', 0)
}
```

or

```python
regfile = RegisterFile(width=32)
regfile.add_register(Register('reg0', 0x0018, 32, 'rw', 0))
-->```

<!-- 
somethings missing from refile
   1. mixed widths, the registers need to be packet, sparse
      definitions will not be optimal.  Future enhancement 
      that can occur under the hood
-->

<!-- move to the docs
#### Adding a Register File to a Peripheral


#### Adding a Memory-Mapped Bus to a System
-->

<!--
### memmap
The memory-map type buses

   * Wishbone
   * Avalon
   * simple


models
------
To facilitate development and verification models are created of external 
devices or "golden" models of an internal peripheral or processing block.



cores
-----
The following is a list of currently implemented cores.


### fpgalink

This is a MyHDL implementation of the HDL for the *fpgalink*
project.  The fpgalink HDL core can be instantiated into 
a design:


```python

    from mn.cores.usbext import m_fpgalink_fx2
 
    # ...
    # fpgalink interface 
    g_fli = m_fpgalink_fx2(clock,reset,fx2bus,flbus) 

    # ...
```

For simulation and verification the *fpgalink* interface can be
stimulated using the FX2 model and high-level access functions:

```python
   from mn.models.usbext import fpgalink_host
   from mn.cores.usbext import fpgalink 
   from mn.cores.usbext import m_fpgalink_fx2
 
   # instantiate the components, etc (see examples in example dir)
   # ...
   # use high-level accessors to 
   fh.WriteAddress(1, [0xC3])     # write 0xCE to address 1
   fh.WriteAddress(0, [1,2,3,4])  # write 1,2,3,4 to address 0
   rb = fh.ReadAddress(1)         # read address 1
```

The following is a pictorial of the verification environment .


For more information on the [fpgalink]() software, firmware, and
general design information see [makestuff]().


### usbp

USB Peripheral, this is another Cypress FX2 controller interface, 
this has two interfaces a "control" interface and a "streaming" 
interface.  This FX2 interface is intended to work with the 
[fx2 firmware]() that configures the controller as a USB CDC/ACM
device (virtual serial port).  The [fx2 firmware]() also has a
couple vendor unique commands that can be sent using the pyusb
(or other low-level USB interfaces like libusb).  The Python
version of the host software (including firmware) can be retrieved
via pip.

|   >> pip install usbp
|   >>> import usbp
|   >>> import serial

One of the tricky items with USB devices is setting the permissions
correctly.  On a linux system to set the …


### fifo ramp


### spi
-->

test
----
The test directory contains test for the different cores in the package.
Most of the test have the additional dependency of the `myhdl_tools`_ 
package.


examples
--------
In the examples directory are projects that demonstrate how to build 
systems using the cores and various tools and target a particular FPGA 
development board.  As mentioned above the examples have an additional 
dependency, [gizflo]() to create the actual bitstreams.  

<!-- move to the docs
### Xess Xula(2)
Examples

   * binary hello (blinky)
   * VGA


### Digilent Nexys
Examples 

   * binary hello (blinky)
   * fpgalink
   * usbp


### Digilent Atlys
   * binary hello (blinky)
   * fpgalink
   * usbp


### Digilent Zybo
   * binary hello (blinky)
   


### Open-Source UFO-400
Examples

   * binary hello
   * usbp


### DSPtronics Signa-X1 (sx1)
Examples

   * binary hello
   * fpgalink
   * usbp
   * audio examples
      * audio echo
      * audio streaming
      
 -->
