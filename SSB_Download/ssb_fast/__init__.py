import time
import sys
from etc import Etc as e
import serial

#class etcFlash(object):
class etcFlash:
    def __init__(self, port_num):
        #"""   ------------------------------------------------------------------------------------------- """
        #"""                              Set-up the COM port                                              """
        #"""   ------------------------------------------------------------------------------------------- """
        self.ser = serial.Serial(
            port='COM'+str(port_num),     # Change the COM port number according to your settings
            baudrate=115200,
            bytesize=8,
            parity='N',
            stopbits=1,
            timeout=1,
            xonxoff=0,
            rtscts=0)

        if self.ser.isOpen() != 1:
            print "The COM Port is NOT Active; Check your COM number : ", ser.name
            sys.exit(0)
        print "  COM Port Is Alive   : ", self.ser.name
		
	def flush_uart_rx(self):
         self.ser.flush()
         while(self.ser.readline()):
             pass

		 
	def uart921600(self):
         s = "\n"
         s += "w %s %s xxx\n" % (e.UART_BD, "010f") # set baud rate to 921600
         self.ser.write(s)
         time.sleep(0.2)
         self.ser.baudrate=921600
         s = "\n# just something\n"
         self.ser.write(s)
         self.ser.flush()

    def uart115200(self):
         s = "\n"
         s += "w %s %s xxx\n" % (e.UART_BD, "087a") # set baud rate to 115200
         self.ser.write(s)
         time.sleep(0.2)
         self.ser.baudrate=115200
         s = "\n# just something\n"
         self.ser.write(s)
         self.ser.flush()
    

    def mspi_en(self):
         s = """
         m F383 03C0 03C0 xxx \n
         m F384 0000 03C0 xxx \n
         m F511 0001 0001 xxx \n
        """
         self.ser.write(s)

    def flash_erase(self):
         print "\n Flash Erase in Progress ............. \n"
         self.mspi_en()
         s = """
         w F51C 0600 xxx
         w F512 0008 xxx
         w F51C 6000 xxx
         w F51D 0000 xxx
         w F512 0008 xxx
         w F51C 0600 xxx
         w F512 0008 xxx
         w F51C C700 xxx
         w F51D 0000 xxx
         w F512 0008 xxx
         """
         self.ser.write(s)
         time.sleep(5.0)
         rdata = self.rd_flash(0)
         if rdata != "ffff":
             print "\n Erase Flash NOT successful!!! :\n",rdata
             sys.exit(0)
         else:
             print "\n Flash Erased .........\n"
		 
		 
    def mscs_overide_low(self):
         s = """
         m F382 0200 0200 xxx
         m F380 0200 0200 xxx
         m F383 01C0 03C0 xxx
         m F380 0000 0200 xxx
         """
         self.ser.write(s)

    def mscs_pull_high(self):
         s = """
         m F380 0200 0200 xxx
         m F383 03C0 03C0 xxx
         """
         self.ser.write(s)

    def wr_flash_enable(self):
         s = """
         w F51C 0600 xxx
         w F512 0008 xxx
         """
         self.ser.write(s)
   
    def wr_cmd_addr(self,addr_int):
         a = addr_int + 2**24
         addrh = hex(a)[3:5]
         addrl = hex(a)[5:9]
         s = """
         w F51C 02%s xxx
         w F51D %s xxx
         w F512 000B xxx
         """ % (addrh, addrl)
         self.ser.write(s)

    def wr_data(self,data_8byte):
         d01 = data_8byte[2:4]+data_8byte[0:2]
         d23 = data_8byte[6:8]+data_8byte[4:6]
         d45 = data_8byte[10:12]+data_8byte[8:10]
         d67 = data_8byte[14:16]+data_8byte[12:14]
         s = """
         w F51C %s xxx
         w F51D %s xxx
         w F51E %s xxx
         w F51F %s xxx
         w F512 000F xxx
         """ % (d01,d23,d45,d67)
         self.ser.write(s)

    def wr_block(self, addr_int, data_block):
         self.wr_flash_enable()
         self.mscs_overide_low()
         self.wr_cmd_addr(addr_int)
         for i in range(0,len(data_block),16):
             self.wr_data(data_block[i:i+16])
         self.mscs_pull_high()

    def rd_data(self):
         self.ser.flush()
         xx = self.ser.readline()
         while(xx):
             x = xx.strip('\r\n')
             if len(x) == 4:
                 return x
             xx = self.ser.readline()
         return x
	
    def rd_flash(self,addr_int):
         a = addr_int + 2**24
         addrh = hex(a)[3:5]
         addrl = hex(a)[5:9]
         s = """
         w F51C 03%s xxx
         w F51D %s xxx
         w F512 000D xxx
         """ % (addrh, addrl)
         self.ser.write(s)
         time.sleep(0.1)
         self.ser.flushInput()
         s = """
         r F51A xxx
         """
         self.ser.write(s)
		 # clear the q
         time.sleep(0.1)
         return self.rd_data()
    
    def flash_down_ld(self,f):
         #self.uart921600()
         s = "\n"
         s += "w %s %s xxx\n" % (e.UART_BD, "010f") # set baud rate to 921600
         self.ser.write(s)
         time.sleep(0.2)
         self.ser.baudrate=921600
         s = "\n# just something\n"
         self.ser.write(s)
         self.ser.flush()
         #
         ix = 127
         data_block = ""
         addr_int = 0
         line = f.readline().rstrip('\n')
         while(line):
             if len(line) < 4:
                 print "address: ", str(addr_int)
                 print "data: ", line
                 print "\nInput file format incorrect!!!\n"
                 sys.exit(0)
             if ix == 0:
                 data_block = data_block + line[0:4]
                 print "addr: ", hex(addr_int)
                 self.wr_block(addr_int, data_block)
                 data_block = ""
                 addr_int = addr_int + 256
                 ix = 127
             else:
                 data_block = data_block + line[0:4]
                 ix = ix -1
        
             line = f.readline().rstrip('\n')
         f.close()
         self.uart115200()         
		 
	def ssb_down_ld(self,f):
         #self.uart921600()
         s = "\n"
         s += "w %s %s xxx\n" % (e.UART_BD, "010f") # set baud rate to 921600
         self.ser.write(s)
         time.sleep(0.2)
         self.ser.baudrate=921600
         s = "\n# just something\n"
         self.ser.write(s)
         self.ser.flush()
         #
         ix = 127
         data_block = ""
         addr_int = 0
         line = f.readline().rstrip('\n')
         while(line):
             if len(line) < 4:
                 print "address: ", str(addr_int)
                 print "data: ", line
                 print "\nInput file format incorrect!!!\n"
                 sys.exit(0)
             if ix == 0:
                 data_block = data_block + line[0:4]
                 print "addr: ", hex(addr_int)
                 self.wr_block(addr_int, data_block)
                 data_block = ""
                 addr_int = addr_int + 256
                 ix = 127
             else:
                 data_block = data_block + line[0:4]
                 ix = ix -1
        
             line = f.readline().rstrip('\n')
         f.close()
         self.uart115200()         
	 

    def check_dwnld(self):
         rdata = self.rd_flash(0)
         if rdata != "5656":
             return 0
         rdata = self.rd_flash(2)
         if rdata != "5656":
             return 0
         return 1

    def close(self):
         #self.uart115200()
         self.ser.close()