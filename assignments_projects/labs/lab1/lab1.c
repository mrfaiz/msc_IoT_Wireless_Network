#include "contiki.h"
#include <stdio.h> //printf
#include "dev/leds.h" // for leds
#include "sys/node-id.h" // to get node_id
#include "net/netstack.h"  // for sending data
#include "net/nullnet/nullnet.h" // for nullnet
#include <string.h> // for memcpy
#include <random.h> // for generating random number

/*-- Configurations --*/
#define SEND_INTERVAL (1 * CLOCK_SECOND) 
void toggle_led(unsigned);

/*---------------------------------------------------------------------------*/
static struct etimer timer;
/*---------------------------------------------------------------------------*/
void input_callback(const void *data, uint16_t len,
  const linkaddr_t *src, const linkaddr_t *dest)
{
    if(len == sizeof(unsigned)) {
        unsigned count;
        memcpy(&count, data, sizeof(count));
        printf("Received %u \n", count);
        toggle_led(count);
    }
}

void toggle_led(unsigned count){
        switch (count)
        {
        case 1:
            leds_toggle(LEDS_RED);
            break;
        case 2:
            leds_toggle(LEDS_GREEN);
            break;
        case 3:
            leds_toggle(LEDS_YELLOW);
            break;
        default:
            leds_on(LEDS_RED);
            leds_on(LEDS_GREEN);
            leds_on(LEDS_YELLOW);
            break;
        }
}

unsigned generate_random_number(){
    return random_rand()%3 + 1;
}
/*---------------------------------------------------------------------------*/
PROCESS(lab1, "Lab1 of IoTWN");
AUTOSTART_PROCESSES(&lab1);
/*---------------------------------------------------------------------------*/

PROCESS_THREAD(lab1, ev, data)
{
    static unsigned counter = 0;
    PROCESS_BEGIN();
    /* Initialize NullNet */
    nullnet_buf = (uint8_t *)&counter;
    nullnet_len = sizeof(counter);
    
    nullnet_set_input_callback(input_callback);

    etimer_set(&timer, SEND_INTERVAL);
    while(1){
        PROCESS_WAIT_EVENT_UNTIL(etimer_expired(&timer));
        counter = generate_random_number();
        if(node_id == 1){
            toggle_led(counter);
            NETSTACK_NETWORK.output(NULL);
            printf("broadcasting %u\n",counter);
        }
        etimer_reset(&timer);
    }
    PROCESS_END();
}
/*--------------------------------------------------------------------------------*/