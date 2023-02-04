# Bof
# Solution
Analyzing the bof.c file we notice that there is a buffer of length 32, without any type of control over the length.
We know that the get() function takes an input of infinite length until you hit enter.

The key must be equal to 0xcafebabe.

I calculate the offset between the memory address where the input is placed and the one where the key variable passed as input to the function is stored and I send in the get() function 52 'A' to identify where the input is saved and after 52, the input overwrites the key variable in input to the function.

Since the function needs to be run remotely, remote from pwntools is used.
## Usage
```
python exploi_remote.py
```