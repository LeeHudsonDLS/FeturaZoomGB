#!/bin/env dls-python

import sys, os, re
from motorhome import *

#Gonio omega pre string for phasing
gonioOmegaPhase = """
        if(m148 = 1)
          cmd "#1$"
          timer = 20 MilliSeconds ; Small delay to start moving
		  while (timer > 0)
		  endw
		  while(m249=1)
		  endw
          timer = 100 MilliSeconds ; Small delay to start moving
		  while (timer > 0)
		  endw
        endif
"""

gonioZPhase = """
        if(m548 = 1)
          cmd "#5$"
          timer = 20 MilliSeconds ; Small delay to start moving
		  while (timer > 0)
		  endw
		  while(m549=1)
		  endw
          timer = 100 MilliSeconds ; Small delay to start moving
		  while (timer > 0)
		  endw
        endif
"""

detectorZPreMove = """
        cmd "#8j+"
        while(m821=0) 
        endw

        timer = 100 MilliSeconds ; Small delay to start moving
		while (timer > 0)
        endw

        cmd"#8j-"
        while(m821=1)
        endw
        
        cmd"#8j/"
        timer = 100 MilliSeconds ; Small delay to start moving
		while (timer > 0)
        endw
"""
oavYPhase = """
        if(m648=1)
          cmd "#6k"
          while(m621=0)
          endwhile
          m671=2634
          timer = 500 MilliSeconds ; Small delay to start moving
		  while (timer > 0)
          endw
          m648=0
        endif
        cmd "#6j+"
        while(m621=0)
        endwhile

"""

oavYPost = """
        cmd "setphase6"
        m648=0
"""

oavXPhase = """
        if(m548=1)
          cmd "#5k"
          while(m521=0)
          endwhile
          m571=3765
          timer = 500 MilliSeconds ; Small delay to start moving
		  while (timer > 0)
          endw
          m548=0
        endif
        cmd "#5j+"
        while(m521=0)
        endwhile
"""

oavXPost = """
        cmd "setphase5"
        m548=0
"""
# find the plc number and name from the filename
filename = sys.argv[1]
result = re.search(r"PLC(\d+)_([^_]*)_HM\.pmc", filename)
if result is not None:
    num, name = result.groups()
else:
    sys.stderr.write("***Error: Incorrectly formed homing plc filename: %s\n" % filename)
    sys.exit(1)

plc = PLC(int(num), post = None,ctype=PMAC)

################# BL02I-MO-PMAC-01 ###################
if name == "S1":
    plc.add_motor(1, group = 2, htype=HSW_HLIM, jdist=-500)
    plc.add_motor(2, group = 3, htype=HSW_HLIM, jdist=-500)
    plc.add_motor(3, group = 4, htype=HSW_HLIM, jdist=-500)
    plc.add_motor(4, group = 5, htype=HSW_HLIM, jdist=-500)

################# BL02I-MO-STEP-05 ###################
elif name == "DMM":
    plc = PLC(int(num), post = None,ctype=GEOBRICK)
    plc.add_motor(1, group=2, htype=HSW_HLIM, jdist=-1000)
    plc.add_motor(4, group=3, htype=HSW_HLIM, jdist=-1000)
    plc.add_motor(5, group=4, htype=HSW_HLIM, jdist=-1000)
    plc.add_motor(6, group=5, htype=HSW_HLIM, jdist=1000)
    plc.add_motor(7, group=7, htype=HSW_DIR, jdist=1000)
    for axis in (2,3): # Both Inboard Y and Outboard Y grouped together
        plc.add_motor(axis, group=6, htype = HSW_HLIM, jdist=-1000)

################# BL02I-MO-PMAC-02 ###################

#elif name == "DET":
#    plc = PLC(int(num), post = None,ctype=PMAC)
#    for axis in (1,2): # Both translations grouped together
#        plc.add_motor(axis, group=2, htype=HSW_HLIM, jdist=1000)
#    plc.add_motor(21, group=3, htype=HSW_HLIM, jdist=1000)
#    plc.add_motor(22, group=4, htype=HSW_HLIM, jdist=1000)
elif name == "TABLE":
    plc = PLC(int(num), post = None,ctype=PMAC)
    for axis in (6,7,8): # All 3 jacks grouped together
        plc.add_motor(axis, group=3, htype = HOME, jdist = 10000)
    for axis in (17,18): # Both translations grouped together
        plc.add_motor(axis, group=2, htype = HOME, jdist = 1000)
elif name == "GONP":
    plc = PLC(int(num), post = None,ctype=PMAC)
    plc.add_motor(3, group=2, htype = HSW, jdist = 10000)
    plc.add_motor(4, group=3, htype = HSW, jdist = 2000)
    plc.add_motor(5, group=4, htype = HSW, jdist = 1000)

################# BL02I-MO-PMAC-03 ###################

elif name == "OMEGA":
    plc = PLC(int(num), post = None,ctype=PMAC)
    plc.add_motor(1, group=2, htype = HOME, jdist = 0)

################# BL02I-MO-STEP-01 ###################

elif name == "BSX":
    plc = PLC(int(num), post = None,ctype=GEOBRICK)
    plc.add_motor(1, group=2, htype=HOME, jdist=0)
elif name == "MAPTXZ":
    plc = PLC(int(num), post = None,ctype=GEOBRICK)
    plc.add_motor(2, group=2, htype=HOME, jdist=0)
    plc.add_motor(3, group=3, htype=HOME, jdist=0)
elif name == "SCAT":
    plc = PLC(int(num), post = None,ctype=GEOBRICK)
    plc.add_motor(4, group=2, htype=HOME, jdist=0)
    plc.add_motor(5, group=3, htype=HOME, jdist=0)

################# BL02I-MO-STEP-02 ###################

elif name == "SCIN":
    plc = PLC(int(num), post = None,ctype=GEOBRICK)
    plc.add_motor(1, group=2, htype=RLIM, jdist=0)
    plc.add_motor(8, group=3, htype=RLIM, jdist=0)
elif name == "MAPTY":
    plc = PLC(int(num), post = None,ctype=GEOBRICK)
    plc.add_motor(7, group=2, htype=HSW, jdist=1000)

################# BL02I-MO-STEP-03 ###################

elif name == "BSYZ":
    plc = PLC(int(num), post = None,ctype=GEOBRICK)
    plc.add_motor(1, group=2, htype=HSW, jdist=1000)
    plc.add_motor(2, group=3, htype=HSW, jdist=1000)
elif name == "SAMP":
    plc = PLC(int(num), post = None,ctype=GEOBRICK)
    plc.add_motor(3, group=2, htype=RLIM, jdist=0)
    plc.add_motor(4, group=3, htype=RLIM, jdist=0)

################# BL02I-MO-STEP-04 ###################

elif name == "CRL":
    plc = PLC(int(num), post = None,ctype=GEOBRICK)
    plc.add_motor(1, group=2, htype=HSW, jdist=1000)
    plc.add_motor(2, group=3, htype=HSW, jdist=2000)
    plc.add_motor(3, group=4, htype=HSW, jdist=1000)
    plc.add_motor(4, group=5, htype=HSW, jdist=-2000)
    plc.add_motor(5, group=6, htype=HSW, jdist=-1000)

elif name == "ZOOM":
    plc = PLC(int(num), post = None,ctype=GEOBRICK)
    plc.add_motor(7, group=2, htype=HSW, jdist=-1000)
    plc.add_motor(8, group=3, htype=HSW, jdist=1000)
    plc.configure_group(2, post='cmd "#7J=-38264"')
    plc.configure_group(3, post='cmd "#8J=-48882"')
################# BL03I-MO-STEP-06 ###################

elif name == "DCM":
    plc = PLC(int(num), post = None,ctype=GEOBRICK)
    plc.add_motor(1, group=2, htype=HSW_HLIM, jdist=-100000)
    plc.add_motor(5, group=3, htype=HSW_HLIM, jdist=-1000)
    plc.add_motor(3, group=4, htype=HSW_HLIM, jdist=20000)
    plc.add_motor(4, group=5, htype=HSW_HLIM, jdist=-1000)

elif name == "ATT2":
    plc = PLC(int(num), post = None,ctype=GEOBRICK)
    plc.add_motor(6, group=2, htype=RLIM, jdist=-1000)


################# BL03I-MO-STEP-09 ###################

elif name == "CHOPX":
    plc = PLC(int(num), post = None,ctype=GEOBRICK)
    plc.add_motor(2, group=2, htype=RLIM, jdist=-100000)
elif name == "S4":
    plc = PLC(int(num), post = None,ctype=GEOBRICK)
    plc.add_motor(5, group = 2, htype=RLIM, jdist=0)
    plc.add_motor(6, group = 3, htype=RLIM, jdist=0)
    plc.add_motor(7, group = 4, htype=RLIM, jdist=0)
    plc.add_motor(8, group = 5, htype=RLIM, jdist=0)

################# BL02I-MO-STEP-10 ###################

elif name == "VMFM":
    plc = PLC(int(num), post = None,ctype=GEOBRICK)
    plc.add_motor(1, group=5, htype=HSW, jdist=-1000)
    plc.add_motor(2, group=2, htype=RLIM,jdist=0)
    plc.add_motor(3, group=3, htype=HSW, jdist=-1000)
    plc.add_motor(4, group=4, htype=HSW, jdist=-1000)

elif name == "HMFM":
    plc = PLC(int(num), post = None,ctype=GEOBRICK)
    plc.add_motor(5, group=5, htype=HSW, jdist=-1000)
    plc.add_motor(6, group=2, htype=HSW, jdist=-50000)
    plc.add_motor(7, group=3, htype=HSW, jdist=-1000)
    plc.add_motor(8, group=4, htype=HSW, jdist=-1000)

################# BL02I-MO-STEP-11 ###################

elif name == "ATT3":
    plc = PLC(int(num), post = None, ctype=GEOBRICK)
    plc.add_motor(1, group=2,htype=HSW, jdist=-500)
    plc.add_motor(2, group=3,htype=HSW, jdist=-500)
    plc.add_motor(3, group=4,htype=HSW, jdist=-500)

################# BL02I-MO-STEP-12 ###################

elif name == "GONIO":
    plc = PLC(int(num), post = None,ctype=GEOBRICK)
    plc.add_motor(2, group=2, htype=HSW, jdist=-1000)
    plc.add_motor(3, group=3, htype=HSW, jdist=-1000)

    
  #  plc.add_motor(1, group=4, htype=HSW, jdist=-1000)
  #  plc.configure_group(4,pre=gonioOmegaPhase,post='cmd "setphase1" ')
######################################################


################# BL02I-MO-STEP-13 ###################

elif name == "OAV":
    plc = PLC(int(num), post = None,ctype=GEOBRICK)
    plc.add_motor(5, group=2, htype=HSW, jdist=10)
    plc.configure_group(2,pre=oavXPhase,post='cmd "setphase5"')
    plc.add_motor(6, group=3, htype=HSW, jdist=10)
    plc.configure_group(3,pre=oavYPhase,post='cmd "setphase6"')

elif name == "DET":
    plc = PLC(int(num), post = None,ctype=GEOBRICK)
    plc.add_motor(8, group=2, htype=HSW_HLIM, jdist=1000)
    plc.configure_group(2,pre=detectorZPreMove)

elif name == "BMSTP":
    plc = PLC(int(num), post = None,ctype=GEOBRICK)
    plc.add_motor(1, group=2, htype=HSW_HSTOP, jdist=-10000)
    plc.add_motor(2, group=3, htype=HSW_HSTOP, jdist=-10000)
    plc.add_motor(3, group=4, htype=HSW_HSTOP, jdist=10000)
######################################################

################# BL02I-MO-STEP-14 ###################
#Not used at the moment as custom routine is used
#elif name == "GONIOX":
#    plc = PLC(int(num), post = None,ctype=GEOBRICK)
#    plc.add_motor(3, group=2, htype=HSW, jdist=-1000)
#    plc.add_motor(4, group=2, htype=HSW, jdist=-1000)

elif name == "GONIOSAM":
    plc = PLC(int(num), post = None,ctype=GEOBRICK)
    plc.add_motor(1, group=2, htype=HSW, jdist=-1000)
    plc.configure_group(2,pre=gonioOmegaPhase,post='cmd "setphase1" ')
    plc.add_motor(5, group=3, htype=HSW, jdist=-1000)
    plc.configure_group(3,pre=gonioZPhase)

elif name == "CHOP":
    plc = PLC(int(num), post = None,ctype=GEOBRICK)
    plc.add_motor(6, group=2, htype=HSW, jdist=-1000)

######################################################

else:
    sys.stderr.write("***Error: Can't make homing PLC %d for %s\n" % (num, name))
    sys.exit(1)

# write out the plc
plc.write(filename)

