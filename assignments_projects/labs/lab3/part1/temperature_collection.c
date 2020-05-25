#include "contiki.h"
#include <stdio.h>
#include "sys/node-id.h"         // to get node_id (uint16_t)
#include "net/netstack.h"        // for sending data
#include "net/nullnet/nullnet.h" // for nullnet (set buffer size, content and call back function)
#include <string.h>              // for memcpy
#include <random.h>              // for generating random number

/*-- Configurations --*/
#define SEND_INTERVAL (120 * CLOCK_SECOND) // type : long unsigned int
#define CENTRAL_NODE 25                     // type: int
#define NODES ((CENTRAL_NODE * 2) - 1)
/*---------------------------------------------------------------------------*/
static struct etimer timer;
struct node_temperature
{
    short temperature;
    uint16_t node_id;
    unsigned short packet_id;
};
struct node_temperature nd_tp;

unsigned long temperatures[NODES + 1]; // Array size will be (NODES+1), because index 0 is not used as a node_id
static short max_teperature = -101;
static unsigned long last_update_time = 0;

/*---------------------------------------------------------------------------*/

void input_callback(const void *data, uint16_t len, const linkaddr_t *src, const linkaddr_t *dest)
{
    if (len == sizeof(nd_tp))
    {
        struct node_temperature obj;
        memcpy(&obj, data, sizeof(obj));
        /* Own packet and same packet will not be processed*/
        if (obj.node_id != node_id && temperatures[obj.node_id] < obj.packet_id) // to avoid Broadcast Strom
        {
            // storing time, node_id is index here
            temperatures[obj.node_id] = obj.packet_id;
            if (node_id == CENTRAL_NODE)
            {
                /*Reseting max_temperature in every 60 seconds*/
                if ((clock_seconds() - last_update_time) > 60)
                {
                    max_teperature = -101;
                }
                last_update_time = clock_seconds();
                if (max_teperature < obj.temperature)
                {
                    max_teperature = obj.temperature;
                }
                printf("%d,%u\n", obj.packet_id, obj.node_id);  
                printf("Max:%d \n", max_teperature);             
            }
            else
            {
                // not a CENTRAL NODE , need Flooding
                nd_tp = obj;
                NETSTACK_NETWORK.output(NULL);
            }
        }
    }
}

short generate_random_number()
{
    return (random_rand() % 200) - 100;
}

/*---------------------------------------------------------------------------*/
PROCESS(temperature_collection, "Temperature collection");
AUTOSTART_PROCESSES(&temperature_collection);
/*---------------------------------------------------------------------------*/

PROCESS_THREAD(temperature_collection, ev, data)
{
    PROCESS_BEGIN();
    /* Initialize NullNet */
    nullnet_buf = (uint8_t *)&nd_tp;
    nullnet_len = sizeof(nd_tp);
    nullnet_set_input_callback(input_callback);
    // We will not broadcast from Central node
    printf("0\n");
    if (node_id != CENTRAL_NODE)
    {
        static unsigned short slave_packet_counter = 0;
        etimer_set(&timer, SEND_INTERVAL);
        while (1)
        {
            PROCESS_WAIT_EVENT_UNTIL(etimer_expired(&timer));
            slave_packet_counter++;
            short temperature = generate_random_number();
            nd_tp.node_id = node_id;
            nd_tp.temperature = temperature;
            printf("%d,%u\n",slave_packet_counter,node_id);
            printf("%d\n", temperature);
            nd_tp.packet_id = slave_packet_counter;
            NETSTACK_NETWORK.output(NULL); // Broadcasting here
             // used a random delay to initialize, because if I start every node in same milisends packet lost increase
            etimer_set(&timer, SEND_INTERVAL - CLOCK_SECOND + (random_rand() % (2 * CLOCK_SECOND)));
        }
    }
    PROCESS_END();
}
/*--------------------------------------------------------------------------------*/