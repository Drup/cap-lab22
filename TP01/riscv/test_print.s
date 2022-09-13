.section .text
.globl main
main:
	addi	sp,sp,-16
	sd	ra,8(sp)
## Your assembly code there
	la	a0, .LC1
	call	println_string
	li	a0,42
	call	print_int
	call	newline
	li	a0,97
	call	print_char
	li	a0,10 #new line char
	call	print_char
	
## /end of user assembly code
	ld	ra,8(sp)
	addi	sp,sp,16
	ret

# Data comes here
	.section	.data
	.align	3
.LC1:
	.string	"HI MIF08!"
