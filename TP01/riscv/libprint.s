	.globl	println_int
println_int:
	addi sp,sp,-8
	sd   ra, 0(sp)
	call print_int
	call newline
	ld   ra, 0(sp)
	addi sp,sp,8
	ret
	
	.globl	println_char
println_char:
	addi sp,sp,-8
	sd   ra, 0(sp)
	call print_char
	call newline
	ld   ra, 0(sp)
	addi sp,sp,8
	ret

	.text
	.align	1
	.globl	println_string
	.type	println_string, @function
println_string: #address stored in a0
	addi	sp,sp,-152
	sd	ra,24(sp)
	sd	s0,16(sp)
	addi	s0,sp,32
        sd      t0,32(sp)
        sd      t1,40(sp)
        sd      t2,48(sp)
        sd      t3,56(sp)
        sd      t4,64(sp)
        sd      t5,72(sp)
        sd      t6,80(sp)

        sd      a0,88(sp)
        sd      a1,96(sp)
        sd      a2,104(sp)
        sd      a3,112(sp)
        sd      a4,120(sp)
        sd      a5,128(sp)
        sd      a6,136(sp)
        sd      a7,144(sp)

	## Argument is already in a0, just forward it to puts
	call	puts

	ld	ra,24(sp)
	ld	s0,16(sp)

        ld      t0,32(sp)
        ld      t1,40(sp)
        ld      t2,48(sp)
        ld      t3,56(sp)
        ld      t4,64(sp)
        ld      t5,72(sp)
        ld      t6,80(sp)

        ld      a0,88(sp)
        ld      a1,96(sp)
        ld      a2,104(sp)
        ld      a3,112(sp)
        ld      a4,120(sp)
        ld      a5,128(sp)
        ld      a6,136(sp)
        ld      a7,144(sp)

	addi	sp,sp,152
	jr	ra
	.size	println_string, .-println_string
	.section	.rodata
	.align	3
fmt_int:
	.string	"%ld"
str_empty:
	.string	""
	.text
	.align	1
	.globl	print_int
	.type	print_int, @function
print_int: # print int stored in a0, saves/restores all scratch registers (except ft<n> which we don't use)
	addi	sp,sp,-152

	sd	ra,24(sp)
	sd	s0,16(sp)

        sd      t0,32(sp)
        sd      t1,40(sp)
        sd      t2,48(sp)
        sd      t3,56(sp)
        sd      t4,64(sp)
        sd      t5,72(sp)
        sd      t6,80(sp)

        sd      a0,88(sp)
        sd      a1,96(sp)
        sd      a2,104(sp)
        sd      a3,112(sp)
        sd      a4,120(sp)
        sd      a5,128(sp)
        sd      a6,136(sp)
        sd      a7,144(sp)

	## first parameter of print_int is second parameter of printf
	mv	a1,a0
	## first parameter of printf is the format string
	la	a0,fmt_int
	call	printf

	ld	ra,24(sp)
	ld	s0,16(sp)

        ld      t0,32(sp)
        ld      t1,40(sp)
        ld      t2,48(sp)
        ld      t3,56(sp)
        ld      t4,64(sp)
        ld      t5,72(sp)
        ld      t6,80(sp)

        ld      a0,88(sp)
        ld      a1,96(sp)
        ld      a2,104(sp)
        ld      a3,112(sp)
        ld      a4,120(sp)
        ld      a5,128(sp)
        ld      a6,136(sp)
        ld      a7,144(sp)

	addi	sp,sp,152
	jr	ra
	.size	print_int, .-print_int
	.align	1
	.globl	newline
	.type	newline, @function
newline: # print int stored in a0, saves/restores all scratch registers (except ft<n> which we don't use)
	addi	sp,sp,-152

	sd	ra,24(sp)
	sd	s0,16(sp)

        sd      t0,32(sp)
        sd      t1,40(sp)
        sd      t2,48(sp)
        sd      t3,56(sp)
        sd      t4,64(sp)
        sd      t5,72(sp)
        sd      t6,80(sp)

        sd      a0,88(sp)
        sd      a1,96(sp)
        sd      a2,104(sp)
        sd      a3,112(sp)
        sd      a4,120(sp)
        sd      a5,128(sp)
        sd      a6,136(sp)
        sd      a7,144(sp)

	## first parameter of printf is the format string
	la	a0,str_empty
	call	puts

	ld	ra,24(sp)
	ld	s0,16(sp)

        ld      t0,32(sp)
        ld      t1,40(sp)
        ld      t2,48(sp)
        ld      t3,56(sp)
        ld      t4,64(sp)
        ld      t5,72(sp)
        ld      t6,80(sp)

        ld      a0,88(sp)
        ld      a1,96(sp)
        ld      a2,104(sp)
        ld      a3,112(sp)
        ld      a4,120(sp)
        ld      a5,128(sp)
        ld      a6,136(sp)
        ld      a7,144(sp)

	addi	sp,sp,152
	jr	ra
	.size	newline, .-newline
	.align	1
	.globl	print_char
	.type	print_char, @function
print_char: # print char stored in a0 (ascii code)
	addi	sp,sp,-152
	sd	ra,24(sp)
	sd	s0,16(sp)

	addi	s0,sp,32


        sd      t0,32(sp)
        sd      t1,40(sp)
        sd      t2,48(sp)
        sd      t3,56(sp)
        sd      t4,64(sp)
        sd      t5,72(sp)
        sd      t6,80(sp)

        sd      a0,88(sp)
        sd      a1,96(sp)
        sd      a2,104(sp)
        sd      a3,112(sp)
        sd      a4,120(sp)
        sd      a5,128(sp)
        sd      a6,136(sp)
        sd      a7,144(sp)

	# call to putchar
	mv	a5,a0
	sb	a5,-17(s0)
	lbu	a5,-17(s0)
	sext.w	a5,a5
	mv	a0,a5
	call	putchar

	#restore registers
	ld	ra,24(sp)
	ld	s0,16(sp)

        ld      t0,32(sp)
        ld      t1,40(sp)
        ld      t2,48(sp)
        ld      t3,56(sp)
        ld      t4,64(sp)
        ld      t5,72(sp)
        ld      t6,80(sp)

        ld      a0,88(sp)
        ld      a1,96(sp)
        ld      a2,104(sp)
        ld      a3,112(sp)
        ld      a4,120(sp)
        ld      a5,128(sp)
        ld      a6,136(sp)
        ld      a7,144(sp)

	addi	sp,sp,152
	jr	ra
	.size	print_char, .-print_char


