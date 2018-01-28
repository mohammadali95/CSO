class Parser_module:
    def __init__(self, in_file):
        self.in_file = open(in_file,"r")

        self.commands = []
        self.curr_pos = 0
        self.number_com = 0
        self.curr_com = ""
        for line in self.in_file.readlines():
            line = line.strip().split("//")[0].strip()
            if line != "":
                self.commands.append(line)
                self.number_com += True 
                
            
    def has_more_commands(self):
        if self.curr_pos == self.number_com:
            return False
        else:
            return True
    def advance(self):
        if self.has_more_commands():
           self.curr_com = self.commands[self.curr_pos]
           self.curr_pos += True
    def command_type(self):
        if self.curr_com[0] == "@":
            return "A Command"
        elif self.curr_com[0] == "(":
            return "L Command"
        else:
            return "C Command"
    def symbol(self):
        if self.command_type() == "A Command":
            return self.curr_com[1:]
        elif self.command_type() == "L Command":
            return self.curr_com[1:len(self.curr_com)-1]
    def dest(self):
        if self.command_type() == "C Command":
            temp = self.curr_com.split("=")
            if len(temp)>1:
                return temp[0]
            else:
                return "null"
    def comp(self):
        if self.command_type() == "C Command":
            temp = self.curr_com.split("=")
            if len(temp)>1:
                return temp[1]
            temp1 = self.curr_com.split(";")
            if len(temp1)>1:
                return temp1[0]

    def jump(self):
        if self.command_type() == "C Command":
            temp = self.curr_com.split(";")
            if len(temp)>1:
                return temp[1]
            else:
                return "null"
        
        
        
        
        
