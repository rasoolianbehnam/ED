/* A simple server listening on TCP port 4010
   from http://www.linuxhowtos.org/data/6/server.c, modified
by Sam Bowne */
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <unistd.h>
#include <sys/types.h> 
#include <sys/socket.h>
#include <netinet/in.h>
#include <arpa/inet.h>


struct data {
char *name;
};



void error(const char *msg)
{
    perror(msg);
    exit(1);
}

int main(int argc, char *argv[])
{
     struct data *d1, *d2;

     int sockfd, newsockfd, portno;
     socklen_t clilen;
     char buffer[4096], reply[5100];
     struct sockaddr_in serv_addr, cli_addr;
     int n;
     char *qPtr;
     char q = 'q';
     char data2[6];

     if (argc < 2)
	{
		printf("%s\n", "Usage: ./p8x portnum");
		return(0);
	}
	
     sockfd = socket(AF_INET, SOCK_STREAM, 0);
     if (sockfd < 0) 
        error("ERROR opening socket");

     d1 = malloc(sizeof(struct data));
     d1->name = malloc(544);

     d2 = malloc(sizeof(struct data));
     d2->name = malloc(1024);


     register int iesp asm("esp");

     bzero((char *) &serv_addr, sizeof(serv_addr));
     portno = atoi(argv[1]);
     serv_addr.sin_family = AF_INET;
     serv_addr.sin_addr.s_addr = INADDR_ANY;
     serv_addr.sin_port = htons(portno);
     if (bind(sockfd, (struct sockaddr *) &serv_addr,
              sizeof(serv_addr)) < 0) 
              error("ERROR on binding");
     listen(sockfd,5);
     clilen = sizeof(cli_addr);
     newsockfd = accept(sockfd, 
                 (struct sockaddr *) &cli_addr, 
                 &clilen);
     if (newsockfd < 0) 
          error("ERROR on accept");
     while (1) {
	sprintf(reply, "Socket connected: %u %s:%u to %u %s:%u\n$esp = %#010x\n", 
		serv_addr.sin_family,
		inet_ntoa(serv_addr.sin_addr), 
		ntohs(serv_addr.sin_port),
		cli_addr.sin_family,
		inet_ntoa(cli_addr.sin_addr), 
		ntohs(cli_addr.sin_port),
                iesp);
        n = write(newsockfd, reply, strlen(reply));
        strcpy(reply, "Server listening.  Enter string to echo.  Enter q (lowercase) to quit.\n");
        n = write(newsockfd, reply, strlen(reply));
        bzero(buffer,4096);
        n = read(newsockfd,buffer,4095);
        if (n < 0) error("ERROR reading from socket");

        qPtr = strchr(buffer, q);
	if(qPtr != NULL)
	   {
           strcpy(reply, "Q received; exiting.\n");
           n = write(newsockfd, reply, strlen(reply));
           close(newsockfd);
           newsockfd = accept(sockfd, 
                       (struct sockaddr *) &cli_addr, 
                       &clilen);
           if (newsockfd < 0) 
                error("ERROR on accept");
   	   }
	else
	   {

           strcpy(d1->name, buffer);
           strncpy(data2, buffer, 4);
           data2[4] = '\0';
           strcpy(d2->name, data2);

           printf("Here is the message: %s\n",buffer);
           strcpy(reply, "I got this message: ");
           strcat(reply, buffer);
           n = write(newsockfd, reply, strlen(reply));
           if (n < 0) error("ERROR writing to socket");
           }
	}
     close(newsockfd);
     close(sockfd);
     return 0; 
}
