ETC Setting for Enabling the SMDIO Interface
1. Pin Strapping Setting P_SL_TYPE - On
2. GPIO_ALTSEL0.4 and GPIO_ALTSEL0.5 - 0(default is 03f3 , set it to 03c3) - ALTSEL0_ADDR = 0xf383
3. GPIO_ALTSEL1.4 and GPIO_ALTSEL1.5 - 1(default is 3f, no need to change) - ALTSEL1_ADDR = 0xf384
2. Write Register SMDIO CFG Register (F480) - 0x1f1 - SMDIO_CFG_ADDR = 0xf480

Connection -
1.FTDI ADBUS(J7.S6) ----> SMDC(J20.8)
2.FTDI_ADBUS(J7.S5) ----> SMDIO(J20.6)
