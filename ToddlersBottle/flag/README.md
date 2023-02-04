# Flag
## Solution
If you analyze the file with the command:
```
strings -n 12 flag
```
You will see, among the many strings that will appear, these two lines:
```
...
$Info: This file is packed with the UPX executable packer http://upx.sf.net $
$Id: UPX 3.08 Copyright (C) 1996-2011 the UPX Team. All Rights Reserved. $
...
```
UPX is a free, secure, portable, extendable, high-performance executable packer for several executable formats.
Click [here](https://upx.github.io/) if you want to know more about that.

Extract the file with the command:
```
upx -d flag
```
And with the command:
```
strings -n 18 flag | grep UP
```
You will find the flag.