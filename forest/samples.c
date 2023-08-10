#include <stdbool.h>
#include <string.h>
#include <stdlib.h>
#include <stdio.h>
#include <time.h>
#include <math.h>


void main(void){
	
	long seed = 1234567;
	
	for(int samp = 0 ; samp < 1000 ; samp++){
		
		char command[50];
		sprintf(command, "forestP.exe %d", seed);
		
		seed = time(NULL);
		srand(seed);
		
		FILE *time;
		time = fopen("./Output/time150.txt", "a");
		fprintf(time, "#Amostra %d seed %ld\n", samp, seed);
		fclose(time);
		printf("Amostra %d\n", samp);
		
		system(command);
	}

}