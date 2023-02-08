# Coin1
This challenge consists in guessing which is the counterfeit coin, with a number of coins that can go from 1 to 999, with a limited number of attempts available in 60 seconds.
```
[+] Start Pwnable Challenge....

	---------------------------------------------------
	-              Shall we play a game?              -
	---------------------------------------------------
	
	You have given some gold coins in your hand
	however, there is one counterfeit coin among them
	counterfeit coin looks exactly same as real coin
	however, its weight is different from real one
	real coin weighs 10, counterfeit coin weighes 9
	help me to find the counterfeit coin with a scale
	if you find 100 counterfeit coins, you will get reward :)
	FYI, you have 60 seconds.
	
	- How to play - 
	1. you get a number of coins (N) and number of chances (C)
	2. then you specify a set of index numbers of coins to be weighed
	3. you get the weight information
	4. 2~3 repeats C time, then you give the answer
	
	- Example -
	[Server] N=4 C=2 	# find counterfeit among 4 coins with 2 trial
	[Client] 0 1 		# weigh first and second coin
	[Server] 20			# scale result : 20
	[Client] 3			# weigh fourth coin
	[Server] 10			# scale result : 10
	[Client] 2 			# counterfeit coin is third!
	[Server] Correct!

	- Ready? starting in 3 sec... -

```

To win this challenge I decided to use a very simple recursive algorithm. Initially I generate numbers from 1 to N, then I split the array in the middle and through the total weight of those numbers I can figure out which of the two lists contains the counterfeit coin. I do this until I get a list with only one number, which is the counterfeit coin.

![alt text](diagram.png)

## Solution

First I created this recursive function, which checks the weight of the left side of the array, then calls itself passing the side of the array with the counterfeit coin.

```
def find_counterfeit_coin(coins, attempts):
    number_of_coins = len(coins)

    if attempts > 0:
        left = coins[:int(math.ceil(number_of_coins/2))]
        right = coins[int(math.trunc(number_of_coins/2)):]

        try:
            left_w = get_weight(args=left)
            left_weight = int(left_w)
        except ValueError:
            print("[-] " + str(left_w))
            return
        attempts -= 1
        if left_weight % 10 == 0:
            attempts = find_counterfeit_coin(coins=right, attempts=attempts)
        else:
            attempts = find_counterfeit_coin(coins=left, attempts=attempts)
    else:
        print("[+] " + str(send_coin(coin=coins)))
```

The get_weight() function sends the list of coins and waits for the response from the server, which will be the total weight of those coins.
```
def get_weight(args):
    cmd = ""
    for i in range(0, len(args)):
        cmd += str(args[i]) + " "

    r.sendline(cmd.encode())
    return r.recvline().decode('utf-8')
```
And finally the send_coin() function sends the counterfeit coin.
```
def send_coin(coin):
    r.sendline(str(coin[0]).encode())
    return r.recvline().decode('utf-8')
```