#MDIO Interface Header
BAUD=10000
SYNC_MODE=0x4
DO_MASK_VAL=0x60
DI_MASK_VAL=0x40

MDIO_ETHSW_SSB_MODE=0xe003
MDIO_ETHSW_SSB_ADDR=0xe004
MDIO_ETHSW_SSB_DATA=0xe005
MDIO_BM_FSQM_GCTRL=0xe046
MDIO_BM_GCTRL=0xe049
MDIO_GPHY_FCR_0=0xf700
MDIO_GPHY_FCR_1=0xf710
MDIO_GPHY_FCR_2=0xf720
MDIO_GPHY_FCR_3=0xf730
MDIO_GPHY_FCR_4=0xf740
MDIO_RST_REQ=0xfa01
MDIO_ADDR = 0xFFFF

UART_ETHSW_SSB_MODE='e003'
UART_ETHSW_SSB_ADDR='e004'
UART_ETHSW_SSB_DATA='e005'
UART_BM_FSQM_GCTRL='e046'
UART_BM_GCTRL='e049'
UART_GPHY_FCR_0='f700'
UART_GPHY_FCR_1='f710'
UART_GPHY_FCR_2='f720'
UART_GPHY_FCR_3='f730'
UART_GPHY_FCR_4='f740'
UART_RST_REQ='fa01'
UART_ADDR = 'ffff'

#BASIC MDIO Read Write Commands
def etc_pdi_write(dev,base_addr,offset,data):
	dev.MDIO_Write(0x1F,0x1F,base_addr)
	dev.MDIO_Write(0x1F,offset,data)
	
def etc_pdi_read(dev,base_addr,offset):
		dev.MDIO_Write(0x1F,0x1F,base_addr)
		data = dev.MDIO_Read(0x1F,offset)
		return data

def no_to_str(data):
		data = hex(data)[2:]
		while len(data) < 4:
			data = '0' + data
		return data

#SSB Memory Write and Read Sequence using UART Interface		
def uart_switch_ssb_write(uart,addr,data):
	uart.gphy_wr(UART_ETHSW_SSB_ADDR,addr)
	uart.gphy_wr(UART_ETHSW_SSB_DATA,data)
	uart.gphy_wr(UART_ETHSW_SSB_MODE,'0001')
	
def uart_switch_ssb_read(uart,addr):
	uart.gphy_wr(UART_ETHSW_SSB_ADDR,addr)
	uart.gphy_wr(UART_ETHSW_SSB_MODE,'0002')
	return uart.gphy_rd(UART_ETHSW_SSB_DATA)

