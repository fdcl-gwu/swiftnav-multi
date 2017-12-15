#include <stdio.h>
#include <stdint.h>
#include <stdlib.h>
#include <string.h>
#include <unistd.h>

#include <libserialport.h>

#include <libsbp/sbp.h>
#include <libsbp/system.h>

char *serial_port_name = NULL;
struct sp_port *piksi_port = NULL;
static sbp_msg_callbacks_node_t heartbeat_callback_node;


void usage(char *prog_name) {
  /* Help string for -h argument */
  fprintf(stderr, "usage: %s [-p path/to/serial/port][-b baud_rate]\n"
          "default values:\n"
          "\t-p = /dev/ttyUSB0\n"
          "\t-b = 115200\n", prog_name);
}


void setup_port(int baud)
{
  /* set the serial port options for the Piksi */

  printf("Attempting to configure the serial port...\n");

  int result;

  // set baud rate
  result = sp_set_baudrate(piksi_port, baud);
  if (result != SP_OK) {
    fprintf(stderr, "Cannot set port baud rate!\n");
    exit(EXIT_FAILURE);
  }
  printf("Configured the baud rate...\n");

  // set flow control
  result = sp_set_flowcontrol(piksi_port, SP_FLOWCONTROL_NONE);
  if (result != SP_OK) {
    fprintf(stderr, "Cannot set flow control!\n");
    exit(EXIT_FAILURE);
  }
  printf("Configured the flow control...\n");

  // set bit size
  result = sp_set_bits(piksi_port, 8);
  if (result != SP_OK) {
    fprintf(stderr, "Cannot set data bits!\n");
    exit(EXIT_FAILURE);
  }
  printf("Configured the number of data bits...\n");

  // set parity
  result = sp_set_parity(piksi_port, SP_PARITY_NONE);
  if (result != SP_OK) {
    fprintf(stderr, "Cannot set parity!\n");
    exit(EXIT_FAILURE);
  }
  printf("Configured the parity...\n");

  // set stop bits
  result = sp_set_stopbits(piksi_port, 1);
  if (result != SP_OK) {
    fprintf(stderr, "Cannot set stop bits!\n");
    exit(EXIT_FAILURE);
  }
  printf("Configured the number of stop bits... done.\n");

}


void heartbeat_callback(u16 sender_id, u8 len, u8 msg[], void *context)
{
  (void)sender_id, (void)len, (void)msg, (void)context;
  fprintf(stdout, "%s\n", __FUNCTION__);
}


u32 piksi_port_read(u8 *buff, u32 n, void *context)
{
  (void)context;
  u32 result;

  result = sp_blocking_read(piksi_port, buff, n, 0);

  return result;
}


int main(int argc, char **argv)
{
  int opt;
  int result = 0;

  sbp_state_t s;

  // parse the args
  serial_port_name = "/dev/ttyUSB0";
  unsigned int baud = 115200;
  while ((opt = getopt(argc, argv, "pb:h")) != -1) {
    switch (opt) {
      case 'p':
        serial_port_name = (char *)calloc(strlen(optarg) + 1, sizeof(char));
        if (!serial_port_name) {
          fprintf(stderr, "Cannot allocate memory!\n");
          exit(EXIT_FAILURE);
        }
        strcpy(serial_port_name, optarg);
        break;
      case 'b':
        baud = atoi(optarg);
        break;
      case 'h':
        usage(argv[0]);
        exit(EXIT_FAILURE);
    }
  }

  printf("Attempting to open %s with baud rate %i ...\n", serial_port_name,
    baud);

  // check for serial port
  if (!serial_port_name) {
    fprintf(stderr, "Check the serial port path of the Piksi!\n");
    exit(EXIT_FAILURE);
  }

  // check if Piksi can be detected
  result = sp_get_port_by_name(serial_port_name, &piksi_port);
  if (result != SP_OK) {
    fprintf(stderr, "Cannot find provided serial port!\n");
    exit(EXIT_FAILURE);
  }

  // open Piksi for readings
  result = sp_open(piksi_port, SP_MODE_READ);
  if (result != SP_OK) {
    fprintf(stderr, "Cannot open %s for reading!\n", serial_port_name);
    exit(EXIT_FAILURE);
  }

  // set baud rate
  setup_port(baud);

  sbp_state_init(&s);
  sbp_register_callback(&s, SBP_MSG_HEARTBEAT, &heartbeat_callback, NULL,
                        &heartbeat_callback_node);

  while(1) {
    sbp_process(&s, &piksi_port_read);
  }

  result = sp_close(piksi_port);
  if (result != SP_OK) {
    fprintf(stderr, "Cannot close %s properly!\n", serial_port_name);
  }
  else {
    printf("Serial at %s port closed.", serial_port_name);
  }

  // clean exit the serial ports
  sp_free_port(piksi_port);
  free(serial_port_name);

  return 0;
}
