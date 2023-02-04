# CMD1
## Solution
The cmd1.c file takes a command as input, but if 'sh', 'flag' or 'tmp' is present in the command it does not execute it.
```
int filter(char* cmd){
	int r=0;
	r += strstr(cmd, "flag")!=0;
	r += strstr(cmd, "sh")!=0;
	r += strstr(cmd, "tmp")!=0;
	return r;
}
```
You can bypass this check with the escape character \\.

In this way the filtering operations are performed on the string "$exploit", which is replaced with the command "/bin/cat flag" directly in the system() function.

I have create and environment variable:
```
export exploit="/bin/cat flag"
```
In this case it was possible to do this thanks to the system() function, which does not directly execute the command, but spawns a shell and executes the command.
This made it interpret the environment variable and not just execute the $exploit 'command', which would have happened with the exec() function instead