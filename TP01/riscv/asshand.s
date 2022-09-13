       .globl main
main:	
	addi a0, a0, 1
	bne a0, a0, main
end:
	ret
