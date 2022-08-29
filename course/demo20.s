#simple RISCV assembly demo
#riscv64-unknown-elf-gcc  demo20.s ../../TP/TP01/code/libprint.s -o demo20
#spike pk demo20
	.text
	.globl main
main:
        addi    sp,sp,-16
        sd      ra,8(sp)
# your assembly code here
	addi t1, zero, 5 		# first op : cte
	la t3, foo                   # second, from memory
	ld t4, 0(t3)
	add a0, t1, t4                  # add --> a0 = result
	call print_int
	call newline
## /end of user assembly code
        ld      ra,8(sp)
        addi    sp,sp,16
        ret
	.section .rodata
foo:
	.dword 37
