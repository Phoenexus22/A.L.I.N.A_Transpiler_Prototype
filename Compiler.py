import sys
infile = open(sys.argv[1], "r")
outfile = open(sys.argv[2], "w")
outfile.write('#include <stdio.h>')
outfile.write('#include "typedef.h"')
outfile.write('int main(int argc, char *argv[]){')
vartype = ""
memorysize = ""
def CompilerSettings():
    #prototype order:  source file, future file, memory bitwidth, memory size
    if sys.argv[3] == ("u8" or "u16" or "u32" or "u64" or "u1" or "i8" or "i16" or "i32" or "i64"):
        vartype = sys.argv[3]
    else:
        raise Exception("Invalid Datatype")
    memorysize = sys.argv[4]
    outfile.write(vartype + " _RAM_[" + memorysize + "];")
CompilerSettings()
