#argument order:  source file, compiled file, memory type, memory size
#to solve the issue of non consecutive labeling- have it as a compiler option so can waste space
# dual operators currently unsupported - do later
import sys
import string, binascii
infile = open(sys.argv[1], "r")
lines = infile.read()
outfile = open(sys.argv[2], "w")
outfile.write('#include <stdio.h>\n')
outfile.write('#include "typedef.h"\n')
outfile.write('int main(int argc, char *argv[]){\n')
global vartype #will be determined by compiler instructions 
memorysize = ""
operators = ["+","-","/","*","~","|","&","^","||","&&", "=", "!", ">", "<", "%"]
intchars = ["1", "2", "3", "4", "5", "6", "7", "8", "9", "0"] 
labelarray = []
largest_index = -1
cpynumber = 0
moutnumber = 0
if sys.argv[3] in ["u8", "u16", "u32", "u64", "i8", "i16", "i32", "i64", "f32", "f64"]:
    vartype = sys.argv[3]
else:
    raise Exception("CompilerError: Invalid Datatype")
memorysize = sys.argv[4]
outfile.write(vartype + " _RAM_[" + memorysize + "];\n")
outfile.write(vartype + " i;\n")

def EndFile():
    outfile.write("\n}")
    outfile.close()

def makecsc(instring):
    validesc = ["a", "b", "f", "n", "r", "t", "v", "'",'d',"?","\\", "g"]# d, g are non standard and are  ", `
    i = 0
    accum = ''
    while (i < len(instring)):
        if instring[i] == "\\":
            if instring[i+1] in validesc:
                if (instring[i+1] == "d"):
                    accum += "'\\" + '"' + "'"
                elif (instring[i+1] == "q"):
                    accum += "'\\" + '?' + "'"  
                elif (instring[i+1] == "g"):
                    accum += "'`'"  
                else:
                    accum += "'\\" + instring[i+1] + "'" 
                i+=1
            else:
                raise Exception('SyntaxError: Invalid Escape Sequence')
        else:
            accum += "'" + instring[i] + "'"
        if (i!=len(instring)-1):
            accum+=','
        i+=1
    return accum

    
def Ramreplace(phrases):
    phrasestrings = [] 
    n = 0
    while n < len(phrases):
            phrasestrings.append("")
            spstrig = list(phrases[n])
            blayers = 0
            lorder = [] # -1 means a num linked value. any other int implies the layer its bound to
            x = 0
            while x < len(spstrig):
                print(lorder)
                if (spstrig[x] == "$"):
                    phrasestrings[n]+="_RAM_["
                    if (spstrig[x] == "("):
                        lorder.append(blayers+1)
                    else:
                        lorder.append(-1)

                elif (spstrig[x] in operators) and len(lorder)>0 and (lorder[len(lorder)-1] == -1):
                    if spstrig[x] == "=":
                        phrasestrings[n] += "]=="
                    else:
                        phrasestrings[n] += "]" + spstrig[x]
                    lorder.pop()

                elif (spstrig[x] == ")" and len(lorder)>0 and lorder[len(lorder)-1] == blayers):
                    phrasestrings[n] +=")]"
                    blayers -=1
                    lorder.pop()

                elif (spstrig[x] == ")" and len(lorder)>0 and lorder[len(lorder)-1] == -1):
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
                elif(spstrig[x] == "#"):
                    phrasestrings[n] +="0x"

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

def remcomments(input):
    spl = input.split("`")
    if (len(spl)%2==0):
        raise Exception("SyntaxError: Comment Character (`) without partner")
    output = ""
    i = 0
    while i < len(spl):
        output+=spl[i]
        i+=2
    return output

def stringhandle(input):
    spl = input.split('"')
    if (len(spl)%2==0):
        raise Exception('SyntaxError: String Character (") without partner')
    output = ""
    i = 0
    while i < len(spl):
        if(not(i%2==0)):
            output+=makecsc(spl[i])
        else:
            output+=spl[i]
        i+=1
    return output

def makelabelarray(srclines):
    prev=-1
    go = True
    retarray = []
    while go:
        accum = ''
        index = srclines.find('>', prev+1)
        if (index == -1):
            go = False
            break
        prev = index
        n = 1
        var = ""
        while var != ';':
            var = srclines[index -n]
            if var==';':
                break
            accum+=var
            n+=1
        retarray.append(int(accum[::-1]))
    return retarray
   
#.encode("utf-8").hex()
def LineHandle(largest_index):
    global cpynumber
    global moutnumber
    global lines
    lines = remcomments(lines)
    lines = stringhandle(lines)
    labelarray = makelabelarray(lines)
    sublines = lines.split(";")
    i = 0
    while i < len(sublines):
        sublines[i] = clearspace(sublines[i]) #removes whitespace
        splitparts = sublines[i].split(">")
        if (len(sublines[i]) == 0):
            i+=1
            continue
        if (not (len(splitparts) < 2)):
            if int(splitparts[0]) > largest_index:
                outfile.write("_" + splitparts[0] + ": ")
                largest_index = int(splitparts[0])
                #labelarray.append(int(splitparts[0]))
            else:
                raise Exception("SyntaxError: Non-Linear line progression at line " + splitparts[0])
        else:
            splitparts.insert(0,"")
        fsplit = splitparts[1].split(":")
        phrases = fsplit[1].split(",")
        phrasestrings = Ramreplace(phrases)
        #number evaluation before function, leave most of it to c

        if fsplit[0] == "set": #changes the value of an address (Address to set, Value to set)
                outfile.write("_RAM_[" + phrasestrings[0] + "]=" + phrasestrings[1] + ";\n")

        elif fsplit[0] == "out": #outputs a character to the console[currently] (Char value to output) 
                outfile.write('printf("%c", (char) ' +  phrasestrings[0] + ");\n")
        #c extention not stable
        #either figure out how to jump to later code, or pick where to start execution

        elif fsplit[0] == "jmp":    # moves the program pointer (Label to jump to, condition (0=false else=true))
            # this code only works for consecutive labels
            f = 0
            stvar = "if(" + phrasestrings[1] + "){goto *((void*[]){"
            while (f < len(labelarray)):
                stvar+="&&_" + str(labelarray[f])
                if (not(f == len(labelarray) -1)):
                    stvar+=","
                f+=1
            outfile.write(stvar + "})[" +  str(phrasestrings[0]) + "];}\n") 

            #learn how scanf works
        #elif fsplit[0] == "in":
             #outfile.write('scanf("%c",_RAM_['+phrasestrings[0]+']);\n')

        elif fsplit[0] == "cpy": # copies a set of values from consecutive memory addresses to elsewhere in memory (old first address, new first address, length )
            outfile.write("i=0;_cpy" + str(cpynumber) + ":_RAM_[i+" + phrasestrings[1] +"]=_RAM_[i+" + phrasestrings[0] +"];i++;if(i!="+ phrasestrings[2] +"){goto _cpy" + str(cpynumber) + ";}\n")
            cpynumber+=1

        elif fsplit[0] == "vout": # outputs a set of values from consecutive memory addresses to the console (first address, length )
            outfile.write("i=0;_mout" + str(moutnumber) + ':printf("%c", (char) _RAM_[i+' + phrasestrings[0] +"]);i++;if(i!="+ phrasestrings[1] +"){goto _mout" + str(moutnumber) + ";}\n")
            moutnumber+=1

        elif fsplit[0] == "mset": #moves multiple values into memory
            p = 1
            while p < len(phrasestrings):
                outfile.write("_RAM_[" + phrasestrings[0] + "+" + str(p-1) + "]=" + phrasestrings[p] + ";\n")
                p+=1
        elif fsplit[0] == "die":
            outfile.write("return " + phrasestrings[0] +";\n")

        elif fsplit[0] == "mout":
            p = 0
            while p < len(phrasestrings):
                outfile.write('printf("%c",(char) ' + phrasestrings[p] + ');\n')
                p+=1

        elif fsplit[0] == "ujmp":    # moves the program pointer (Label to jump to)
            # this code only works for consecutive labels
            f = 0
            stvar = "goto *((void*[]){"
            while (f < len(labelarray)):
                stvar+="&&_" + str(labelarray[f])
                if (not(f == len(labelarray) -1)):
                    stvar+=","
                f+=1
            outfile.write(stvar + "})[" +  str(phrasestrings[0]) + "];\n") 

        elif fsplit[0] == "fjmp":    # moves the program pointer (Label to jump to (must be int), condition (0=false else=true))
            f = 0
            stvar = "if(" + phrasestrings[1] + "){goto _" + str(int(phrasestrings[0])) + "}\n" # first value must be int

        elif fsplit[0] == "ufjmp":    # moves the program pointer (Label to jump to (must be int), condition (0=false else=true))
            f = 0
            stvar = "goto _" + str(int(phrasestrings[0])) + ";\n" # first value must be int

    



LineHandle( largest_index)
EndFile() 