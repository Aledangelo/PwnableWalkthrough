# Fd
## Solution
In the file fd.c there is the variable fd (file descriptor), used to represent a file to be taken as input.
```
int fd = atoi( argv[1] ) - 0x1234;
```
It is calculated by subtracting the input from the number 0x1234 (4660 in decimal)

We know that in the read function, putting 0 (standard input) in place of fd, the input will be taken from the terminal
```
len = read(fd, buf, 32);
```
We just need to enter the string present in the if statement "LETMEWIN" and the flag is printed.
```
if(!strcmp("LETMEWIN\n", buf)){
    printf("good job :)\n");
    system("/bin/cat flag");
    exit(0);
}
```