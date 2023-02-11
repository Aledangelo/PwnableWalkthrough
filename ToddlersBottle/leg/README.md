# Leg
## Solution
In the main function we see that to get the flag, our input must be equal to the output of the key1+key2+key3 functions.
```
printf("Daddy has very strong arm! : ");
	scanf("%d", &key);
	if( (key1()+key2()+key3()) == key ){
		printf("Congratz!\n");
		int fd = open("flag", O_RDONLY);
		char buf[100];
		int r = read(fd, buf, 100);
		write(0, buf, r);
	}
```

We are given an .asm file to be able to parse the assembly code of the executable file.
We can see the assembly code of these three functions.
* Key1()
```
(gdb) disass key1
Dump of assembler code for function key1:
   0x00008cd4 <+0>:	push	{r11}		; (str r11, [sp, #-4]!)
   0x00008cd8 <+4>:	add	r11, sp, #0
   0x00008cdc <+8>:	mov	r3, pc
   0x00008ce0 <+12>:	mov	r0, r3
   0x00008ce4 <+16>:	sub	sp, r11, #0
   0x00008ce8 <+20>:	pop	{r11}		; (ldr r11, [sp], #4)
   0x00008cec <+24>:	bx	lr
End of assembler dump.
```
Before the `mov r0, r3` instruction is executed, r3 is loaded with the value of the program counter (PC), which is the address of the current instruction being executed. After the mov instruction, the value of the PC is stored in the r0 register.

The value inside the r0 register after executing these instructions would be equal to the value inside the r3 register. This is because the instruction at `0x00008ce0` performs a `mov r0, r3` operation, which transfers the contents of the r3 register into the r0 register.

* Key2
```
(gdb) disass key2
Dump of assembler code for function key2:
   0x00008cf0 <+0>:	push	{r11}		; (str r11, [sp, #-4]!)
   0x00008cf4 <+4>:	add	r11, sp, #0
   0x00008cf8 <+8>:	push	{r6}		; (str r6, [sp, #-4]!)
   0x00008cfc <+12>:	add	r6, pc, #1
   0x00008d00 <+16>:	bx	r6
   0x00008d04 <+20>:	mov	r3, pc
   0x00008d06 <+22>:	adds	r3, #4
   0x00008d08 <+24>:	push	{r3}
   0x00008d0a <+26>:	pop	{pc}
   0x00008d0c <+28>:	pop	{r6}		; (ldr r6, [sp], #4)
   0x00008d10 <+32>:	mov	r0, r3
   0x00008d14 <+36>:	sub	sp, r11, #0
   0x00008d18 <+40>:	pop	{r11}		; (ldr r11, [sp], #4)
   0x00008d1c <+44>:	bx	lr
End of assembler dump.
```

At `0x00008d04`, the `mov r3, pc` instruction stores the current value of the PC into the r3 register. The next instruction, `adds r3, #4`, adds 4 to the value stored in the r3 register. The code then pushes the value stored in r3 onto the stack, pops the value off the stack into the program counter (PC), and finally pops the value off the stack into the r6 register. This causes the program to jump to the instruction located at r3, which was previously updated to be `PC + 4`. Finally, the `mov r0, r3` instruction at `0x00008d10` transfers the contents of the r3 register into the r0 register, so the value inside r0 would be equal to the value stored in r3 after it was updated with the adds instruction.

* Key3
```
Dump of assembler code for function key3:
   0x00008d20 <+0>:	push	{r11}		; (str r11, [sp, #-4]!)
   0x00008d24 <+4>:	add	r11, sp, #0
   0x00008d28 <+8>:	mov	r3, lr
   0x00008d2c <+12>:	mov	r0, r3
   0x00008d30 <+16>:	sub	sp, r11, #0
   0x00008d34 <+20>:	pop	{r11}		; (ldr r11, [sp], #4)
   0x00008d38 <+24>:	bx	lr
End of assembler dump.
```

After executing the key3 function, the value inside r0 will be the contents of the lr register (link register) at the time the function was called. The link register holds the return address to the instruction after the call to key3, so that the processor knows where to return to after executing the function.