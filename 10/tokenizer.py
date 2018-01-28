#Tokenizer
import sys

class parser:
    def __init__(self, file):
        self.program = ""
        self.curr_pos = 0
        self.curr_token = ""
        self.tokens = []
        self.file = open(file , "r")
        self.keyword = ["class", "constructor", "function", "method", "field", "static", "var", "int",
                        "char","boolean","void","true","false","null","this","let","do","if","else","while","return"]
        self.symbol = "}{()[].,;+-*/&|<>=~"
        self.get_program()


#get program converts the file into a string getting rid of all the comments and taking care of string constants.
#Basically getting the file ready to tokenize.
    def get_program(self):
        temp = ""
        for lines in self.file.readlines():
            lines = lines.split("//")
            if lines[0] != "":
                temp += lines[0]
        # now we are going to get rid of the multiline comments.
        temp = temp.replace("/*", "*/").split("*/")
        for i in range(len(temp)):
            if i%2 == 0:
                if temp[i] != "":
                    self.program += temp[i]



        for symbol in self.symbol:
            self.program = self.program.replace(symbol," " + symbol + " ")
        #now we check for the string constants.
        self.program = self.program.split("\"")
        for const in range(len(self.program)):
            if const % 2 == 0:
                temp1 = self.program[const].strip().split(" ")
                for i in temp1:
                    if i.strip() != "":
                        self.tokens.append(i.strip())
            else:
                self.tokens.append("\"" + self.program[const])


    def has_more_tokens(self):
        if self.curr_pos < len(self.tokens):
            return True
        else:
            return False
    def advance(self):
        if self.has_more_tokens():
            self.curr_token = self.tokens[self.curr_pos]
            self.curr_pos += True

    def token_type(self):
        if self.curr_token in self.keyword:
            return "KEYWORD"
        if self.curr_token in self.symbol:
            return "SYMBOL"
        if self.curr_token.isdigit():
            return "INT_CONST"
        if "\"" in self.curr_token:
            return "STRING_CONST"
        else:
            return "IDENTIFIER"

    def keyWord(self):
        return self.curr_token
    def Symbol(self):
        return self.curr_token
    def identifier(self):
        return self.curr_token
    def intVal(self):
        return self.curr_token
    def stringVal(self):
        return self.curr_token[1:]


j = parser(sys.argv[1])
out_file = open(sys.argv[1].replace(".jack", "2T.xml") , "w")

out_file.write("<tokens>\n")
while j.has_more_tokens():
    j.advance()
    if j.token_type() == "KEYWORD":
        out_file.write("<keyword> " + j.keyWord() + " </keyword>\n")
    if j.token_type() == "SYMBOL":
        if j.Symbol() in "<>&":
            dic = {"<" : "&lt;", ">" : "&gt;", "&" : "&amp;"}
            out_file.write("<symbol> " + dic[j.Symbol()] + " </symbol>\n")
        else:
            out_file.write("<symbol> " + j.Symbol() + " </symbol>\n")
    if j.token_type() == "INT_CONST":
        out_file.write("<integerConstant> " + j.intVal() + " </integerConstant>\n")
    if j.token_type() == "STRING_CONST":
       out_file.write("<stringConstant> " + j.stringVal() + " </stringConstant>\n")
    if j.token_type() == "IDENTIFIER":
        out_file.write("<identifier> " + j.identifier() + " </identifier>\n")
out_file.write("</tokens>")
out_file.close()
