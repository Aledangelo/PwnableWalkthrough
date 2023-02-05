# Input
# Solution
After looking at the input.c file you notice that there are several conditions that cause the program to stop based on the input.

### Argv
These are the first three conditions based on argv:
```
if(argc != 100) return 0;
if(strcmp(argv['A'],"\x00")) return 0;
if(strcmp(argv['B'],"\x20\x0a\x0d")) return 0;
printf("Stage 1 clear!\n");	
```
* There must be 100 args in input
* The ASCII representation of A is 65, so the 65th arg must be "\x00"
* Reasoning in the same way for B, the 66th arg must be "\x20\x0a\x0d"

### Stdio
In the second stage we have:
```
char buf[4];
read(0, buf, 4);
if(memcmp(buf, "\x00\x0a\x00\xff", 4)) return 0;
read(2, buf, 4);
if(memcmp(buf, "\x00\x0a\x02\xff", 4)) return 0;
printf("Stage 2 clear!\n");
```
* At first, the read() function read from stdin and save the data in buf[4], it must be equal to "\x00\x0a\x00\xff"
* The second read() read data from stderr, and it must be equal to "\x00\x0a\x02\xff"


### Env
In the third stage we have to work with environment variables:
```
if(strcmp("\xca\xfe\xba\xbe", getenv("\xde\xad\xbe\xef"))) return 0;
printf("Stage 3 clear!\n");
```
* We need to set an environment variable named "\xde\xad\xbe\xef" with the value "\xca\xfe\xba\xbe"

### File
Here we have to work with files:
```
FILE* fp = fopen("\x0a", "r");
if(!fp) return 0;
if( fread(buf, 4, 1, fp)!=1 ) return 0;
if( memcmp(buf, "\x00\x00\x00\x00", 4) ) return 0;
fclose(fp);
printf("Stage 4 clear!\n");	
```
* It must be a file named "\x0a"
* In this file there must be written "\x00\x00\x00\x00"

**PAY ATTENTION**: our user doesn't have permission to write in /home/input2 directory! We have to bypass this obstacle, how we can do that?

A possible solution could be to use the symbolic links. I have created two symbolic links in the directory where I put the exploit.py file.
```
ln -s /home/input2/input input
ln -s /home/input2/flag flag
```
In this way, our exploit can create the file and the symbolic link to the executable can read the file.

### Network
To pass the last check we need to work with sockets:
```
int sd, cd;
struct sockaddr_in saddr, caddr;
sd = socket(AF_INET, SOCK_STREAM, 0);
if(sd == -1){
    printf("socket error, tell admin\n");
    return 0;
}
saddr.sin_family = AF_INET;
saddr.sin_addr.s_addr = INADDR_ANY;
saddr.sin_port = htons( atoi(argv['C']) );
if(bind(sd, (struct sockaddr*)&saddr, sizeof(saddr)) < 0){
    printf("bind error, use another port\n");
        return 1;
}
listen(sd, 1);
int c = sizeof(struct sockaddr_in);
cd = accept(sd, (struct sockaddr *)&caddr, (socklen_t*)&c);
if(cd < 0){
    printf("accept error, tell admin\n");
    return 0;
}
if( recv(cd, buf, 4, 0) != 4 ) return 0;
if(memcmp(buf, "\xde\xad\xbe\xef", 4)) return 0;
printf("Stage 5 clear!\n");
```

* The file start a listening socket
* The port number is taken from args['C'], so it's args[67]
* We need to send the value "\xde\xad\xbe\xef" on this socket

## Usage
```
python3 exploit.py
```