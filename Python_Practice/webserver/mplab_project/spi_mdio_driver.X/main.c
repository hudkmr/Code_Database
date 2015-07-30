#include <peripheral/spi.h>
#include <peripheral/system.h>
#include <plib.h>


#define VERSION 		"v4.00RC"	// TCP/IP stack version
//* Oscillator Settings
// Configuration Bits
#pragma config FNOSC = FRCPLL // Internal Fast RC oscillator (8 MHz) w/ PLL
#pragma config FPLLIDIV = DIV_2 // Divide FRC before PLL (now 4 MHz)
#pragma config FPLLMUL = MUL_20 // PLL Multiply (now 80 MHz)
#pragma config FPLLODIV = DIV_2 // Divide After PLL (now 40 MHz)

#pragma config FWDTEN = OFF // Watchdog Timer Disabled
#pragma config ICESEL = ICS_PGx1 // ICE/ICD Comm Channel Select
#pragma config JTAGEN = OFF // Disable JTAG
#pragma config FSOSCEN = OFF // Disable Secondary Oscillator

#define SYSCLK 40000000L
#define ENC_RST_TRIS                    (0)	// Not connected
#define ENC_RST_IO			(0)
#define ENC_CS_TRIS			(TRISBbits.TRISB7)		// User must airwire this
#define ENC_CS_IO			(PORTBbits.RB7)
#define ENC_SCK_TRIS                    (TRISBbits.TRISB14)		// User must airwire this
#define ENC_SDI_TRIS                    (TRISBbits.TRISB8)		// User must airwire this
#define ENC_SDO_TRIS                    (TRISAbits.TRISA1)		// User must airwire this
#define ENC_SPI_IF			(IFS0bits.SPI1IF)
#define ENC_SSPBUF			(SPI1BUF)
#define ENC_SPICON1			(SPI1CON)
#define ENC_SPICON1bits                 (SPI1CONbits)
#define ENC_SPICON2			(SPI1BUF)				// SPI1CON2 doesn't exist, remap to unimportant register
#define ENC_SPISTAT			(SPI1STAT)
#define ENC_SPISTATbits		(SPI1STATbits)
#define mSetSPILatch()      {   TRISBbits.TRISB10 = 0, TRISBbits.TRISB11 = 0, LATBbits.LATB11 = 1, LATBbits.LATB11 = 1; }
#define DIS_ANSELA                      (ANSELA)
#define DIS_ANSELB                      (ANSELB)

int main(void)
{
    unsigned int PBCLK;
    unsigned short dataR;
    PBCLK = SYSTEMConfigPerformance(SYSCLK);

   SYSTEMConfigWaitStatesAndPB(72000000);
    // we need to configure for multi-vectored interrupts
   INTEnableSystemMultiVectoredInt();
   
   ANSELACLR = 0xFFFF;
   ANSELBCLR = 0XFFFF;

    TRISACLR = 1 << 1;
    TRISBCLR = 1 << 7;
    TRISBCLR = 1 << 14;
    TRISBSET = 1 << 8;

    setup_pps();
    spi_init_16();
    printf("TCP/IP Stack Porting\n");
    while(1)
    {
        //spi_mdio_write_16(0xFA01,0x00,0x000F);
        spi_mdio_read_16(0xFA00,0x01,&dataR);
    }
    return 0;

}


