#include "contiki.h"
#include <stdio.h>
#include "sys/node-id.h" // to get node_id
#include "net/netstack.h"  // for sending data
#include "net/nullnet/nullnet.h" // for nullnet (set buffer size, content and call back function)
#include <string.h> // for memcpy
#include <random.h> // for generating random number

/*-- Configurations --*/
#define SEND_INTERVAL (1 * CLOCK_SECOND) 
static linkaddr_t dest_addr =  {{ 0x01, 0x01, 0x01, 0x00, 0x01, 0x74, 0x12, 0x00 }};
/*---------------------------------------------------------------------------*/
static struct etimer timer;
struct node_temperature
{
    short temperature;
    uint16_t n_id;
};

struct node_temperature nd_tp;
static short temperatures[6];
static unsigned short packet_counter;
/*---------------------------------------------------------------------------*/
short get_avg(){
    return  (temperatures[2] + temperatures[3] + temperatures[4] + temperatures[5])/4;
}
 
void input_callback(const void *data, uint16_t len,
  const linkaddr_t *src, const linkaddr_t *dest)
{
    if(len == sizeof(nd_tp)) {
        struct node_temperature obj;
        memcpy(&obj, data, sizeof(obj));
        temperatures[obj.n_id] = obj.temperature;
        packet_counter++;
        if(packet_counter == 4){
            packet_counter = 0;
            printf("Temperatures: %d, %d, %d, %d \n",temperatures[2],  temperatures[3] , temperatures[4] , temperatures[5]);
            printf("Average: %d \n",get_avg());
        }
    }
}

short generate_random_number(){
    return (random_rand()%200)-100;
}
/*---------------------------------------------------------------------------*/
PROCESS(lab1_part2, "");
AUTOSTART_PROCESSES(&lab1_part2);
/*---------------------------------------------------------------------------*/

PROCESS_THREAD(lab1_part2, ev, data)
{
    PROCESS_BEGIN();
    packet_counter = 0;
    /* Initialize NullNet */
   
    nullnet_buf = (uint8_t *)&nd_tp;
    nullnet_len = sizeof(nd_tp);
    nullnet_set_input_callback(input_callback);

    etimer_set(&timer, SEND_INTERVAL);
    while(1){
        PROCESS_WAIT_EVENT_UNTIL(etimer_expired(&timer));
        if(node_id>=2 && node_id <= 5){
            short temperature = generate_random_number();
            nd_tp.n_id = node_id;
            nd_tp.temperature = temperature;
            printf("Temperature: %d\n",temperature);
            NETSTACK_NETWORK.output(&dest_addr);
        }
        etimer_reset(&timer);
    }
    PROCESS_END();
}
/*--------------------------------------------------------------------------------*/