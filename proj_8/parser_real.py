



class parser:
    def __init__(self, filename):
        self.filename = open(filename, "r")
        self.curr_command = ""
        self.curr_pos = -1
        self.commands = []
        self.arithmetic = ["add", "sub", "neg", "eq", "gt", "lt", "and", "or", "not"]
        
        

        for line in self.filename.readlines():
            com = line.split("//")
            if com[0].strip() != "":
                print (com[0])
                self.commands.append(com[0].strip())
        print (len(self.commands))
            
            

        


    def has_more_commands(self):
        if self.curr_pos < len(self.commands) -1:
            return True
        else:
            return False
        

    def advance(self):
        if self.has_more_commands():
            self.curr_command = self.commands[self.curr_pos + 1]
            self.curr_pos += True

    def command_type(self):
        name = self.curr_command.split(" ")[0]
        if name in self.arithmetic:
            return "C_ARITHMETIC"
        elif name == "push":
            return "C_PUSH"
        elif name == "pop":
            return "C_POP"
        elif name == "label":
            return "C_LABEL"
        elif name == "function":
            return "C_FUNCTION"
        elif name == "call":
             return "C_CALL"
        elif name == "return":
            return "C_RETURN"
        elif name == "goto":
            return "C_GOTO"
        elif name == "if-goto":
            return "C_IF"

    def arg1(self):
        if self.curr_command == "return":
            pass
        elif self.command_type() == "C_ARITHMETIC":
            return self.curr_command
        else:
            return self.curr_command.split(" ")[1]

    def arg2(self):
        ctype = self.command_type()
        if ctype == "C_PUSH" or ctype == "C_POP" or ctype == "C_FUNCTION" or ctype == "C_CALL":
            return self.curr_command.split(" ")[2]

    def know_command(self):
        return self.curr_command.split(" ")[0]
        
        
        
            
            
        
        
        
        
        
    
