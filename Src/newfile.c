#include <stdio.h>
#include "typedef.h"
int main(int argc, char *argv[]){
u32 _RAM_[2048];
u32 i;
_0: _RAM_[0]=97;
_RAM_[1]=98;
_RAM_[2]=99;
_RAM_[3]=100;
i=0;_mout0:printf("%c", (char) _RAM_[i+0]);i++;if(i!=4){goto _mout0;}
i=0;_cpy0:_RAM_[i+5]=_RAM_[i+0];i++;if(i!=4){goto _cpy0;}
i=0;_mout1:printf("%c", (char) _RAM_[i+5]);i++;if(i!=4){goto _mout1;}
_1: if(1){goto *((void*[]){&&_0,&&_1})[1];}
return 0;}