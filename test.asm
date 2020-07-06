	.ORIG x3000
	LD R1,Address
	ADD R2,R2,#15
	ADD R2,R2,R2
	ADD R2,R2,R2
	ADD R4,R2,#0 ;R4 store 60
	ADD R2,R2,#15
	ADD R2,R2,#15
	ADD R2,R2,#11	;R2 conunts 101
	ADD R6,R6,R2 ;R6 store 101
	ADD R3,R3,#-1
LOOP	STR R3,R1,#0
	ADD R1,R1,#1 ;address+1
	ADD R2,R2,#-1
	BRp LOOP

; set -1 form 0x4000 to 0x4064

	LD R1,Scores ;Address in R1
	ADD R2,R4,#0 ;counts in R2
	LD R5,Max ;0x4064 in R5
LOOP2	LDR R3,R1,#0 ;scores in R3
	NOT R4,R3
	ADD R4,R4,#1
	ADD R4,R4,R5 ;new address in R4
	STR R3,R4,#0 ;score be stored in the address
	ADD R1,R1,#1
	ADD R2,R2,#-1
	BRp LOOP2

; insert scores form 0x4000 to 0x4064

	LD R1,Address ;Address in R1
	ADD R4,R1,#0  ;R4 stored address
	ADD R2,R6,#0 ;counts in R2 101
	AND R6,R6,#0 ;to counts the A B D numbles
	AND R5,R5,#0
	ADD R0,R0,#15 ;R0 is to judge A
	AND R7,R7,#0
	ADD R7,R7,#10
	LD R5,Grade
LOOP3	LDR R3,R1,#0
	BRn LOOP4
	STR R3,R4,#0
	ADD R4,R4,#1
	ADD R6,R6,#1 ;counts the numbers

	ADD R0,R0,#-1
	BRn LOOP6

LP6_re	ADD R1,R1,#1
	ADD R2,R2,#-1
	BRp LOOP3
	BRnzp LOOP5
LOOP4	ADD R1,R1,#1

	ADD R0,R0,#-1
	BRn LOOP7

LP7_re	ADD R2,R2,#-1
	BRp LOOP3

LOOP5	HALT

LOOP6	STR R6,R5,#0 ;
	ADD R0,R0,R7
	ADD R5,R5,#1 ; address plus 1
	AND R6,R6,#0
	ADD R7,R7,#15
	ADD R7,R7,R7
	ADD R7,R7,R7
	NOT R7,R7
	ADD R7,R7,#1
	ADD R7,R7,R2
	BRz JUDGE6
	AND R7,R7,#0
	ADD R7,R7,#15
	BRnzp ELP6
JUDGE6	NOT R7,R7
	ADD R7,R7,#1
ELP6	BRnzp LP6_re

LOOP7	STR R6,R5,#0 ;
	ADD R0,R0,R7
	ADD R5,R5,#1 ; address plus 1
	AND R6,R6,#0
	ADD R7,R7,#15
	ADD R7,R7,R7
	ADD R7,R7,R7
	NOT R7,R7
	ADD R7,R7,#1
	ADD R7,R7,R2
	BRz JUDGE7
	AND R7,R7,#0
	ADD R7,R7,#15
	BRnzp ELP7
JUDGE7	NOT R7,R7
	ADD R7,R7,#1
ELP7	BRnzp LP7_re

Address	.FILL x4000
Scores	.FILL x3200
Max	.FILL x4064
Grade	.FILL x4100
	.END