md F400 D000 FF00         # GSWIP_CFG  15 enable switch  14 disable port6  12 disable port4
md F410 32A0 FFE0        # force port 4 link up  1000Mbps  full duplex and bidirectional pause enable    
md F383 0000 0033         # GPIO_ALTSEL0
md F3840030 0033        # GPIO_ALTSEL1
md F393 ffFF 7FFF         # GPIO2_ALTSEL0   only enable LEDx0 and LEDx1
md F480 0001 0001    	   # enable SMDIO
md F700 8010 FFFF         # GPHY code offset (point to EEPROM)
md F710 8010 FFFF 
md F720 8010 FFFF 
md F730 8010 FFFF 
md F740 8010 FFFF 
md F100 4000 6000         # MII_CFG_5 EN and NO_ISOL
md F101 0204 0787         # PCDU_5  TXDLY2 0 4 2.0ns   RXDLY9 7 4 2.0ns  DELMD10 0 direct delay setting  
md FA00 0003 FFFF 
md FA01 1010 F01F         # do not release/reset port4