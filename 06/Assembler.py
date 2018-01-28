import Parser
import Code
import Symbol_table_module
import sys


class Assembler:

    def __init__(self, filename):
        self.Symbol_Table = Symbol_table_module.Symbol_table()
        self.code = Code.code_module()
        self.rom = 0
        self.Ram_address = 16
        self.file = filename
        self.out_file = open(self.file.replace(".asm", ".hack"), 'w')
    def first_pass(self):
        parser1 = Parser.Parser_module(self.file)
        while parser1.has_more_commands():
            parser1.advance()
            if parser1.command_type() == "L Command":
                self.Symbol_Table.add_entry(parser1.symbol(), self.rom)

            else:
                self.rom += True

    def second_pass(self):
        parser1 = Parser.Parser_module(self.file)
        while parser1.has_more_commands():
            parser1.advance()

            if parser1.command_type() == "A Command":
                if parser1.symbol().isdigit():
                    a = bin(int(parser1.symbol()))
                    a = a[2:]
                    a = a.zfill(16)
                    self.out_file.write(a + "\n")



                else:
                    if self.Symbol_Table.contains(parser1.symbol()):
                       a = bin(self.Symbol_Table.Get_Address(parser1.symbol()))
                       a = a[2:]
                       a = a.zfill(16)
                       self.out_file.write(a + "\n")


                    else:
                        self.Symbol_Table.add_entry(parser1.symbol(), self.Ram_address)
                        self.Ram_address += True
                        a = bin(self.Symbol_Table.Get_Address(parser1.symbol()))
                        a = a[2:]
                        a = a.zfill(16)
                        self.out_file.write(a + "\n")


            if parser1.command_type() == "C Command":
                a = "111"
                a = a + self.code.comp(parser1.comp())+ self.code.dest(parser1.dest())+ self.code.jump(parser1.jump())
                self.out_file.write(a + "\n")
        self.out_file.close()


def main():
    if len(sys.argv) == 1:
        print("Usage: python3 Text.py file.asm")
        sys.exit(1)
    else:
        run(sys.argv[1])

def run(filename):
    a = Assembler(filename)
    b = a.first_pass()
    c = a.second_pass()


if __name__ == '__main__':
    main()
