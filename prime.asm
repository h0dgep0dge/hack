@MAIN
0;JMP

(MULT) // Computers R2*R3, placing the product in R1, and jumps to R0
    @count$MULT
    M=0
    @product$MULT
    M=0

    (MULTLOOP)
        @count$MULT
        D=M
        @R2
        D=M-D
        @MULTBREAK
        D;JLE // Break loop if count >= R2

        @count$MULT
        M=M+1 // Increment count

        @R3
        D=M
        @product$MULT
        M=D+M // Add R3 to the product

    @MULTLOOP
    0;JMP

    (MULTBREAK)

    @product$MULT
    D=M
    @R1
    M=D // Store product at R1
    @R0
    A=M
    0;JMP // Jump back to main

(DIV) // Computes R3/R4, placing the result in R1 and the remainder in R2, and jumps to R0
    @count$DIV
    M=0
    @R3
    D=M
    @dividend$DIV
    M=D

    (DIVLOOP)
    
        @dividend$DIV
        D=M
        @R4
        A=M
        D=D-A
        @DIVBREAK
        D;JLT

        @dividend$DIV
        M=D
        @count$DIV
        M=M+1

    @DIVLOOP
    0;JMP

    (DIVBREAK)

    @count$DIV
    D=M
    @R1
    M=D
    @dividend$DIV
    D=M
    @R2
    M=D
    @R0
    A=M
    0;JMP

(ISPRIME) // Computes if R2 is prime, setting R1 to 1 if so, and jumps to R0
    @R2
    D=M
    @test$ISPRIME
    M=D

    @R0
    D=M
    @return$ISPRIME
    M=D


    @test$ISPRIME
    D=M-1
    @FALSE$ISPRIME
    D;JLE // 1 or less is not prime

    @test$ISPRIME
    D=M
    @2
    D=D-A
    @TRUE$ISPRIME
    D;JEQ // 2 is prime

    @2
    D=A
    @counter$ISPRIME
    M=D // starting the counter at 2

    (LOOP$ISPRIME)

    @counter$ISPRIME
    D=M
    @PRINT
    M=D


    @test$ISPRIME
    D=M
    @R3
    M=D

    @counter$ISPRIME
    D=M
    @R4
    M=D

    @ISPRIME$1
    D=A
    @R0
    M=D

    @DIV
    0;JMP

    (ISPRIME$1)

    @R2
    D=M
    @FALSE$ISPRIME
    D;JEQ


    @counter$ISPRIME // Increment the divisor
    M=M+1

    @counter$ISPRIME
    D=M
    @R2
    M=D
    @R3
    M=D
    @ISPRIME$2
    D=A
    @R0
    M=D

    @MULT
    0;JMP

    (ISPRIME$2)

    @R1
    D=M
    @test$ISPRIME
    D=D-M
    @TRUE$ISPRIME
    D;JGT

    @LOOP$ISPRIME
    0;JMP

    (TRUE$ISPRIME)
        @R1
        M=1
        @return$ISPRIME
        A=M
        0;JMP
    (FALSE$ISPRIME)
        @counter$ISPRIME
        D=M
        @PRINT
        M=D
        @R1
        M=0
        @return$ISPRIME
        A=M
        0;JMP


(MAIN)
@19997
D=A
@R2
M=D

@MAIN$1
D=A
@R0
M=D

@ISPRIME
0;JMP

(MAIN$1)
@R1
D=M
@PRINT
M=D

@HALT
0;JMP