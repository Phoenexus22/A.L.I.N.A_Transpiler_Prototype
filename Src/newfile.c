#include <stdio.h>
#include "typedef.h"
int main(int argc, char *argv[]){
u32 _RAM_[2048];
_0: _RAM_[0]=97;
_RAM_[1]=98;
_1: printf("%c", (char) _RAM_[0]);
printf("%c", (char) _RAM_[1]);
_RAM_[3]=_RAM_[3]+1;
if(_RAM_[3]<10){goto *((void*[]){&&_0,&&_1})[1];}
}