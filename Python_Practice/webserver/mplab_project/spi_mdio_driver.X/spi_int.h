/* 
 * File:   spi_int.h
 * Author: udayakum
 *
 * Created on August 28, 2014, 4:43 PM
 */

#ifndef SPI_INT_H
#define	SPI_INT_H

#ifdef	__cplusplus
extern "C" {
#endif

//Basic Functions
void setup_pps(void);
void spi_init(void);
char spi_rw (char c);
void spi_write (char c);
char spi_read (void);

//enc28j60 functions
char spi_rcr(unsigned char addr);
void spi_wcr(unsigned char addr, unsigned char data);


#define SPI_RCR_OC  (0x0 << 5)
#define SPI_RBM_OC  (0x1 << 5
#define SPI_WCR_OC  (0x2 << 5)
#define SPI_WBM_OC  (0x3 << 5)
#define SPI_BFS_OC  (0x4 << 5)
#define SPI_BFC_OC  (0x5 << 5)
#define SPI_SRC_OC  (0x7 << 5)

#ifdef	__cplusplus
}
#endif

#endif	/* SPI_INT_H */

