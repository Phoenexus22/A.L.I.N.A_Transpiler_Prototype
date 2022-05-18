#include <stdio.h>
#include "typedef.h"
int main(int argc, char *argv[]){
u32 _RAM_[2048];
u32 i;
_0: _RAM_[0+1-1]='a';
_RAM_[0+2-1]='b';
_RAM_[0+3-1]='c';
_RAM_[0+4-1]='d';
i=0;_mout0:printf("%c", (char) _RAM_[i+0]);i++;if(i!=4){goto _mout0;}
i=0;_cpy0:_RAM_[i+0xf]=_RAM_[i+0];i++;if(i!=4){goto _cpy0;}
i=0;_mout1:printf("%c", (char) _RAM_[i+0xf]);i++;if(i!=4){goto _mout1;}
return 0;

}