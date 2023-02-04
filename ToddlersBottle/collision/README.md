# Collision
## Solution
Analyzing the col.c file we note that the input must have a length of 20.
```
if(strlen(argv[1]) != 20){
    printf("passcode length should be 20 bytes\n");
    return 0;
}
```
The check_password() function must return a result equal to the value of the variable hascode=0x21DD09EC.
```
unsigned long check_password(const char* p){
	int* ip = (int*)p;
	int i;
	int res=0;
	for(i=0; i<5; i++){
		res += ip[i];
	}
	return res;
}
```
We see that the function takes the argv as input and adds it in a for loop with 5 iterations.
Reasoning at intervals of 4 bytes, we gradually add 4 'A' in A string of 16 'A' in the res variable and then we subtract it from the hascode variable to calculate the value to put in input.
## Usage
```
python exploit.py
```