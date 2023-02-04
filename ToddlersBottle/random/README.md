# Random
## Solution
Analyzing the random.c file it's clear that to obtain the flag, the XOR between the key and random variables must be equal to **0xdeadbeef**.

With gdb you can see that the rand() function always outputs the same number i.e. **0x6b8b4567**.
This number is saved on the stack and the input of the scanf function is saved immediately afterwards.

To guess the key, simply perform a XOR operation between the 'random' number and the number to obtain.