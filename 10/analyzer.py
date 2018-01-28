class analyzer:
    def __init__(self, file):
        self.file = open(file, "r")
        self.file_lines = self.file.readlines()
        self.i = 0
        self.curr = 1
        self.keyword = ["class", "constructor", "function", "method", "field", "static", "var", "int",
                        "char","boolean","void","true","false","null","this","let","do","if","else","while","return"]
        self.file_name = ""

        self.file_name = file
        name = self.file_name.replace("2T", "T")
        print (name)
        self.out_file = open(name, 'w')
        self.out_file.write("<class>\n")
        self.i += 2
        self.comp_class()
        self.p("symbol")
        self.out_file.write("</class>")

    def close(self):
        self.out_file.close()


    #got help from Karthik.
    def p(self,tag):
        temp = self.file_lines[self.curr].split(" ")
        tag = " " * self.i + "<" +tag + "> " + " ".join(self.file_lines[self.curr].split(" ")[1:-1]) + " </" + tag + ">\n"
        self.out_file.write(tag)

    def comp_class(self):
        l = ['constructor' , 'function', 'method', 'void']
        self.p("keyword")
        self.curr += 1
        self.p("identifier")
        self.curr += 1
        self.p("symbol")
        self.curr += 1
        while "static" in self.file_lines[self.curr] or "field" in self.file_lines[self.curr]:
            self.out_file.write(" " * self.i + "<classVarDec>\n")
            self.i += 2
            self.class_vardec()
            self.i -= 2
            self.out_file.write(" " * self.i + "</classVarDec>\n")

        for i in l:
            while i in self.file_lines[self.curr]:
                self.out_file.write(" " * self.i + "<subroutineDec>\n")
                self.i +=2
                self.sub_dec()
                self.i -=2
                self.out_file.write(" " * self.i + "</subroutineDec>\n")



    def class_vardec(self):
        self.p("keyword")
        self.curr += 1
        if self.file_lines[self.curr].split(" ")[1] in "intcharboolean":
            self.p("keyword")
            self.curr += 1
        else:
            self.p("identifier")
            self.curr += 1


        self.p("identifier")
        self.curr += 1
        self.p("symbol")
        while ";" not in self.file_lines[self.curr]:
            self.curr += 1
            self.p("identifier")
            self.curr += 1
            self.p("symbol")
        self.curr += 1

    def sub_dec(self):

        self.p("keyword")
        self.curr += 1
        if "void" in self.file_lines[self.curr]:
            self.p("keyword")
            self.curr += 1
        elif self.file_lines[self.curr].split(" ")[1] in "intcharboolean":
            self.p("keyword")
            self.curr += 1
        else:
            self.p("identifier")
            self.curr += 1
        self.p("identifier")
        self.curr += 1
        self.p("symbol")
        self.curr += 1
        self.out_file.write(" " * self.i + "<parameterList>\n")
        self.i += 2
        if ")" not in self.file_lines[self.curr]:
            self.paraL()
        self.i -= 2
        self.out_file.write(" " * self.i + "</parameterList>\n")
        self.p("symbol")
        self.curr += 1
        self.out_file.write(" " * self.i + "<subroutineBody>\n")
        self.i += 2
        self.p("symbol")
        self.curr += 1
        while "var" in self.file_lines[self.curr]:
            self.out_file.write(" " * self.i + "<varDec>\n")
            self.varDec()
            self.out_file.write(" " * self.i + "</varDec>\n")

        self.out_file.write(" " * self.i + "<statements>\n")

        self.i += 2
        self.compStat()
        self.i -= 2
        self.out_file.write(" " * self.i + "</statements>\n")
        self.p("symbol")
        self.curr += 1




        self.i -= 2
        self.out_file.write(" " * self.i + "</subroutineBody>\n")

    def paraL(self):
        if self.file_lines[self.curr].split(" ")[1] in "intcharboolean":
            self.p("keyword")
            self.curr += 1
        else:
            self.p("identifier")
            self.curr += 1
        self.p("identifier")
        self.curr += 1
        while "," in self.file_lines[self.curr]:
            self.p("symbol")
            self.curr += 1
            if self.file_lines[self.curr].split(" ")[1] in "intcharboolean":
                self.p("keyword")
                self.curr += 1
            else:
                self.p("identifier")
                self.curr += 1
            self.p("identifier")
            self.curr += 1

    def varDec(self):

        self.p("keyword")
        self.curr += 1
        if self.file_lines[self.curr].split(" ")[1] in self.keyword:
            self.p("keyword")
        else:
            self.p("identifier")
        self.curr+= 1
        self.p("identifier")
        self.curr += 1
        while "," in self.file_lines[self.curr]:
            self.p("symbol")
            self.curr += 1

            if self.file_lines[self.curr].split(" ")[1] in self.keyword:
                self.p("keyword")
            else:
                self.p("identifier")
            self.curr+= 1
        self.p("symbol")
        self.curr += 1

    def compStat(self):
        if "let" in self.file_lines[self.curr]:
            self.out_file.write(" " * self.i + "<letStatement>\n")
            self.i += 2
            self.let()
            self.i -= 2
            self.out_file.write(" " * self.i + "</letStatement>\n")
            self.compStat()
        elif self.file_lines[self.curr].split(" ")[1] == "if":
            self.out_file.write(" " * self.i + "<ifStatement>\n")
            self.i += 2
            self.iff()
            self.i -= 2
            self.out_file.write(" " * self.i + "</ifStatement>\n")
            self.compStat()
        elif "while" in self.file_lines[self.curr]:
            self.out_file.write(" " * self.i + "<whileStatement>\n")
            self.i += 2
            self.whily()
            self.i -= 2
            self.out_file.write(" " * self.i + "</whileStatement>\n")
            self.compStat()
        elif "do" in self.file_lines[self.curr]:
            self.out_file.write(" " * self.i + "<doStatement>\n")
            self.i += 2
            self.do()
            self.i -= 2
            self.out_file.write(" " * self.i + "</doStatement>\n")
            self.compStat()
        elif "return" in self.file_lines[self.curr]:
            self.out_file.write(" " * self.i + "<returnStatement>\n")
            self.i += 2
            self.ret()
            self.i -= 2
            self.out_file.write(" " * self.i + "</returnStatement>\n")

            self.compStat()

    def let(self):
        self.p("keyword")
        self.curr += 1
        self.p("identifier")
        self.curr += 1
        while "=" not in self.file_lines[self.curr]:
            self.p("symbol")
            self.curr += 1
            self.out_file.write(" " * self.i + "<expression>\n")
            self.comp_exp()
            self.out_file.write(" " * self.i + "</expression>\n")
            self.p("symbol")
            self.curr += 1
        self.p("symbol")
        self.curr += 1
        self.out_file.write(" " * self.i + "<expression>\n")
        self.comp_exp()
        self.out_file.write(" " * self.i + "</expression>\n")
        self.p("symbol")
        self.curr += 1

    def iff(self):
        self.p("keyword")
        self.curr += 1
        self.p("symbol")
        self.curr += 1
        self.out_file.write(" " * self.i + "<expression>\n")
        self.comp_exp()
        self.out_file.write(" " * self.i + "</expression>\n")
        self.p("symbol")
        self.curr += 1
        self.p("symbol")
        self.curr+= 1
        self.out_file.write(" " * self.i + "<statements>\n")
        self.compStat()
        self.out_file.write(" " * self.i + "</statements>\n")
        self.p("symbol")
        self.curr += 1
        if "else" in self.file_lines[self.curr]:
            self.p("keyword")
            self.curr += 1
            self.p("symbol")
            self.curr + 1
            self.out_file.write(" " * self.i + "<statements>\n")
            self.compStat()
            self.out_file.write(" " * self.i + "</statements>\n")
            self.p("symbol")


    def whily(self):
        self.p("keyword")
        self.curr += 1
        self.p("symbol")
        self.curr += 1
        self.out_file.write(" " * self.i + "<expression>\n")
        self.comp_exp()
        self.out_file.write(" " * self.i + "</expression>\n")
        self.p("symbol")
        self.curr += 1
        self.p("symbol")
        self.curr += 1
        self.out_file.write(" " * self.i + "<statements>\n")
        self.compStat()
        self.out_file.write(" " * self.i + "</statements>\n")
        self.p("symbol")
        self.curr += 1

    def do(self):

        self.p("keyword")
        self.curr += 1
        self.comp_term()
        self.p("symbol")
        self.curr += 1

    def ret(self):
        self.p("keyword")
        self.curr += 1
        while ";" not in self.file_lines[self.curr]:
            self.out_file.write(" " * self.i + "<expression>\n")
            self.comp_exp()
            self.out_file.write(" " * self.i + "</expression>\n")
        self.p("symbol")
        self.curr += 1


    def comp_exp(self):
        self.i += 2
        self.out_file.write(" " * self.i + "<term>\n")
        self.comp_term()
        self.out_file.write(" " * self.i + "</term>\n")

        while self.file_lines[self.curr ].split(" ")[1] in ["+","-","*","/","&","|","=","&lt;", "&gt;"] :


            self.p("symbol")
            self.curr += 1
            self.out_file.write(" " * self.i + "<term>\n")
            self.comp_term()
            self.out_file.write(" " * self.i + "</term>\n")
        self.i -= 2


    def comp_explist(self):
        if ")" not in self.file_lines[self.curr]:
            self.out_file.write(" " * self.i + "<expression>\n")
            self.comp_exp()
            self.out_file.write(" " * self.i + "</expression>\n")

            while "," in self.file_lines[self.curr + 1]:
                self.curr += 1
                self.p("symbol")
                self.curr += 1
                self.comp_exp()



    def comp_term(self):
        if "identifier" in self.file_lines[self.curr]:
            self.p("identifier")

            if "[" in self.file_lines[self.curr + 1]:
                self.curr += 1
                self.p("symbol")
                self.curr += 1
                self.out_file.write(" " * self.i + "<expression>\n")
                self.comp_exp()

                self.out_file.write(" " * self.i + "</expression>\n")
                self.p("symbol")
                self.curr += 1
            elif "(" in self.file_lines[self.curr + 1]:
                self.curr += 1
                self.p("symbol")
                self.curr += 1
                self.out_file.write(" " * self.i + "<expressionList>\n")
                self.comp_explist()

                self.out_file.write(" " * self.i + "</expressionList>\n")
                self.p("symbol")
                self.curr += 1
            elif "." in self.file_lines[self.curr + 1]:
                self.curr += 1
                self.p("symbol")
                self.curr += 1
                self.p("identifier")
                self.curr += 1
                self.p("symbol")
                self.curr += 1
                self.out_file.write(" " * self.i + "<expressionList>\n")
                self.comp_explist()

                self.out_file.write(" " * self.i + "</expressionList>\n")
                self.p("symbol")
                self.curr += 1
            else:
                self.curr += 1
        elif "integerConstant" in self.file_lines[self.curr]:
            self.p("integerConstant")
            self.curr += 1
        elif "stringConstant" in self.file_lines[self.curr]:
            self.p("stringConstant")
            self.curr += 1

        elif self.file_lines[self.curr].split(" ")[1] in "truefalsenullthis":
            self.p("keyword")
            self.curr += 1
        elif "(" in self.file_lines[self.curr]:
            self.p("symbol")
            self.curr += 1
            self.out_file.write(" " * self.i + "<expression>\n")
            self.comp_exp()

            self.out_file.write(" " * self.i + "</expression>\n")
            self.p("symbol")
            self.curr += 1
        else:

            self.p("symbol")
            self.curr += 1
            self.out_file.write(" " * self.i + "<term>\n")
            self.comp_term()
            self.out_file.write(" " * self.i + "</term>\n")

import sys
if len(sys.argv) > 1:
    a = analyzer(sys.argv[1])
    a.close()
else:
    a = analyzer(input("Enter filename:"))
    a.close()
