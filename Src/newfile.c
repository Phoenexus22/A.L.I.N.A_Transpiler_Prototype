#include <stdio.h>
#include "typedef.h"
int main(int argc, char *argv[]){
u32 _RAM_[2];
u32 i;
_0: _RAM_[0]=1;
_1: _RAM_[1]=_RAM_[0];
_2: if((_RAM_[1]==1)){goto *((void*[]){&&_0,&&_1,&&_2,&&_3,&&_4,&&_5})[3];}
if((_RAM_[1]%2==0)){goto *((void*[]){&&_0,&&_1,&&_2,&&_3,&&_4,&&_5})[4];}
if(1){goto *((void*[]){&&_0,&&_1,&&_2,&&_3,&&_4,&&_5})[5];}
_3: _RAM_[0]=_RAM_[0]+1;
if(_RAM_[0]<100){goto *((void*[]){&&_0,&&_1,&&_2,&&_3,&&_4,&&_5})[1];}
printf("%c",(char) 'D');
printf("%c",(char) 'O');
printf("%c",(char) 'N');
printf("%c",(char) 'E');
return 0;
_4: _RAM_[1]=_RAM_[1]/2;
if(1){goto *((void*[]){&&_0,&&_1,&&_2,&&_3,&&_4,&&_5})[2];}
_5: _RAM_[1]=(_RAM_[1]*3)+1;
if(1){goto *((void*[]){&&_0,&&_1,&&_2,&&_3,&&_4,&&_5})[2];}

}