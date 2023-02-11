# Blukat
This challenge is very very easy, but I only realized it at the end, after won the challenge in a more difficult way...

## Solution
I created on my local machine the directory `home/blukat/` and I put inside it the file `password` written by me.
```
mkdir /home/blukat
echo "qwerty" >> /home/blukat/password
```
I did this because the program tries to open the file `/home/blukat/password`
```
int main(){
	FILE* fp = fopen("/home/blukat/password", "r");
	fgets(password, 100, fp);
...
```
After that, I started the program with gdb and inspected the processor registers values after the fgets() function was executed. I preferred running gdb on my pc because I have on it **pwndbg**, which is a more user-friendly version of the classic gdb debugger.
```
   0x400824 <main+42>    mov    rax, qword ptr [rbp - 0x78]
   0x400828 <main+46>    mov    rdx, rax
   0x40082b <main+49>    mov    esi, 0x64
   0x400830 <main+54>    mov    edi, password                 <0x6010a0>
   0x400835 <main+59>    call   fgets@plt                      <fgets@plt>
 
 ► 0x40083a <main+64>    mov    edi, 0x400982
   0x40083f <main+69>    call   puts@plt                      <puts@plt>
 
   0x400844 <main+74>    mov    rdx, qword ptr [rip + 0x200835] <stdin@@GLIBC_2.2.5>
   0x40084b <main+81>    lea    rax, [rbp - 0x70]
   0x40084f <main+85>    mov    esi, 0x80
   0x400854 <main+90>    mov    rdi, rax
─────────────────────────────────────────────────────────────────────────────────────────────────[ STACK ]─────────────────────────────────────────────────────────────────────────────────────────────────
00:0000│ rsp 0x7ffc6ba39180 ◂— 0x2
01:0008│     0x7ffc6ba39188 —▸ 0x7562a0 ◂— 0xfbad2488
02:0010│     0x7ffc6ba39190 ◂— 0x0
... ↓        5 skipped
───────────────────────────────────────────────────────────────────────────────────────────────[ BACKTRACE ]───────────────────────────────────────────────────────────────────────────────────────────────
 ► f 0         0x40083a main+64
   f 1   0x7fc5af8f8d90 __libc_start_call_main+128
   f 2   0x7fc5af8f8e40 __libc_start_main+128
   f 3         0x4006b9 _start+41
───────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────
pwndbg> x/ls $rax
0x6010a0 <password>:	"qwerty\n"
pwndbg>
```
So in the `$rax` register, just after running the `fgets()` function, we can find the value of the "password" file. Now that I know where to read the contents of the file, I repeated the same steps connecting myself to `blukat@pwnable.kr` with ssh.
```
...
(gdb) run
Starting program: /home/blukat/blukat 

Breakpoint 1, 0x00000000004007fe in main ()
(gdb) next
Single stepping until exit from function main,
which has no line number information.

Breakpoint 2, 0x0000000000400830 in main ()
(gdb) next
Single stepping until exit from function main,
which has no line number information.

Breakpoint 3, 0x000000000040083a in main ()
(gdb) x/ls $rax
0x6010a0 <password>:	"cat: password: Permission denied\n"
```
So the password actually is "cat: password: Permission denied".

## Easy way
Trying to read the password file with the `more` command, it produces this output:
```
blukat@pwnable:~$ more password 
cat: password: Permission denied
```
It was easy to understand that this was the content of the file and not an error message.

But it doesn't matter, at least I practiced a bit with gdb.