# CMD2
## Solution
I don't know why, but the old soluiton didn't work here :(

I had to look for another way to bypass the filter and I found on the internet the way to pass the octal representation of the character '/'
```
./cmd2 '$(printf "%bbin%bcat %s%s" "\57" "\57" "fl" "ag")'
```
So I managed to pass the command: 
```
printf(/bin/cat flag)
```