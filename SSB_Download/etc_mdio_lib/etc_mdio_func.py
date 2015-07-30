from etc_mdio_lib.etc_mdio_header import *

#Miscellaneous functions		
def file_len(fname):
    with open(fname) as f:
        for i, l in enumerate(f):
            pass
    return i + 1

#SSB Memory write Sequence using MDIO interface
def mdio_switch_ssb_write(dev_mdio,addr,data):
	etc_pdi_write(dev_mdio,MDIO_ETHSW_SSB_ADDR,0x0,addr)
	etc_pdi_write(dev_mdio,MDIO_ETHSW_SSB_DATA,0x0,data)
	etc_pdi_write(dev_mdio,MDIO_ETHSW_SSB_MODE,0x0,0x0001)

def mdio_switch_ssb_read(dev_mdio,addr):
	etc_pdi_write(dev_mdio,MDIO_ETHSW_SSB_ADDR,0x0,addr)
	etc_pdi_write(dev_mdio,MDIO_ETHSW_SSB_MODE,0x0,0x0002)
	return etc_pdi_read(dev_mdio,MDIO_ETHSW_SSB_DATA,0x0)
	
def Download_Gphy_firmware(dev_mdio,ADDR):
#Download Gphy firmware to SSB Memory
#reading the hex file
	file_name = raw_input('Enter the gphy firmware file name:')
	hex_file = open(file_name,'r+')
	noce = file_len(file_name)
	ix = noce
	#write the data into SSB Memory
	while ix:
		#Data read from the hex file
		dataS = int(hex_file.read(5)[:-1],16)	
		#mdio_switch_ssb_write(dev_mdio,ADDR,dataS)
		dataR = mdio_switch_ssb_read(dev_mdio,ADDR)
		print hex(ADDR), hex(ix), hex(dataS), dataR
		ADDR = ADDR - 1
		ix = ix -1

	#reduce number of ssb segments to be used by switch
	etc_pdi_write(dev_mdio,MDIO_BM_FSQM_GCTRL, 0x00,(510-(noce >> 7)))
	etc_pdi_write(dev_mdio,MDIO_BM_GCTRL,0x00,0xE049)	

	#point GPHY CPU' to begining of SSB
	etc_pdi_write(dev_mdio,MDIO_GPHY_FCR_0,0x00,0x2000)	
	etc_pdi_write(dev_mdio,MDIO_GPHY_FCR_1,0x00,0x2000)	
	etc_pdi_write(dev_mdio,MDIO_GPHY_FCR_2,0x00,0x2000)	
	etc_pdi_write(dev_mdio,MDIO_GPHY_FCR_3,0x00,0x2000)	
	etc_pdi_write(dev_mdio,MDIO_GPHY_FCR_4,0x00,0x2000)	
	etc_pdi_write(dev_mdio,MDIO_RST_REQ,0x00,0x0000)
	
def enable_pie_insertion_extraction(dev_mdio):
	etc_pdi_write(dev_mdio,0xFA01,0x00,0x0000)
	etc_pdi_write(dev_mdio,0xFA01,0x00,0x001F)
	etc_pdi_write(dev_mdio,0xF400,0x00,0x8000)
	etc_pdi_write(dev_mdio,0xF40F,0x00,0x3200)
	etc_pdi_write(dev_mdio,0xE080,0x00,0x0001)
	etc_pdi_write(dev_mdio,0xE082,0x00,0x0001)
	etc_pdi_write(dev_mdio,0xE084,0x00,0x0001)
	etc_pdi_write(dev_mdio,0xE086,0x00,0x0001)
	etc_pdi_write(dev_mdio,0xE088,0x00,0x0001)
	etc_pdi_write(dev_mdio,0xE08A,0x00,0x0001)
	etc_pdi_write(dev_mdio,0xE08C,0x00,0x0001)
	etc_pdi_write(dev_mdio,0xF130,0x00,0x0200)
	etc_pdi_write(dev_mdio,0xE455,0x00,0x007F)
	etc_pdi_write(dev_mdio,0xE454,0x00,0x007F)
	etc_pdi_write(dev_mdio,0xFA01,0x00,0x0000)



	
