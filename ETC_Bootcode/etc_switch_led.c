// --------------------------------------
// 8051uC Code example code for toggling LED
// --------------------------------------

#include <mcs51/8051.h>
#include <compiler.h>
#include <stdio.h>
#include <ctype.h>

#include <flow25g_regdef.h>
#include <flow25g_xrfi_proc.h>

void delay()
{
	unsigned int i,j;
	for(i=0;i<1000;i++)
		for(j=0;j<1000;j++);
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
unsigned int read_input()
{
	unsigned int data;
	delay();
	data =  XRFISingleRd(GPIO2_IN);
	return (data &0x4000);
}

void main()
{
	//First State - Wait for User Input to Begin the Boot Code Execution
	
	unsigned int val;
	led_init();
	val = 0x0000;
	for(;;){
		
		if (read_input() == 0){
			XRFISingleWr(GPIO2_OUT, val);
			val = ~val & 0x0002;
		}	
	
  	}
  	
}