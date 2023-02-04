# Mistake
## Hint
Operator priority
## Solution
The open() function opens a file and returns a non-negative integer representing the lowest numbered unused as file descriptor (fd).
```
	int fd;
	if(fd=open("/home/mistake/password",O_RDONLY,0400) < 0){
		printf("can't open password %d\n", fd);
		return 0;
	}
```
However, comparison operators such as < are given higher priority than assignment operators =, then the open function is called and it is checked if his output is less than zero, the condition is False so it returns 0.

At this point we have fd = 0. When file descriptor is zero then input is taken from stdin (standard input).
```
    char pw_buf[PW_LEN+1];
	int len;
	if(!(len=read(fd,pw_buf,PW_LEN) > 0)){
		printf("read error\n");
		close(fd);
		return 0;		
	}
```

So it doesn't read the password from the file, but our input.
We have to put a string 10 long, for an example: 
```
1111111111
```
Then you have to enter the password.
There is the variable XORKEY=1, so the password that is entered is put in xor with all 1's.
```
	// xor your input
	xor(pw_buf2, 10);
```
We have to insert 0000000000 as password, so the xor result will be 1111111111 and the flag will be printed on the screen :)
