#include <plib.h>
#include "spi_int.h"

#if 0
#define START_BITS  (1 << 30)
#define WRITE_CMD   (1 << 28)
#define READ_CMD    (2 << 28)
#define SMDIO_ADDR  (0x1F <<23)
#define PDI_REG_A   (0x1F << 18)
#define PAD_BITS    (0x2 << 16)
#endif

#define START_BITS  (1 << 14)
#define WRITE_CMD   (1 << 12)
#define READ_CMD    (2 << 12)
#define SMDIO_ADDR  (0x1F << 7)
#define PDI_REG_A   (0x1F << 2)
#define PAD_BITS    (0x2 << 0)


 void setup_pps(void)
 {
     SYSKEY = 0x0;
     SYSKEY = 0xAA996655;
     SYSKEY = 0x556699AA;

     CFGCONbits.IOLOCK = 0;
     RPB14R = 0x0000;       //Default Connection enabled to RPB14 - SCK
     RPB7R = 0x0003;        //SS1 Mapped to RB7
     RPA1R = 0x0003;        //SO1 Mapped to RA1
     SDI1R = 0x0004;        //SD1R Mapped to RB8
     CFGCONbits.IOLOCK = 1;

     SYSKEY = 0x0;
 }

void spi_init_16(void)
{
    //SPI setup
   IEC0CLR=0x03800000;  // disable all interrupts
   SPI1CON = 0;         // Stops and resets the SPI1.
   int rData=SPI1BUF;   // clears the receive buffer
   IFS0CLR=0x03800000;  // clear any existing event
   IPC5CLR=0x1f000000;  // clear the priority
   IPC5SET=0x0d000000;  // Set IPL=3, Subpriority 1
   IEC0SET=0x03800000;  // Enable RX, TX and Error interrupts
   SPI1STATCLR = 0x40;  //Clears overflow
   SPI1CON=0x87A0;
   SPI1BRG = 0x200;
}

unsigned short spi_rw_16 (unsigned short c)
{
    SPI1BUF = c;                   // send data to slave
    while (SPI1STATbits.SPIBUSY);  // wait until SPI transmission complete
    return SPI1BUF;
}

unsigned short spi_read_16 (void)
{
    return spi_rw_16(0);
}

void spi_write_16 (unsigned short c)
{
    (void) spi_rw_16(c);
}

void spi_mdio_write_16(unsigned short base_addr,unsigned char offset, unsigned short data)
{
    unsigned short dataToSend[4];
    dataToSend[0] = START_BITS | WRITE_CMD | SMDIO_ADDR | PDI_REG_A | PAD_BITS;
    dataToSend[1] = base_addr;
    dataToSend[2] = START_BITS | WRITE_CMD | SMDIO_ADDR | offset << 2 | PAD_BITS;
    dataToSend[3] = data;
    spi_write_16(0xFFFF);
    spi_write_16(dataToSend[0]);
    spi_write_16(dataToSend[1]);
    spi_write_16(0xFFFF);
    spi_write_16(dataToSend[2]);
    spi_write_16(dataToSend[3]);
    
}

void spi_mdio_read_16(unsigned short base_addr,unsigned char offset, unsigned short *dataptr)
{
    unsigned int dataToSend[3];
    dataToSend[0] = START_BITS | WRITE_CMD | SMDIO_ADDR | PDI_REG_A | PAD_BITS;
    dataToSend[1] = base_addr;
    dataToSend[2] = START_BITS | READ_CMD | SMDIO_ADDR | offset << 2 | PAD_BITS;
    SPI1CON=0x87A0;
    TRISACLR = 1 << 1;
    spi_write_16(0xFFFF);
    spi_write_16(dataToSend[0]);
    spi_write_16(dataToSend[1]);
    spi_write_16(0xFFFF);
    spi_write_16(dataToSend[2]);
    SPI1CON=0x97A0;
    TRISASET = 1 << 1;
    *dataptr = spi_read_16() >> 1;

}

void packet_

#if 0

void spi_init_32(void)
{
    //SPI setup
   IEC0CLR=0x03800000;  // disable all interrupts
   SPI1CON = 0;         // Stops and resets the SPI1.
   int rData=SPI1BUF;   // clears the receive buffer
   IFS0CLR=0x03800000;  // clear any existing event
   IPC5CLR=0x1f000000;  // clear the priority
   IPC5SET=0x0d000000;  // Set IPL=3, Subpriority 1
   IEC0SET=0x03800000;  // Enable RX, TX and Error interrupts

   SPI1STATCLR = 0x40;      //Clears overflow
   SPI1CON=0x8BA0;
   SPI1BRG = 0x200;
}

char spi_rw_8 (char c)
{
    SPI1BUF = c;                   // send data to slave
    while (SPI1STATbits.SPIBUSY);  // wait until SPI transmission complete
    return SPI1BUF;
}

char spi_read_8 (void)
{
    return spi_rw_8(0);
}

void spi_write_8 (char c)
{
    (void) spi_rw_8(c);
}


unsigned int spi_rw_32 (unsigned int c)
{
    SPI1BUF = c;                   // send data to slave
    while (SPI1STATbits.SPIBUSY);  // wait until SPI transmission complete
    return SPI1BUF;
}

unsigned int spi_read_32 (void)
{
    return spi_rw_32(0);
}

void spi_write_32 (unsigned int c)
{
    (void) spi_rw_32(c);
}


void spi_mdio_write(unsigned short base_addr,unsigned char offset, unsigned short data)
{
    unsigned int dataToSend[2];
    dataToSend[0] = START_BITS | WRITE_CMD | SMDIO_ADDR | PDI_REG_A | PAD_BITS | base_addr;
    dataToSend[1] = START_BITS | WRITE_CMD | SMDIO_ADDR | offset << 2 | PAD_BITS | data;
    spi_write_32(0xFFFFFFFF);
    spi_write_32(dataToSend[0]);
    spi_write_32(0xFFFFFFFF);
    spi_write_32(dataToSend[1]);
}

void spi_mdio_read(unsigned short base_addr,unsigned char offset, unsigned int *dataptr)
{
    unsigned int dataToSend[2];
    dataToSend[0] = START_BITS | WRITE_CMD | SMDIO_ADDR | PDI_REG_A | PAD_BITS | base_addr;
    dataToSend[1] = START_BITS | READ_CMD | SMDIO_ADDR | offset << 2 | PAD_BITS | 0xFFFF;
    spi_write_32(0xFFFFFFFF);
    spi_write_32(dataToSend[0]);
    spi_write_32(0xFFFFFFFF);
    *dataptr = spi_rw_32(dataToSend[1]);
}


char spi_read_control_register(unsigned char addr)
{
    unsigned char addrToSend,temp;
    addrToSend = SPI_RCR_OC | (addr & 0x1F);
    temp = SPI1BUF;
    spi_write_8(addrToSend);
    return spi_read_8();
}

void spi_write_control_register(unsigned char addr,unsigned data)
{
    unsigned char addrToSend,temp;
    addrToSend = SPI_WCR_OC | (addr & 0x1F);
    temp = SPI1BUF;
    spi_write_8(addrToSend);
    spi_write_8(data);
}

#endif