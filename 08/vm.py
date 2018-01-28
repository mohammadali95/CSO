import parser_real
import code_writer

class vm:
    #got help from Karthik on how to take multiple files and put the output into one file.
    def __init__ (self, file_or_path):
        self.file_or_path = file_or_path
        if ".vm" not in self.file_or_path:
            import os
            os.chdir(self.file_or_path)
            self.code_writer = code_writer.code_writer(self.file_or_path)
            self.code_writer.write_init()
            for files in os.listdir():
                if '.vm' in files:
                    self.file = files
                    self.code_writer.set_file_name(files[:-3])
                    self.translate()
        else:
            self.file = self.file_or_path
            self.code_writer = code_writer.code_writer(self.file_or_path[:-3])
            self.code_writer.set_file_name(self.file[:-3])
            self.translate()



    def translate(self):
        p =  parser_real.parser(self.file)
        while p.has_more_commands():
            p.advance()
            if p.command_type() == "C_ARITHMETIC":
                self.code_writer.write_arith(p.arg1())
            elif p.command_type() == "C_PUSH" or p.command_type() == "C_POP":
                self.code_writer.write_push_pop(p.command_type(), p.arg1(), p.arg2())
            elif p.command_type() == "C_LABEL":
                self.code_writer.write_label(p.arg1())
            elif p.command_type() == "C_FUNCTION":
                self.code_writer.write_function(p.arg1(), p.arg2())
            elif p.command_type() == "C_CALL":
                self.code_writer.write_call(p.arg1(), p.arg2())
            elif p.command_type() == "C_RETURN":
                self.code_writer.write_return()
            elif p.command_type() == "C_GOTO":
                self.code_writer.write_goto(p.arg1())
            elif p.command_type() == "C_IF":
                self.code_writer.write_if_goto(p.arg1())
        # self.code_writer.close_file()

import os
import sys
if len(sys.argv) > 1:
    vm = vm(sys.argv[1])


# files = os.listdir()
# vms = []
# for file in files:
#     if ".vm" in file:
#         vms.append(file)
# for v in vms:
#     print (v)
#     vm = vm(v)
#     vm.translate()
# if len(sys.argv) > 1:
#     vm = vm(sys.argv[1])
#     vm.translate()
# else:
#     vm = vm(input("Enter filename:"))
#     vm.translate()
