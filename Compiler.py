import sys
import string, binascii
infile = open(sys.argv[1], "r")
lines = infile.readlines()
outfile = open(sys.argv[2], "w")
outfile.write('#include <stdio.h>\n')
outfile.write('#include "typedef.h"\n')
outfile.write('int main(int argc, char *argv[]){\n')
vartype = ""
memorysize = ""
operators = ["+","-","/","*","~","|","&","^","||","&&", "=", "!"]
intchars = ["1", "2", "3", "4", "5", "6", "7", "8", "9", "0"] 
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

def Ramreplace(phrases):
    phrasestrings = ["", "", "", ""]
    n = 0
    while n < len(phrases):
            phrasestrings[n] = ""
            spstrig = list(phrases[n])
            print(spstrig)
            blayers = 0
            lorder = [] # -1 means a num linked value. any other int implies the layer its bound to
            x = 0
            while x < len(spstrig):

                if (spstrig[x] == "$"):
                    phrasestrings[n]+="_RAM_["
                    if (spstrig[x] == "("):
                        lorder.append(blayers+1)
                    else:
                        lorder.append(-1)

                elif (spstrig[x] in operators) and (lorder[len(lorder)-1] == -1):
                    if spstrig[x] == "=":
                        phrasestrings[n] += "]=="
                    else:
                        phrasestrings[n] += "]" + spstrig[x]
                    lorder.pop()

                elif (spstrig[x] == ")" and lorder[len(lorder)-1] == blayers):
                    phrasestrings[n] +=")]"
                    blayers -=1
                    lorder.pop()

                elif (spstrig[x] == ")" ):
                    phrasestrings[n] +=")"
                    blayers -=1

                elif (spstrig[x] == "("):
                    blayers +=1
                    phrasestrings[n] +="("

                elif(spstrig[x] == "="):
                    phrasestrings[n] +="=="

                else:
                    phrasestrings[n] +=spstrig[x]
                if (x == len(spstrig)-1 and (len(lorder) > 0)):
                   while(len(lorder) > 0):
                       lorder.pop()
                       phrasestrings[n] +="]"
                x+=1 
            n+=1
    return phrasestrings



def clearspace(invar):
    for elem in [" ", "\n", "\r", "\t", "\00"]:
        invar = invar.replace(elem,"")
    return invar


#.encode("utf-8").hex()
def LineHandle(index, largest_index):
    sublines = lines[index].split(";")
    i = 0
    while i < len(sublines):
        #print("subline(" + str(i) + ")" + sublines[i])
        sublines[i] = clearspace(sublines[i]) # put remove whitespace here
        splitparts = sublines[i].split(">")
        if (len(sublines[i]) == 0):
            i+=1
            continue
        #print(splitparts[0] + "this is the numstring")
        #print(str(len(splitparts[0])) + "this is the length")
        #print(str(splitparts[0].encode("utf-8").hex()) + "this is the hex")
        if int(splitparts[0]) > largest_index:
            outfile.write("_" + splitparts[0] + ": ")
            largest_index = int(splitparts[0])
        else:
            raise Exception("Non-Linear line progression at line " + splitparts[0])
        fsplit = splitparts[1].split(":")
        phrases = fsplit[1].split(",")
        phrasestrings = Ramreplace(phrases)
        #number evaluation before function, leave most of it to c
        if fsplit[0] == "set":
                outfile.write("_RAM_[" + phrasestrings[0] + "]=" + phrasestrings[1] + ";\n")
        elif fsplit[0] == "out":
                outfile.write("printf(" +  phrasestrings[0] + ");\n")
        #c extention computed gotos
        #elif fsplit[0] == "jmp":                        
           # outfile.write("if(" + phrasestrings[1] + "){goto _" + phrasestrings[0] + ";\n")
        i+=1

    


    
CompilerSettings()
i = 0
while (i < len(lines)):
    LineHandle(i, largest_index)
    i+=1
EndFile() 
