#include "contiki.h"
#include <stdio.h> //printf
#include "dev/leds.h" // for leds
#include "sys/node-id.h" // to get node_id
#include "net/netstack.h"  // for sending data
#include "net/nullnet/nullnet.h" // for nullnet
#include <string.h> // for memcpy
#include <random.h> // for generating random number
#include "sys/log.h"

/*-- Configurations --*/
#define SEND_INTERVAL (20 * CLOCK_SECOND) 
#define CENTRAL_NODE 5

#define LOG_MODULE "Lab2"
#define LOG_LEVEL LOG_LEVEL_INFO

void toggle_led(unsigned);

/*---------------------------------------------------------------------------*/

static unsigned int recv_pkt_counter = 0;
static unsigned int pkt_loss = 0;
static struct etimer timer;
struct complex_data
{
    unsigned short led_number;
    uint16_t n_id;
    unsigned int pkt_counter;
   // unsigned long clock_seconds()
};
struct complex_data c_data;
/*---------------------------------------------------------------------------*/
void input_callback(const void *data, uint16_t len,
  const linkaddr_t *src, const linkaddr_t *dest)
{
    if(len == sizeof(c_data) && node_id != CENTRAL_NODE) {
        struct complex_data received_data;
        memcpy(&received_data, data, sizeof(received_data));
        if( recv_pkt_counter < received_data.pkt_counter){
            pkt_loss = pkt_loss + (received_data.pkt_counter - recv_pkt_counter -1);
            recv_pkt_counter = received_data.pkt_counter;
            printf("%u,%u\n", received_data.pkt_counter,pkt_loss);
            c_data = received_data;
            NETSTACK_NETWORK.output(NULL);
            toggle_led(received_data.led_number);
        }
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

unsigned short generate_random_number(){
    return random_rand()%3 + 1;
}
/*---------------------------------------------------------------------------*/
PROCESS(lab1, "Lab1 of IoTWN");
AUTOSTART_PROCESSES(&lab1);
/*---------------------------------------------------------------------------*/

PROCESS_THREAD(lab1, ev, data)
{
    static unsigned int send_packet_counter = 1;
    PROCESS_BEGIN();
    /* Initialize NullNet */
    nullnet_buf = (uint8_t *)&c_data;
    nullnet_len = sizeof(c_data);
    
    nullnet_set_input_callback(input_callback);

    etimer_set(&timer, SEND_INTERVAL);
    while(1){
        PROCESS_WAIT_EVENT_UNTIL(etimer_expired(&timer));
        unsigned short led_number = generate_random_number();
        if(node_id == CENTRAL_NODE){
            toggle_led(led_number);
            c_data.n_id = node_id;
            c_data.led_number = led_number;
            c_data.pkt_counter = send_packet_counter;
            NETSTACK_NETWORK.output(NULL);
            printf("bCast#: %u\n",send_packet_counter);
            send_packet_counter++;
        }
        etimer_reset(&timer);
    }
    PROCESS_END();
}
/*--------------------------------------------------------------------------------*/

