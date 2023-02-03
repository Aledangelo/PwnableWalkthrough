## col: setuid ELF 32-bit LSB executable, Intel 80386, version 1 (SYSV), dynamically linked, interpreter /lib/ld-linux.so.2, for GNU/Linux 2.6.24, BuildID[sha1]=05a10e253161f02d8e6553d95018bc82c7b531fe, not stripped
from pwn import *

h = 0x21DD09EC
data = 'A' * 16
data = data.encode()

res = 0

for i in range(0,4):
    d = data[i*4:(i+1)*4]
    int_d = int.from_bytes(d, 'little')
    res += int_d
    res = res & 0xFFFFFFFF      # trunc on 32 bit

off = h - res
off = off & 0xFFFFFFFF
off = off.to_bytes(byteorder='little', length=4)

inp = data + off

print(inp)

command = ['./col', inp]
p = process(command)
p.interactive()