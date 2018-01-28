@R2 // Sets R2 to zero
M=0
(LOOP) // Loops until R0 is 0
@R0
D=M //Loads the value in the D register
@END // If yes then just end everything
D;JEQ
@R0 // Goes to R0 again
M=M-1 // Decrements R0
@R1 // goes to R1
D=M // Loads the Value into the D register
@R2// Goes to R2
M=M+D // adds R2 twice
@LOOP // ends the loop
0;JMP
(END)
@END
0;JMP
