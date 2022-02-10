
#include<stdlib.h>
#include<unistd.h>
int main(){
while(1)
{
char* allocatedHeap=(char*)malloc(200*1024*1024);
sleep(10);
free(allocatedHeap);
sleep(10);
}
return 0;
}
