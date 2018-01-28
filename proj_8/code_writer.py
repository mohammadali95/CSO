class code_writer:
    def __init__(self, filename):
        self.arithmetic = { "add" :"@SP\nM=M-1\nA=M\nD=M\nA=A-1\nM=M+D\n",
                            "sub" :"@SP\nM=M-1\nA=M\nD=M\nA=A-1\nM=M-D\n",
                            "neg" :"@SP\nA=M-1\nM=-M\n",
                            "and" :"@SP\nM=M-1\nA=M\nD=M\nA=A-1\nM=M&D\n",
                            "or" : "@SP\nM=M-1\nA=M\nD=M\nA=A-1\nM=M|D\n",
                            "not" : "@SP\nA=M-1\nM=!M\n"}
        self.label = 0
        self.file_name = ""
        self.set_file_name(filename)
        self.out_file = open(self.file_name + ".asm", 'w')

    def write_init(self):
        self.out_file.write("@256\nD=A\n@SP\nM=D\n")
        self.out_file.write("@300\nD=A\n@LCL\nM=D\n")
        self.out_file.write("@400\nD=A\n@ARG\nM=D\n")
        self.out_file.write("@3000\nD=A\n@THIS\nM=D\n")
        self.out_file.write("@4000\nD=A\n@THAT\nM=D\n")\
        self.write_call("Sys.init", '0')

    def set_file_name(self, file_name):
        self.file_name = file_name

    def close_file(self):
        self.out_file.close()

    def write_arith(self,command):
        self.label += 1
        loop = "LOOP" + str(self.label)
        end  = "END" + str(self.label)
        if command == "eq":
            x = "@SP\nM=M-1\nA=M\nD=M\nA=A-1\nM=M-D\nD=M\n@" + loop + "\n"
            x = x + "D;JNE\n@SP\nM=M-1\nA=M\nM=-1\n@" + end + "\n0;JMP\n(" + loop + ")\n@SP\nM=M-1\nA=M\nM=0\n(" + end + ")\n@SP\nM=M+1"
            self.out_file.write(x + "\n")
        elif command == "lt":
            x = "@SP\nM=M-1\nA=M\nD=M\nA=A-1\nM=M-D\nD=M\n@" + loop + "\n"
            x = x + "D;JGE\n@SP\nM=M-1\nA=M\nM=-1\n@" + end + "\n0;JMP\n(" + loop + ")\n@SP\nM=M-1\nA=M\nM=0\n(" + end + ")\n@SP\nM=M+1"
            self.out_file.write(x + "\n")
        elif command == "gt":
            x = "@SP\nM=M-1\nA=M\nD=M\nA=A-1\nM=M-D\nD=M\n@" + loop  + "\n"
            x = x + "D;JLE\n@SP\nM=M-1\nA=M\nM=-1\n@" + end + "\n0;JMP\n(" + loop + ")\n@SP\nM=M-1\nA=M\nM=0\n(" + end + ")\n@SP\nM=M+1"
            self.out_file.write(x + "\n")

        else:
            x = self.arithmetic[command]
            self.out_file.write(x + "\n")

    def write_push_pop(self, command, segment, index):
        if command == "C_PUSH":
            if segment == "local":
                x = "@" + index + "\nD=A\n@LCL\nA=M+D\nD=M\n@SP\nA=M\nM=D\n@SP\nM=M+1"
            if segment == "constant":
                x = "@" + index + "\nD=A\n@SP\nA=M\nM=D\n@SP\nM=M+1"
            if segment == "argument":
                x = "@" + index + "\nD=A\n@ARG\nA=M+D\nD=M\n@SP\nA=M\nM=D\n@SP\nM=M+1"
            if segment == "this":
                x = "@" + index + "\nD=A\n@THIS\nA=M+D\nD=M\n@SP\nA=M\nM=D\n@SP\nM=M+1"
            if segment == "that":
                x = "@" + index + "\nD=A\n@THAT\nA=M+D\nD=M\n@SP\nA=M\nM=D\n@SP\nM=M+1"
            if segment == "pointer":
                x = "@" + index + "\nD=A\n@THIS\nA=A+D\nD=M\n@SP\nA=M\nM=D\n@SP\nM=M+1"
            if segment == "temp":
                x = "@" + index + "\nD=A\n@5\nA=A+D\nD=M\n@SP\nA=M\nM=D\n@SP\nM=M+1"
            if segment == "static":
                x = "@" + self.file_name + "." + index + "\nD=M\n@SP\nA=M\nM=D\n@SP\nM=M+1"

        if command == "C_POP":
             if segment == "local":
                x = "@" + index + "\nD=A\n@LCL\nD=D+M\n@13\nM=D\n@SP\nM=M-1\nA=M\nD=M\n@13\nA=M\nM=D"
             if segment == "argument":
                x = "@" + index + "\nD=A\n@ARG\nD=D+M\n@13\nM=D\n@SP\nM=M-1\nA=M\nD=M\n@13\nA=M\nM=D"
             if segment == "this":
                x = "@" + index + "\nD=A\n@THIS\nD=D+M\n@13\nM=D\n@SP\nM=M-1\nA=M\nD=M\n@13\nA=M\nM=D"
             if segment == "that":
                x = "@" + index + "\nD=A\n@THAT\nD=D+M\n@13\nM=D\n@SP\nM=M-1\nA=M\nD=M\n@13\nA=M\nM=D"
             if segment == "pointer":
                x = "@" + index + "\nD=A\n@THIS\nD=D+A\n@13\nM=D\n@SP\nM=M-1\nA=M\nD=M\n@13\nA=M\nM=D"
             if segment == "temp":
                x = "@" + index + "\nD=A\n@5\nD=D+A\n@13\nM=D\n@SP\nM=M-1\nA=M\nD=M\n@13\nA=M\nM=D"
             if segment == "static":
                x =  "@SP\nM=M-1\nA=M\nD=M\n" + "@" + self.file_name + "." + index + "\nM=D"
        self.out_file.write(x + "\n")



    def write_label(self, label):
        self.out_file.write("(" + label + ")\n")


    def write_goto(self, label):
        self.out_file.write("@"+ label + "\n0;JMP\n")


    def write_if_goto(self, label):
        self.out_file.write("@SP\nM=M-1\nA=M\nD=M\nA=A-1\n@"+ label +"\nD;JNE\n")


    def write_function(self, name, k):
        self.label += 1
        loop = "LOOP" + str(self.label)
        end  = "END" + str(self.label)
        self.out_file.write('(' + name + ')\n@' + k + '\nD=A\n@i\nM=D\nD=M\n@' + name + '.' + k+ '\nD;JEQ\n(' + name + '..' + k + ')\n@SP\nA=M\nM=0\n@SP\nD=M\nD=D+1\nM=D\n@i\nD=M\nD=D-1\nM=D\n@' + name + '..' + k + '\nD;JNE\n(' + name + '.' + k + ')\n')


    def write_call(self, name,arg):
        self.label += 1
        rtr = "RETURN" + str(self.label)
        self.out_file.write("@" + rtr + "\nD=A\n@SP\nA=M\nM=D\n@SP\nM=M+1\n@LCL\nD=M\n@SP\nA=M\nM=D\n@SP\nM=M+1\n@ARG\nD=M\n@SP\nA=M\nM=D\n@SP\nM=M+1\n@THIS\nD=M\n@SP\nA=M\nM=D\n@SP\nM=M+1\n@THAT\nD=M\n@SP\nA=M\nM=D\n@SP\nM=M+1\n@SP\nD=M\n@"+arg+"\nD=D-A\n@5\nD=D-A\n@ARG\nM=D\n@SP\nD=M\n@LCL\nM=D\n@"+name+"\n0;JMP\n("+rtr+")\n")

    def write_return(self):
        self.out_file.write('@LCL\nD=M\n@FRAME\nM=D\n@FRAME\nD=M\n@5\nD=D-A\nA=D\nD=M\n@RET\nM=D\n@SP\nD=M\nD=D-1\nA=D\nD=M\n@ARG\nA=M\nM=D\n@ARG\nD=M\nD=D+1\n@SP\nM=D\n@FRAME\nD=M\nD=D-1\nA=D\nD=M\n@THAT\nM=D\n@FRAME\nD=M\n@2\nD=D-A\nA=D\nD=M\n@THIS\nM=D\n@FRAME\nD=M\n@3\nD=D-A\nA=D\nD=M\n@ARG\nM=D\n@FRAME\nD=M\n@4\nD=D-A\nA=D\nD=M\n@LCL\nM=D\n@RET\nA=M\n0;JMP\n')
