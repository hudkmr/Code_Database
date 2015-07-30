#MDIO Interface Header
BAUD=10000
SYNC_MODE=0x4
DO_MASK_VAL=0x60
DI_MASK_VAL=0x40

HALT_MODE = True
loop = True

def etc_pdi_write(dev,base_addr,offset,data):
	dev.MDIO_Write(0x1F,0x1F,base_addr)
	dev.MDIO_Write(0x1F,offset,data)
	
def etc_pdi_read(dev,base_addr,offset):
		dev.MDIO_Write(0x1F,0x1F,base_addr)
		data = dev.MDIO_Read(0x1F,offset)
		return data