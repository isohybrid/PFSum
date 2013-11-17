// #define __USE_BSD             /* Using BSD IP header */
#include <netinet/ip.h>       /* Internet Protocol */
#define __FAVOR_BSD           /* Using BSD TCP header */
#include <netinet/tcp.h>      /* Transmission Control Protocol */

#include <sys/socket.h>
#include <arpa/inet.h>
#include <netinet/in.h>

#include <pcap.h>
#include <stdlib.h>
#include <string.h>
#include <time.h>
#include <stdio.h>

#define MAXBYTES2CAPTURE 2048

int main(int argc, char *argv[])
{
  int count = 0;
  bpf_u_int32 netaddr = 0, mask = 0;
  pcap_t *device = NULL;
  struct bpf_program filter;
  struct ip *ip_hdr = NULL;
  struct tcphdr *tcp_hdr = NULL;
  struct pcap_pkthdr pkthdr;
  const unsigned char *packet = NULL;

  char errBuf[PCAP_ERRBUF_SIZE];
  memset(errBuf, 0, PCAP_ERRBUF_SIZE);

  FILE *fp;
  fp = fopen("portraffic.log", "a");

  if (argc != 2){
    printf("Usage: portraffic <interface>\n");
    exit(1);
  }

  /* open network device for packet capture */
  device = pcap_open_live(argv[1], MAXBYTES2CAPTURE, 1, 0, errBuf);
  if(!device){
    printf("error: pcap_open_live(): %s\n", errBuf);
    exit(1);
  }

  /* Look up info from the packet capture */
  pcap_lookupnet( argv[1], &netaddr, &mask, errBuf);

  /* Compiles the filter expression */
  pcap_compile(device, &filter, "(tcp) or (udp)", 1, mask);

  /* load the filter program into the packet capture device. */
  pcap_setfilter(device, &filter);
  
  while(1){
    packet = pcap_next(device, &pkthdr);
    /* Assuming is Ethernet! */
    ip_hdr = (struct ip *)(packet+14);
    /* Assuming no IP options! */
    tcp_hdr = (struct tcphdr *)(packet+14+20);

    /*
    printf("length : %d\n", pkthdr.len);
    int i=0;
    for(i=0; i < pkthdr.len; i++){
      printf("%02x", packet[i]);
      if((i+1) % 16 == 0)
        printf("\n");
    }
    */
    fprintf(fp, "%s\t%s\t%s\t%d\t%d\n",\
        ctime((const time_t *)&pkthdr.ts.tv_sec),\
        inet_ntoa(ip_hdr->ip_src),\
        inet_ntoa(ip_hdr->ip_dst),\
        ntohs(tcp_hdr->th_sport),\
        ntohs(tcp_hdr->th_dport));

    printf("------------------------------------------------\n");
    printf("Received Packet:         %d\n", ++count);
    printf("DST IP:                  %s\n", inet_ntoa(ip_hdr->ip_dst));
    printf("SRC IP:                  %s\n", inet_ntoa(ip_hdr->ip_src));
    printf("SRC PORT:                %d\n", ntohs(tcp_hdr->th_sport));
    printf("DST PORT:                %d\n", ntohs(tcp_hdr->th_dport));
    printf("------------------------------------------------\n");
  }

  pcap_close(device);
  fclose(fp);

  return 0;
}
