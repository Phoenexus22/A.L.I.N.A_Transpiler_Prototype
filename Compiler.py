import sys
infile = open(sys.argv[1], "r")
lines = infile.readlines()
outfile = open(sys.argv[2], "w")
outfile.write('#include <stdio.h>\n')
outfile.write('#include "typedef.h"\n')
outfile.write('int main(int argc, char *argv[]){\n')
vartype = ""
memorysize = ""
largest_index = -1
def CompilerSettings():
    #prototype order:  source file, future file, memory bitwidth, memory size
    if sys.argv[3] in ["u8", "u16", "u32", "u64", "u1", "i8", "i16", "i32", "i64"]:
        vartype = sys.argv[3]
    else:
        raise Exception("Invalid Datatype")
    memorysize = sys.argv[4]
    outfile.write(vartype + " _RAM_[" + memorysize + "];\n")

def EndFile():
    outfile.write("}")
    outfile.close()

def LineHandle(index):
    splitparts = lines[index].split(">")
    if int(splitparts[0]) >largest_index:
        outfile.write("_" + splitparts[0] + ": ")
        largest_index = int(splitparts[0])
    else:
        raise Exception("Non-Linear line progression at line " + splitparts[0])
    fsplit = splitparts[1].split(":")
    #number evaluation before function, leave most of it to c
    match fsplit[0]:
        case "set":
            None#tmp
        case "out":
            None#tmp

    


    
CompilerSettings()
i = 0
while (i < len(lines)):
    LineHandle(i)
EndFile() 
