from cProfile import label
import sys
import string, binascii
infile = open(sys.argv[1], "r")
lines = infile.readlines()
outfile = open(sys.argv[2], "w")
outfile.write('#include <stdio.h>\n')
outfile.write('#include "typedef.h"\n')
outfile.write('int main(int argc, char *argv[]){\n')
global vartype
memorysize = ""
operators = ["+","-","/","*","~","|","&","^","||","&&", "=", "!", ">", "<"]
intchars = ["1", "2", "3", "4", "5", "6", "7", "8", "9", "0"] 
labelarray = []
largest_index = -1
cpynumber = 0
moutnumber = 0
 #prototype order:  source file, future file, memory bitwidth, memory size
if sys.argv[3] in ["u8", "u16", "u32", "u64", "u1", "i8", "i16", "i32", "i64"]:
    vartype = sys.argv[3]
else:
    raise Exception("Invalid Datatype")
memorysize = sys.argv[4]
outfile.write(vartype + " _RAM_[" + memorysize + "];\n")
outfile.write(vartype + " i;\n")

def EndFile():
    outfile.write("return 0;}")
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

                elif (spstrig[x] == ")" and lorder[len(lorder)-1] == -1):
                    phrasestrings[n] +="])"
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
    global cpynumber
    global moutnumber
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
        if (not (len(splitparts) < 2)):
            if int(splitparts[0]) > largest_index:
                outfile.write("_" + splitparts[0] + ": ")
                largest_index = int(splitparts[0])
                labelarray.append(int(splitparts[0]))
            else:
                raise Exception("Non-Linear line progression at line " + splitparts[0])
        else:
            splitparts.insert(0,"")
        fsplit = splitparts[1].split(":")
        phrases = fsplit[1].split(",")
        phrasestrings = Ramreplace(phrases)
        #number evaluation before function, leave most of it to c
        if fsplit[0] == "set":
                outfile.write("_RAM_[" + phrasestrings[0] + "]=" + phrasestrings[1] + ";\n")
        elif fsplit[0] == "out":
                outfile.write('printf("%c", (char) ' +  phrasestrings[0] + ");\n")
        #c extention computed gotos    goto *((void*[]){&&label, &&babel})[1];
        elif fsplit[0] == "jmp":    
            f = 0
            stvar = "if(" + phrasestrings[1] + "){goto *((void*[]){"
            while (f < len(labelarray)):
                stvar+="&&_" + str(labelarray[f])
                if (not(f == len(labelarray) -1)):
                    stvar+=","
                f+=1
            print(labelarray)
            #crap, this might rely on the compiler computing
            outfile.write(stvar + "})[" +  str(phrasestrings[0]) + "];}\n") # this code only works for consecutive values
            #learn how scanf works
        #elif fsplit[0] == "in":
             #outfile.write('scanf("%c",_RAM_['+phrasestrings[0]+']);\n')
        elif fsplit[0] == "cpy":
            outfile.write("i=0;_cpy" + str(cpynumber) + ":_RAM_[i+" + phrasestrings[1] +"]=_RAM_[i+" + phrasestrings[0] +"];i++;if(i!="+ phrasestrings[2] +"){goto _cpy" + str(cpynumber) + ";}\n")
            cpynumber+=1
        elif fsplit[0] == "mout":
            outfile.write("i=0;_mout" + str(moutnumber) + ':printf("%c", (char) _RAM_[i+' + phrasestrings[0] +"]);i++;if(i!="+ phrasestrings[1] +"){goto _mout" + str(moutnumber) + ";}\n")
            moutnumber+=1
        #a function to load many variables into memory would be nice

        i+=1

    


i = 0
while (i < len(lines)):
    LineHandle(i, largest_index)
    i+=1
EndFile() 