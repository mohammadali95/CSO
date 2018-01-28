import parser_real
import code_writer

class vm():
    def __init__ (self):
       self.code_writer = code_writer.code_writer("StaticTest.vm")

    def translate(self):
        p =  parser_real.parser("StaticTest.vm")
        while p.has_more_commands():
            p.advance()
            if p.command_type() == "C_ARITHMETIC":
                self.code_writer.write_arith(p.arg1())
            elif p.command_type() == "C_PUSH" or p.command_type() == "C_POP":
                self.code_writer.write_push_pop(p.command_type(), p.arg1(), p.arg2())
        self.code_writer.close_file()
    

vm = vm()
vm.translate()
