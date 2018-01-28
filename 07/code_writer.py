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
        self.out_file = open(self.file_name.replace(".vm", ".asm"), 'w')

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
