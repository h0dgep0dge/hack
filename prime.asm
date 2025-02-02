@MAIN
0;JMP

(MULT)


@count
M=0
@product
M=0

(MULTLOOP)
@count
D=M
@R1
D=M-D
@MULTBREAK
D;JLE

@count
M=M+1

@R2
D=M
@product
M=D+M

@MULTLOOP
0;JMP

(MULTBREAK)

@product
D=M
@R0
M=D
@CONTINUE
0;JMP


(MAIN)
@123
D=A
@R1
M=D

@99
D=A
@R2
M=D

@MULT
0;JMP

(CONTINUE)
@R0
D=M
@PRINT
M=D

@HALT
0;JMP