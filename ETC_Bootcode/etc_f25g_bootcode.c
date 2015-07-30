// --------------------------------------
// ETC A21 Boot Code  
// --------------------------------------
//
// This is the top most file of ETC Boot Code.
// It follows the ETC Boot Code Document (please see doc for details).
//
// --------------------------------------

// ------------------------------------
//   History
// -------------------------------------
// A21:
// 	1. load parser-code
//	2. power down unused PLL outputs
//	3. modification of 0000 and FFFF commands to 1111 and 2222
//	4. initiate Pause frame source MAC
//      5. RCAL trigger
//      6. enable low power mode for switch
// ------------------------------------

#include <mcs51/8051.h>
#include <compiler.h>
#include <stdio.h>
#include <ctype.h>

#include <flow25g_regdef.h>
#include <flow25g_xrfi_proc.h>


// define addresses for internal GSWIP registers needed in bootcode
#define  SDMA_PFCTR8_0 0xEC0E
#define  SDMA_PFCTR8_1 0xEC12
#define  SDMA_PFCTR8_2 0xEC16
#define  SDMA_PFCTR8_3 0xEC1A
#define  SDMA_PFCTR8_4 0xEC1E
#define  SDMA_PFCTR8_5 0xEC22
#define  SDMA_PFCTR8_6 0xEC26
#define  SDMA_PFCTR9_0 0xEC0F
#define  SDMA_PFCTR9_1 0xEC13
#define  SDMA_PFCTR9_2 0xEC17
#define  SDMA_PFCTR9_3 0xEC1B
#define  SDMA_PFCTR9_4 0xEC1F
#define  SDMA_PFCTR9_5 0xEC23
#define  SDMA_PFCTR9_6 0xEC27

#define  GSWIP_CFG      0xF400

#define  MAC_PFSA_0     0xE8C2
#define  MAC_PFSA_1     0xE8C3
#define  MAC_PFSA_2     0xE8C4
#define  SYSPLL_CFG_3   0xF98C
//#define  CDB_CTRL       0xF840
#define  CDB_BIAS_0     0xF844

 //unsigned int  ETCB_flashRd

  unsigned char   __idata  flashRd_addrmd;
  unsigned char   __idata  flashRd_manctrl;
  unsigned int    __idata  flashRd_dout01;
  unsigned int    __idata  flashRd_dout23;
  unsigned int    __idata  flashRd_tmp;

 //unsigned char  ETCB_detect_flash / ETCB_gphy_init 
 
  unsigned int    __xdata  tmp;
  unsigned int    __xdata  val;
  unsigned int    __xdata  addrmd;
  unsigned char   __xdata  detected;

 //void ETCB_flash_download(unsigned char ps_led_md, unsigned char ps_subtype_md) 

  unsigned int   __idata  noce;
  unsigned int   __idata  type;
  unsigned long int   __idata  flash_addr;
  unsigned int   __idata  increment;
  unsigned char  __idata  multipland;
  unsigned int   __idata  offset;
  unsigned char  __idata  match;

  unsigned char  __idata  jx;

  // combined variables for flash_download subfunctions / ETCB_fuse_download

  unsigned long int   __idata  f_addr;
  unsigned int   __idata  fcr_val;
  unsigned int   __idata  addr;
  unsigned int   __idata  data;
  unsigned int   __idata  enable;
  unsigned char  __idata  shift;
  unsigned long int  __idata  data_long;  // warning 32-bits
  unsigned int   __idata  fuse_addr;

  unsigned int   __idata  ix;


  //void main() 
  unsigned int   __xdata  ps0_val;
  unsigned int   __xdata  ps1_val;
  
  unsigned char  __xdata  ps_xtal;
  unsigned char  __xdata  ps_op_md1;
  unsigned char  __xdata  ps_subtype_md43;
  unsigned char  __xdata  ps_nowait; 
  unsigned char  __xdata  ps_op_md0;
  unsigned char  __xdata  ps_subtype_md210;          
  unsigned char  __xdata  flash_detected;          

//--------------------------------------
// ETCB_flashRd
//--------------------------------------

unsigned int  ETCB_flashRd(unsigned long int addrl )   
{
//  unsigned char flashRd_addrmd;
//  unsigned char flashRd_manctrl;
//  unsigned int flashRd_dout01;
//  unsigned int flashRd_dout23;

  // request manual mode of MSPI
  XRFISingleWr(MSPI_OP,0x0001);  // write MSPI_OP.MDSEL=1

  flashRd_addrmd = (unsigned char) (XRFISingleRd(MSPI_CFG)>>14) & 0x0003; //bit 15:14

  flashRd_dout01 = 0x0000;
  flashRd_dout23 = 0x0000;
  flashRd_manctrl = 0x00;

  // 9-bit mode
  if(flashRd_addrmd == 0){
    flashRd_dout01 = 0x0300 | ((unsigned int) addrl & 0x00FF) | (((unsigned int) addrl & 0x0100)<<3);
    flashRd_dout23 = 0x0000;
    flashRd_manctrl = 0x0B;   // size = 3 (4-Bytes)
  }

  // 16-bit mode
  if(flashRd_addrmd == 1){
    flashRd_dout01 = 0x0300 | (unsigned int) addrl>>8;
    flashRd_dout23 = (unsigned int) addrl<<8;
    flashRd_manctrl = 0x0C;  // size = 4 (5-Bytes)
  }

  // 24-bit mode
  if(flashRd_addrmd == 2){
    flashRd_dout01 = (unsigned int) (0x0300 | ((addrl>>16) & 0x00FF));
    flashRd_dout23 = (unsigned int) addrl;
    flashRd_manctrl = 0x0D;  // size = 5 (6-Bytes)
  }

  // 24-bit high speed mode
  if(flashRd_addrmd == 3){
    flashRd_dout01 = (unsigned int) (0x0B00 | ((addrl>>16) & 0x00FF));
    flashRd_dout23 = (unsigned int) addrl;
    flashRd_manctrl = 0x0E;  // size = 6 (7-Bytes)
  }

  XRFISingleWr(MSPI_DOUT01,flashRd_dout01);
  XRFISingleWr(MSPI_DOUT23,flashRd_dout23);
  XRFISingleWr(MSPI_DOUT45,0x0000);
  XRFISingleWr(MSPI_DOUT67,0x0000);

  // wait for manual mode acknowledge
  flashRd_tmp = (XRFISingleRd(MSPI_OP)>>1) & 0x0001;
  while(flashRd_tmp == 0){   
    flashRd_tmp = (XRFISingleRd(MSPI_OP)>>1) & 0x0001;
  }

  XRFISingleWr(MSPI_MANCTRL,(unsigned int) flashRd_manctrl);
 
  // wait for BUSY = 0  - end of transaction
  while((XRFISingleRd(MSPI_OP)>>2) & 0x0001 == 1){   
    ;
  }

  // release manual mode of MSPI  - this is very important !!!!
  XRFISingleWr(MSPI_OP,0x0000);  // write MSPI_OP.MDSEL=0
  

  // 9-bit mode
  if(flashRd_addrmd == 0){
    return XRFISingleRd(MSPI_DIN23);
  }

  // 16-bit mode
  if(flashRd_addrmd == 1){
    return (XRFISingleRd(MSPI_DIN23)<<8) | (XRFISingleRd(MSPI_DIN45)>>8);
  }

  // 24-bit mode
  if(flashRd_addrmd == 2){
    return XRFISingleRd(MSPI_DIN45);
  }

  // 24-bit high speed mode
  if(flashRd_addrmd == 3){
    return (XRFISingleRd(MSPI_DIN45)<<8) | (XRFISingleRd(MSPI_DIN67)>>8);
  }

  return 0x0000;   // if unknown mode is set  !Never happens!
}


//--------------------------------------
// ETCB_detect_flash
//--------------------------------------

unsigned char  ETCB_detect_flash(void) {
 
//  unsigned int tmp;
//  unsigned int addrmd;
//  unsigned char detected;
//
  // enable MSPI in GPIO
  XRFISingleRdMdfWr(GPIO_ALTSEL0,0x03C0,0x03C0); // enable MSPI on GPIO         
  XRFISingleRdMdfWr(GPIO_ALTSEL1,0x0000,0x03C0);
    
  // read first two bytes in 24-bit address mode iregardles of actual flash mode
  tmp = ETCB_flashRd(0x00000000);

  // check 
  addrmd = 2;
  detected = 0;
  
  if(tmp==0x5454){
    addrmd = 0;
    detected = 1;
  }

  if(tmp==0x5555){
    addrmd = 1;
    detected = 1;
  }

  if(tmp==0x5656){
    addrmd = 2;
    detected = 1;
  }

  if(tmp==0x5757){
    addrmd = 3;
    detected = 1;
  }
  
  if(detected == 0){
    //    XRFISingleRdMdfWr(GPIO_ALTSEL0,0x0000,0x03C0); //
    //    XRFISingleRdMdfWr(GPIO_ALTSEL1,0x0000,0x03C0); //
    return 0x00;  // flash not detected
  }

  // set address mode for MSPI
  XRFISingleRdMdfWr(MSPI_CFG,addrmd<<14,0xC000);

  // read speed value from flash
  tmp = ETCB_flashRd(0x00000004);

  if( (tmp>>8) != 0x00AA){
    XRFISingleWr(MSPI_CFG,0x8019); // reset value
    //    XRFISingleRdMdfWr(GPIO_ALTSEL0,0x0000,0x03C0); //
    //    XRFISingleRdMdfWr(GPIO_ALTSEL1,0x0000,0x03C0); //
    return 0x00;  // flash not detected
  }

  XRFISingleRdMdfWr(MSPI_CFG,tmp,0x00FF);
  return 0x01; // flash successfully detected
}



//--------------------------------------
// ETCB_gphy_init
//--------------------------------------

void  ETCB_gphy_init(void){

  //    unsigned int tmp;
  
    XRFISingleWr(GPHY_FCR_0,0x0000);       
    XRFISingleWr(GPHY_FCR_1,0x0000);          
    XRFISingleWr(GPHY_FCR_2,0x0000);          
    XRFISingleWr(GPHY_FCR_3,0x0000);          
    XRFISingleWr(GPHY_FCR_4,0x0000);   //new uMc is not dedicated to any Gphy

    if (ps_xtal == 0){
      XRFISingleWr(GPHY_BFDEV_0,0x51EC);
      XRFISingleWr(GPHY_BFDEV_1,0x51EC);
      XRFISingleWr(GPHY_BFDEV_2,0x51EC);
      XRFISingleWr(GPHY_BFDEV_3,0x51EC);
      XRFISingleWr(GPHY_BFDEV_4,0x51EC);

    }

	
	//GPHY_GPS Register Configuration
    tmp = XRFISingleRd(FUSE_WAFERID)>>13;  //only bits 15,14,13
    tmp = (2 << 0 | 1 << 2  | ((tmp & 0x3) << 3) | (~(tmp >> 3) << 5));

    XRFISingleRdMdfWr(GPHY_GPS_0,tmp,0x003F);          
    XRFISingleRdMdfWr(GPHY_GPS_1,tmp,0x003F);          
    XRFISingleRdMdfWr(GPHY_GPS_2,tmp,0x003F);          
    XRFISingleRdMdfWr(GPHY_GPS_3,tmp,0x003F);          
    XRFISingleRdMdfWr(GPHY_GPS_4,tmp,0x003F);  

	//GPHY_ANEG Register Configuration
	tmp =  XRFISingleRd(FUSE1) & 0x3FF; 
	XRFISingleRdMdfWr(GPHY_ANEG_0,tmp,0x03FF);
	tmp =  XRFISingleRd(FUSE2) & 0x3FF; 
	XRFISingleRdMdfWr(GPHY_ANEG_1,tmp,0x03FF);
	tmp =  XRFISingleRd(FUSE3) & 0x3FF; 
	XRFISingleRdMdfWr(GPHY_ANEG_2,tmp,0x03FF);
	tmp =  XRFISingleRd(FUSE4) & 0x3FF; 
	XRFISingleRdMdfWr(GPHY_ANEG_3,tmp,0x03FF);
	tmp =  XRFISingleRd(FUSE5) & 0x3FF; 
	XRFISingleRdMdfWr(GPHY_ANEG_4,tmp,0x03FF);

    // clear the sticky bit for PLL unlock (both plls)
    XRFISingleRdMdfWr(SYS_PLL_MISC,0x4022,0x4000);
    XRFISingleRdMdfWr(CDB_PLL_MISC,0x4194,0x4000);

    // initiate Pause frame source MAC
    XRFISingleWr(MAC_PFSA_0,0x0000);
    XRFISingleWr(MAC_PFSA_1,0x9600);
    XRFISingleWr(MAC_PFSA_2,0xAC9A);

    // RCAL triger 
    // XRFISingleRdMdfWr(CDB_CTRL, 0x9000, 0x9000);  // reset RCAL
    // XRFISingleRdMdfWr(CDB_CTRL, 0x0000, 0x9000);  // remove reset
    XRFISingleRdMdfWr(CDB_BIAS0, 0x8000, 0x8000);  // start RCAL
    XRFISingleRdMdfWr(CDB_BIAS0, 0x0000, 0x8000);  // start RCAL
    

    // power down unused PLL outputs
    XRFISingleRdMdfWr(SYSPLL_CFG_3,0x0038,0x0038);  // SYS_RO_PLL PD all outputs except 1
}


//--------------------------------------
// ETCB_config_slave_if
//--------------------------------------

void  ETCB_config_slave_if(void){

  if (ps_op_md0 == 1){   

	  // SMDIO Configuration
	  tmp =  ((ps_subtype_md43 <<3 | ps_subtype_md210) <<4); 
      XRFISingleRdMdfWr(SMDIO_CFG,tmp,0x01F0);
	
	  //UART Configuration	
	  XRFISingleWr(UART_BD,0x0B87);
      XRFISingleWr(UART_FDIV,0x0064);
      
    }
  	else if (ps_op_md0 == 0) {    	// SSPI Config

		if ((ps_subtype_md210 & 0x4) && (ps_subtype_md43 & 0x1)){
			val = 0 <<1;
			}else {
				val = (4 - ((ps_subtype_md43 <<1) | (ps_subtype_md210>>2)))<<1;
				}

		if(!(ps_subtype_md43 >>1)){
			val |= (0 <<8);
			} else {
			val |= (2 <8);
				}

		val |= 1 | ~(ps_subtype_md210 & 2) << 14 | ~(ps_subtype_md210 &1) << 15;
		
	  	XRFISingleWr(SSPI_CFG,val);   
      	XRFISingleRdMdfWr(GPIO_ALTSEL0,0x003C,0x003C);
	  	XRFISingleRdMdfWr(GPIO_ALTSEL1,0x0000,0x003C);
 
       }
  
}


//--------------------------------------
// ETCB_halt
//--------------------------------------

void    ETCB_halt(void)
{
  XRFISingleRdMdfWr(RESET_STATUS,0x0001,0x0001); // set init bit
  XRFISingleWr(RST_REQ,0x001F);
}


//--------------------------------------
// ETCB_config_unman_mode
//--------------------------------------

void    ETCB_config_unman_mode(void){

	
	if((ps_op_md1 == 1) && (ps_op_md0 == 1)){
		tmp = ps_subtype_md210 & 0xFF;
			
		if(tmp == 0x00){
			val = 0x00 << 4;
		}
		else if (tmp == 0x01){
			val = 0x04 << 4;
		}
		else if (tmp == 0x02){
			val = 0x10 << 4;
		}
		else if (tmp == 0x03){
			val = 0x1F << 4;
		}	
		
		XRFISingleRdMdfWr(SMDIO_CFG,val,0x01F0);   

		//XRFISingleRdMdfWr(GPIO_ALTSEL0,0x003C,0x003C);
  		//XRFISingleRdMdfWr(GPIO_ALTSEL1,0x0000,0x003C);

		tmp = 0x2 << 13;
		XRFISingleRdMdfWr(MII_CFG_5,tmp,0x6000);
		XRFISingleRdMdfWr(MII_CFG_6,tmp,0x6000);

		XRFISingleWr(PHY_ADDR_5,0x32A5);
		XRFISingleWr(PHY_ADDR_6,0x32A6);

		if(ps_subtype_md43 & 0x2 == 0x2){
			tmp = 0x4 << 7 | 0x4 ;
			XRFISingleRdMdfWr(PCDU_5,tmp,0x0387);
			XRFISingleRdMdfWr(PCDU_6,tmp,0x0387);

		}
		// enable switch with 5ports enabled
		XRFISingleWr(GSWIP_CFG,0x8000); 

		}

	else if(ps_op_md1 == 1 && ps_op_md0 == 0){

		tmp = (~ps_op_md0) << 15 | (~ps_op_md1) << 14 | 0x1;
		XRFISingleWr(SSPI_CFG,tmp);   
  		XRFISingleRdMdfWr(GPIO_ALTSEL0,0x003C,0x003C);
  		XRFISingleRdMdfWr(GPIO_ALTSEL1,0x0000,0x003C);

		tmp = 0x2 << 13;
		XRFISingleRdMdfWr(MII_CFG_5,tmp,0x6000);
		XRFISingleRdMdfWr(MII_CFG_6,tmp,0x6000);

		XRFISingleWr(PHY_ADDR_5,0x32A5);
		XRFISingleWr(PHY_ADDR_6,0x32A6);

		if(ps_subtype_md43 & 0x2 == 0x2){
			tmp = 0x4 << 7 | 0x4 ;
			XRFISingleRdMdfWr(PCDU_5,tmp,0x0387);
			XRFISingleRdMdfWr(PCDU_6,tmp,0x0387);

		}
		// enable switch with 5ports enabled
		XRFISingleWr(GSWIP_CFG,0x8000); 

	}	

  	else if(ps_op_md1 == 0){
    
    	XRFISingleRdMdfWr(SMDIO_CFG,0x0000,0x0001);  // disable SMDIO
		XRFISingleWr(UART_BD,0x0B87);
      	XRFISingleWr(UART_FDIV,0x0064);

		tmp = ps_subtype_md43;
    	XRFISingleRdMdfWr(GPHY_GPS_0,tmp,0x0003);          
	    XRFISingleRdMdfWr(GPHY_GPS_1,tmp,0x0003);          
    	XRFISingleRdMdfWr(GPHY_GPS_2,tmp,0x0003);          
    	XRFISingleRdMdfWr(GPHY_GPS_3,tmp,0x0003);          
    	XRFISingleRdMdfWr(GPHY_GPS_4,tmp,0x0003); 
    	
    	XRFISingleRdMdfWr(GPIO_ALTSEL0,0x0030,0x0030);          
    	XRFISingleRdMdfWr(GPIO_ALTSEL1,0x0030,0x0030);
    	XRFISingleRdMdfWr(GPIO_PUDEN,0x0000,0x0030);
	    XRFISingleRdMdfWr(GPIO_OUT,1<<5,0x0020); //PWLED ON
	    XRFISingleRdMdfWr(GPIO_DRIVE1_CFG,0x0020,0x0020); // PWLED 12mA
	    //XRFISingleRdMdfWr(GPIO_OD,((unsigned int) ps_subtype_md210)<<5,0x0020);  //PWLED mode    
	    
	    if (ps_subtype_md43== 0){
	      XRFISingleWr(GPIO2_ALTSEL0,0x7FFF);          
	      XRFISingleWr(GPIO2_PUDEN,0x4000);
	      XRFISingleWr(GPIO2_DRIVE1_CFG,0x7FFF);          
	   	}

	    if (ps_subtype_md43 == 1){
	      XRFISingleWr(GPIO2_ALTSEL0,0x43FF);          
	      XRFISingleWr(GPIO2_PUDEN,0x7C00);
	      XRFISingleWr(GPIO2_DRIVE1_CFG,0x03FF);          
	    }

	    if (ps_subtype_md43 == 2){
	      XRFISingleWr(GPIO2_ALTSEL0,0x7FFF);          
	      XRFISingleWr(GPIO2_PUDEN,0x4000);
	      XRFISingleWr(GPIO2_DRIVE1_CFG,0x7FFF);          
	    }

	    if (ps_subtype_md43 == 3){
	      XRFISingleWr(GPIO2_ALTSEL0,0x43FF);          
	      XRFISingleWr(GPIO2_PUDEN,0x7C00);
	      XRFISingleWr(GPIO2_DRIVE1_CFG,0x03FF);          
	    }

    	//XRFISingleWr(GPIO2_OD,0x7FFF);  //initial setting
    	//XRFISingleWr(LED_MD_CFG,0x0000);  //initial setting

		/*
    
    	if ((ps_subtype_md210 & 1) == 0){
        XRFISingleRdMdfWr(GPIO2_OD,0x0000,0x001F);  //bits 0,1,2,3,4
        XRFISingleRdMdfWr(LED_MD_CFG,0x7FFF,0x001F);  
        }
    
    	if ((ps_subtype_md210 & 2) == 0){
        XRFISingleRdMdfWr(GPIO2_OD,0x0000,0x03E0);  //bits 5,6,7,8,9
        XRFISingleRdMdfWr(LED_MD_CFG,0x7FFF,0x03E0);  
        }
    
    	if ((ps_subtype_md210 & 4) == 0){
        XRFISingleRdMdfWr(GPIO2_OD,0x0000,0x7C00);  //bits 10,11,12,13,14
        XRFISingleRdMdfWr(LED_MD_CFG,0x7FFF,0x7C00);  
        } */
    
    	XRFISingleWr(PCE_PCTRL_2_P3,0x0001);
    	XRFISingleWr(PCE_PCTRL_2_P4,0x0001);
    
    	XRFISingleWr(BM_WRED_GTH_0,0x0100);
    	XRFISingleWr(BM_WRED_GTH_1,0x0100);

    	XRFISingleWr(PCE_PMAP_2,0x003F);
    	XRFISingleWr(PCE_PMAP_3,0x003F);

    	XRFISingleWr(SDMA_PFCTR8_0,0x0018);
    	XRFISingleWr(SDMA_PFCTR8_1,0x0018);
    	XRFISingleWr(SDMA_PFCTR8_2,0x0018);
    	XRFISingleWr(SDMA_PFCTR8_3,0x0018);
    	XRFISingleWr(SDMA_PFCTR8_4,0x0018);
    
    	XRFISingleWr(SDMA_PFCTR9_0,0x001E);
    	XRFISingleWr(SDMA_PFCTR9_1,0x001E);
    	XRFISingleWr(SDMA_PFCTR9_2,0x001E);
    	XRFISingleWr(SDMA_PFCTR9_3,0x001E);
    	XRFISingleWr(SDMA_PFCTR9_4,0x001E);
    
    	XRFISingleWr(SDMA_FCTHR1,0x03FF);
    	XRFISingleWr(SDMA_FCTHR2,0x03FF);
    	XRFISingleWr(SDMA_FCTHR3,0x03FF);
    	XRFISingleWr(SDMA_FCTHR4,0x03FF);
    
    	// buffer reservation
    	for (ix = 0; ix < 32; ix++) {
      	while ( (XRFISingleRd(BM_RAM_CTRL) & 0x8000) != 0 ) {
		;
      	}
      		XRFISingleWr(BM_RAM_ADDR,(unsigned int) ix<<3);
      		XRFISingleWr(BM_RAM_VAL_0,0x001E);
      		XRFISingleWr(BM_RAM_CTRL,0x8029);
    	}

    	// WRED min/max for green
    	for (ix = 0; ix < 32; ix++) {
      	while ( (XRFISingleRd(BM_RAM_CTRL) & 0x8000) != 0 ) {
		;
      	}
      		XRFISingleWr(BM_RAM_ADDR,((unsigned int) ix<<3)+1);
      		XRFISingleWr(BM_RAM_VAL_0,0x03FF);
      		XRFISingleWr(BM_RAM_VAL_1,0x03FF);
      		XRFISingleWr(BM_RAM_CTRL,0x8029);

	  
    	}

		//Queue Weight for each queue
	  	//TBU

		// enable switch with 5ports enabled
    	XRFISingleWr(GSWIP_CFG,0x8000); 

	}
			
}


//--------------------------------------
// ETCB_reboot
//--------------------------------------

void ETCB_reboot(void)
{
// unsinged int data;

  XRFISingleRdMdfWr(RESET_STATUS,0x0011,0x0011); // set init bit
  data = XRFISingleRd(GPHY_FCR_4);
  if (data == 0x4000) {
        XRFISingleWr(RST_REQ,0x0010);
  }
  else {
        XRFISingleWr(RST_REQ,0x1000);
  }
}


//--------------------------------------
// ETCB_fuse_download
//--------------------------------------

void  ETCB_fuse_download(void){

//  unsigned int addr;
//  unsigned int data;
//  unsigned int enable;
//  unsigned int fuse_addr;

  fuse_addr = FUSE0;

  addr = XRFISingleRd(fuse_addr);
  fuse_addr = fuse_addr + 1;
  data = XRFISingleRd(fuse_addr);
  fuse_addr = fuse_addr + 1;
  enable = XRFISingleRd(fuse_addr);
  addr = addr + 1;

  while( (addr != 0) && (fuse_addr<FUSE28) ){
    XRFISingleRdMdfWr(addr,data,enable);

    addr = XRFISingleRd(fuse_addr);
    fuse_addr = fuse_addr + 1;
    data = XRFISingleRd(fuse_addr);
    fuse_addr = fuse_addr + 1;
    enable = XRFISingleRd(fuse_addr);
    addr = addr + 1;
  }
}


//--------------------------------------
// ETCB_fd_incremental
//--------------------------------------

void ETCB_fd_incremental(void) {                

//  unsigned int addr;
//  unsigned int data;
//  unsigned int ix;
//  unsigned int f_addr;

  ix = noce;
  f_addr = flash_addr;
  addr = ETCB_flashRd(f_addr);

  while( ix != 0 ){  
    ix = ix -1;
    
    f_addr = f_addr+2;
    data = ETCB_flashRd(f_addr);
    
    XRFISingleWr(addr,data);
    
    addr = addr +1;
  }
}

//--------------------------------------
// ETCB_fd_pairs
//--------------------------------------

void ETCB_fd_pairs(void) {

//  unsigned int addr;
//  unsigned int data;
//  unsigned int ix;
//  unsigned int f_addr;

  ix = noce;
  f_addr = flash_addr;

  while( ix != 0 ){  
    ix = ix -1;
    
    addr = ETCB_flashRd(f_addr);
    f_addr = f_addr+2;
    data = ETCB_flashRd(f_addr);
    f_addr = f_addr+2;
    
    XRFISingleWr(addr,data);
    
  }
}

 
//--------------------------------------
// ETCB_fd_triplets
//--------------------------------------

void ETCB_fd_triplets(void) {

//  unsigned int addr;
//  unsigned int data;
//  unsigned int enable;
//  unsigned int ix;
//  unsigned int f_addr;
//
  ix = noce;
  f_addr = flash_addr;

  while( ix != 0 ){  
    ix = ix -1;
    
    addr = ETCB_flashRd(f_addr);
    f_addr = f_addr+2;
    data = ETCB_flashRd(f_addr);
    f_addr = f_addr+2;
    enable = ETCB_flashRd(f_addr);
    f_addr = f_addr+2;
    
    XRFISingleRdMdfWr(addr,data,enable);
    
  }
}

  
//--------------------------------------
// ETCB_fd_copy
//--------------------------------------

void ETCB_fd_copy(void) {

//  unsigned int addr;
//  unsigned long int data_long;  // warning 32-bits
//  unsigned int enable;
//  unsigned char shift;
//  unsigned char ix;
//  unsigned int f_addr;

  ix = noce;
  f_addr = flash_addr;

  while( ix != 0 ){  
   ix = ix -1;
    
    addr = ETCB_flashRd(f_addr); // read source addr
    data_long = (unsigned long int) XRFISingleRd(addr);
    f_addr = f_addr+2;
    addr = ETCB_flashRd(f_addr); // read destination addr
    f_addr = f_addr+2;
    enable = ETCB_flashRd(f_addr); // read destination enable
    f_addr = f_addr+2;
    shift = (unsigned char) ETCB_flashRd(f_addr); // read shift
    f_addr = f_addr+2;

    for (ix = 0; ix < (shift & 0x7f); ix++) {
      data_long = data_long<<1;  
    }

    if ((shift>>7) == 1){
      data_long = ~data_long;
    }

    XRFISingleRdMdfWr(addr,(unsigned int) (data_long>>16),enable);
   }
}

 
//--------------------------------------
// ETCB_fd_conditional_wait
//--------------------------------------

void ETCB_fd_conditional_wait(void) {

//  unsigned int ix;
//  unsigned int addr;
//  unsigned int data;
//  unsigned int enable;
//  unsigned int f_addr;

  f_addr = flash_addr;

  addr = ETCB_flashRd(f_addr); // read addr
  f_addr = f_addr+2;
  data = ETCB_flashRd(f_addr); // read data
  f_addr = f_addr+2;
  enable = ETCB_flashRd(f_addr); // read mask

  while( (XRFISingleRd(addr) & enable) != ( data & enable) ){  
    for (ix = 0; ix < 0xFF; ix++) {  // wait few ms
      ;
    }
  }
}

//--------------------------------------
// ETCB_fd_conditional_jump
//--------------------------------------

void ETCB_fd_conditional_jump(void) {

//  unsigned int addr;
//  unsigned int data;
//  unsigned int enable;
//  unsigned int offset;
//  unsigned int f_addr;

  f_addr = flash_addr;

  addr = ETCB_flashRd(f_addr); // read addr
  f_addr = f_addr+2;
  data = ETCB_flashRd(f_addr); // read data
  f_addr = f_addr+2;
  enable = ETCB_flashRd(f_addr); // read mask
  f_addr = f_addr+2;
  offset = ETCB_flashRd(f_addr); // read offset

  if( (XRFISingleRd(addr) & enable) != ( data & enable) ){ 
    offset = 0x0000;
  }
}


//--------------------------------------
// ETCB_fd_ssb
//--------------------------------------

void ETCB_fd_ssb(unsigned int gphy_mask) {

//  unsigned int data;
//  unsigned int addr;
//  unsigned int ix;
//  unsigned int f_addr;

  ix = noce; // two bytes in single cycle
  f_addr = flash_addr;
  addr = 0xFFFF; // first SSB address

  while( ix != 0 ){  
    ix = ix -1;
    
    data = ETCB_flashRd(f_addr);

    f_addr = f_addr+2;

    XRFISingleWr(ETHSW_SSB_ADDR,addr); //SSB addr
    XRFISingleWr(ETHSW_SSB_DATA,data); //SSB data
    XRFISingleWr(ETHSW_SSB_MODE,0x0001); //SSB write command

    addr = addr -1; // write backwards
  }

  // reduce number of SSB segments to be used by switch
  XRFISingleWr(BM_FSQM_GCTRL, 510 - (noce>>7));  // bug fixed from 510 - (noce>>8)
  XRFISingleWr(BM_GCTRL, 0xE049);

  // point GPHY CPU's to begining of SSB
  // zero is active
  if ((gphy_mask & 0x0001) == 0) {
    XRFISingleWr(GPHY_FCR_0,0x2000);  
  }     
  if ((gphy_mask & 0x0002) == 0) {
    XRFISingleWr(GPHY_FCR_1,0x2000);          
  }     
  if ((gphy_mask & 0x0004) == 0) {
    XRFISingleWr(GPHY_FCR_2,0x2000);          
  }     
  if ((gphy_mask & 0x0008) == 0) {
    XRFISingleWr(GPHY_FCR_3,0x2000);          
  }     
  if ((gphy_mask & 0x0010) == 0) {
    XRFISingleWr(GPHY_FCR_4,0x2000); 
  }     
}


//--------------------------------------
// ETCB_fd_eeprom
//--------------------------------------

void ETCB_fd_eeprom(unsigned int gphy_mask) {

  //  unsigned int fcr_val;

  fcr_val = (unsigned int) (0x8000 | ((flash_addr>>4) & 0x3FFF));

  // eeprom code must start on address that is multiple of 16
  // if block does not start at such address, padding is require (upto 15 Bytes)
  if ((flash_addr & 0x0000000F) != 0){
    fcr_val = fcr_val +1;
  }

  // point GPHY CPU's to begining of EEPROM CODE
  // zero is active
  if ((gphy_mask & 0x0001) == 0) {
    XRFISingleWr(GPHY_FCR_0,fcr_val);  
  }     
  if ((gphy_mask & 0x0002) == 0) {
    XRFISingleWr(GPHY_FCR_1,fcr_val);          
  }     
  if ((gphy_mask & 0x0004) == 0) {
    XRFISingleWr(GPHY_FCR_2,fcr_val);          
  }     
  if ((gphy_mask & 0x0008) == 0) {
    XRFISingleWr(GPHY_FCR_3,fcr_val);          
  }     
  if ((gphy_mask & 0x0010) == 0) {
    XRFISingleWr(GPHY_FCR_4,fcr_val);  
  }     
}


//--------------------------------------
// ETCB_fd_parsercode
//--------------------------------------

void ETCB_fd_parsercode(void) {                

//  unsigned int addr;
//  unsigned int data;
//  unsigned int ix;
//  unsigned int f_addr;

  ix = noce;
  f_addr = flash_addr;
  addr = 0;

  XRFISingleRdMdfWr(PCE_GCTRL_0,0x00000,0x00080 ); // invalidate microcode (bit 3 = 0)

  while( ix != 0 ){  
    ix = ix -1;
    
    // PCE_TBL_VAL_3
    f_addr = f_addr+2;
    data = ETCB_flashRd(f_addr);
    XRFISingleWr(PCE_TBL_VAL_3,data);
    
    // PCE_TBL_VAL_2
    f_addr = f_addr+2;
    data = ETCB_flashRd(f_addr);
    XRFISingleWr(PCE_TBL_VAL_2,data);
    
    // PCE_TBL_VAL_1
    f_addr = f_addr+2;
    data = ETCB_flashRd(f_addr);
    XRFISingleWr(PCE_TBL_VAL_1,data);
    
    // PCE_TBL_VAL_0
    f_addr = f_addr+2;
    data = ETCB_flashRd(f_addr);
    XRFISingleWr(PCE_TBL_VAL_0,data);
    
    // PCE_TBL_ADDR
    XRFISingleWr(PCE_TBL_ADDR,addr);
    addr = addr +1;

    // PCE_TBL_CTRL
    XRFISingleWr(PCE_TBL_CTRL, 0x8020);
  }

  XRFISingleRdMdfWr(PCE_GCTRL_0,0x00080,0x00080 ); // validate microcode  (bit 3 = 1)
}


  
//--------------------------------------
// ETCB_flash_download
//--------------------------------------

void ETCB_flash_download(void) {

//  unsigned int noce;
//  unsigned int type;
//  unsigned int flash_addr;
//  unsigned int flash_addr_high;
//  unsigned int increment;
//  unsigned char multipland;
//  unsigned int offset;
//  unsigned int old_flash_addr;
//  unsigned char match;
//  unsigned char jx;

  flash_addr = 8;

  noce = ETCB_flashRd(flash_addr);
  flash_addr = flash_addr+2;

  type = ETCB_flashRd(flash_addr);
  flash_addr = flash_addr + 2;

  match = 1; // init cannot be 0 as while loop checks against 0

  // repeat until NOCE == 0
  while ((noce != 0x0000) && (noce != 0xFFFF) && (match != 0)) {

    match = 0;  // handling no match kind of situation
    increment = 0; 
    multipland = 1;

    // Incremental Access Type 1111    -changed from 0000
    if (type == 0x1111) {
      ETCB_fd_incremental();
      increment = noce +1;
      multipland = 2;
      match = 1;
    }

    //  Single Access Without Write EnableType 2222  -changed from FFFF
    if (type == 0x2222) {
      ETCB_fd_pairs();
      increment = noce;
      multipland = 4;
      match = 2;
    }

    //  Single Access With Mask Type 6666
    if (type == 0x6666) {
      ETCB_fd_triplets();
      increment = noce;
      multipland = 6;
      match = 3;
    }

    //  Conditional Wait 5555
    if (type == 0x5555) {
      ETCB_fd_conditional_wait();
      increment = 3;
      multipland = 2;
      match = 4;
    }

    //  Conditional Jump AAAA
    if (type == 0xAAAA) {
      ETCB_fd_conditional_jump();
      increment = 4;
      multipland = 2;
      match = 5;

      // apply offset:  new_addr = old_addr + 2*offset    (offset is signed number)
      if ((offset>>15) == 1) {  // NEGATIVE OFFSET
	offset = (~offset) +1;          // offset = -offset
	flash_addr = flash_addr - offset; // minus offset
	flash_addr = flash_addr - offset ; // minus offset
      }
      else {
	flash_addr = flash_addr + offset; // plus offset
	flash_addr = flash_addr + offset; // plus offset
      }
    }

    //  GPHY code download to SSB 8000
    if ((type & 0xFFE0) == 0x8000) {
      ETCB_fd_ssb(type & 0x001F );
      increment = noce;
      multipland = 2;
      match = 6;
    }

    //  GPHY code run from EEPROM/flash 7000  !!! WARNING: start of actual code must be block 16 alligned !!!
    if ((type & 0xFFE0) == 0x7000) {
      ETCB_fd_eeprom(type & 0x001F);
      increment = noce;
      multipland = 2;
      match = 7;
    }

    //  do an unmanaged config from EEPROM 9999
    if (type == 0x9999) {
      ETCB_config_unman_mode();
      increment = 0;
      multipland = 2;
      match = 8;
    }

    //  do a fuse download from EEPROM CCCC
    if (type == 0xCCCC) {
      ETCB_fuse_download();
      increment = 0;
      multipland = 2;
      match = 9;
    }

    //  Copy DDDD
    if (type == 0xDDDD) {
      ETCB_fd_copy();
      increment = noce;
      multipland = 8;
      match = 11;
    }

    // PARSER CODE DOWNLOAD 3333 -- added for A21 only
    if (type == 0x3333) {
      ETCB_fd_parsercode();
      increment = noce;
      multipland = 8;
      match = 12;
    }

    // new flash address calculation
    for (jx = 0; jx < multipland; jx++) {  // repeat addition that many times
      flash_addr = flash_addr + increment;
    }

    // NOCE
    noce = ETCB_flashRd(flash_addr);
    flash_addr = flash_addr+2;
    // TYPE
    type = ETCB_flashRd(flash_addr);
    flash_addr = flash_addr+2;
    
  }
}

void led_init()
{

	
	//GPIO_ALTSEL0.1 and GPIO_ALTSEL1.1
	XRFISingleWr(GPIO_ALTSEL0, 0x0002);
	XRFISingleWr(GPIO_ALTSEL1, 0x003C);

	//LED CTRL PIN GPIO30 Input Pin
	//GPIO2_ALTSEL0.1 and ALT.SEL1.1
	XRFISingleWr(GPIO2_ALTSEL0, 0x0000);
	XRFISingleWr(GPIO2_ALTSEL1, 0x0030);

	//GPIO2.1 - Output and GPIO2.14 - Input
	XRFISingleWr(GPIO2_DIR, 0x0002);
	XRFISingleWr(GPIO2_OUT, 0x0002);

}

void delay()
{
	unsigned int i;
	unsigned int j;

	for(i=0;i<1000;i++)
		for(j=0;j<10000;j++);

}

unsigned int read_input(){
	tmp = XRFISingleRd(GPIO2_IN);
	return( tmp & 0x4000);
}

//------------------------------------------------------------------------------------------------------------//
// MAIN()   MAIN()     MAIN()    MAIN()   MAIN()     MAIN()    MAIN()   MAIN()     MAIN()    MAIN()   MAIN()  //
//------------------------------------------------------------------------------------------------------------//


//--------------------------------------
// main() function declaration
//--------------------------------------

void main() {


//--------------------------------------
// variable declaration
//--------------------------------------

//  unsigned int ps0_val;
//  unsigned int ps1_val;
//
//  unsigned char ps_xtal;
//  unsigned char ps_nowait;
//  unsigned char ps_slave_type;
//  unsigned char ps_subtype_md;
//  unsigned char ps_led_md;
//  unsigned char ps_pw_sv;          
//
//  unsigned char flash_detected;          


//--------------------------------------
// Pin-Strap loading
//--------------------------------------
  ps0_val = XRFISingleRd(PS0);
  ps1_val = XRFISingleRd(PS1);

  ps_xtal       		= (unsigned char) (ps0_val>> 3) & 1;  
  ps_op_md1     		= (unsigned char) (ps0_val>> 7) & 1;      
  ps_subtype_md43      	= (unsigned char) (ps0_val>> 8) & 3;    // 2-bit value 9:8
  ps_nowait     		= (unsigned char) (ps1_val>>10) & 1;     
  ps_op_md0		 		= (unsigned char) (ps1_val>>11) & 1; 
  ps_subtype_md210 		= (unsigned char) (ps1_val>>12) & 7;    // 3-bit value 14:12


//--------------------------------------
// ETCB_gphy_init
//--------------------------------------
  

  //First State - Wait for User Input to Begin the Boot Code Execution
  val = 0;
  unsigned short int data;
  led_init();
  for(;;){
  	data =  XRFISingleRd(GPIO2_IN);
	
  	}
  	
  while(read_input() == 0x4000)
  {
  		delay();
		XRFISingleWr(GPIO2_OUT, 0x0000);
		delay();
		XRFISingleWr(GPIO2_OUT, 0x0002);
  }
  
  ETCB_gphy_init();


//--------------------------------------
// ETCB_config_slave_if
//--------------------------------------

  if (ps_nowait == 0) {
    ETCB_config_slave_if();
  }

//--------------------------------------
// ETCB_fuse_download
//--------------------------------------

  if (ps_nowait == 0) {
    ETCB_fuse_download();
  }


//--------------------------------------
// ETCB_halt
//--------------------------------------

  if (ps_nowait == 0) {
    while(1) {
      ETCB_halt();
    }
  }


//--------------------------------------
// ETCB_detect_flash
//--------------------------------------

  flash_detected = ETCB_detect_flash();    // also programs MSPI_CFG.ADDRMD and MSPI_CFG.CLKDIV


//--------------------------------------
// ETCB_config_unman_mode
//--------------------------------------

  if (flash_detected == 0) {
    ETCB_config_unman_mode();
  }


//--------------------------------------
// ETCB_fuse_download
//--------------------------------------

  ETCB_fuse_download();


//--------------------------------------
// ETCB_flash_download
//--------------------------------------

  if (flash_detected == 1) {
    ETCB_flash_download();   // boot-code may terminate here if flash issues reset from within
  }


//--------------------------------------
// ETCB_reboot
//--------------------------------------

  while(1) {
    ETCB_reboot();
  }

//--------------------------------------
// The End
//--------------------------------------


}
