# BlackJack
It is easy to guess that to unlock the flag we have to win this game.
This challenge may seem difficult, but don't let it fool you :)
## Solution

Initially the length of the code scared me a bit, but it was enough for me to read how the play() function works to find the solution.
In particular, when it calling the betting() function.
```
int betting() //Asks user amount to bet
{
 printf("\n\nEnter Bet: $");
 scanf("%d", &bet);

 if (bet > cash) //If player tries to bet more money than player has
 {
		printf("\nYou cannot bet more money than you have.");
		printf("\nEnter Bet: ");
        scanf("%d", &bet);
        return bet;
 }
 else return bet;
} // End Function
```
This function takes an integer as input and checks that it is not greater than our budget. So... how we can fool it?

If we lose, the number we entered is immediately subtracted from our budget.
```
if(p>21) //If player total is over 21, loss
{
    printf("\nWoah Buddy, You Went WAY over.\n");
    loss = loss+1;
    cash = cash - bet;
    printf("\nYou have %d Wins and %d Losses. Awesome!\n", won, loss);
    dealer_total=0;
    askover();
}
```
Since it doesn't check if the input is a positive or negative number, I tried to enter a negative number and when I lost my budget it increased :D
```
Cash: $500
-------
|D    |
|  Q  |
|    D|
-------

Your Total is 10

The Dealer Has a Total of 4

Enter Bet: $-10


Would You Like to Hit or Stay?
Please Enter H to Hit or S to Stay.
S

You Have Chosen to Stay at 10. Wise Decision!

The Dealer Has a Total of 11
The Dealer Has a Total of 18
Dealer Has the Better Hand. You Lose.

You have 0 Wins and 1 Losses. Awesome!

Would You Like To Play Again?
Please Enter Y for Yes or N for No
Y

-----------------------------------------------

Cash: $510
-------
|D    |
|  6  |
|    D|
-------

Your Total is 6

The Dealer Has a Total of 6

Enter Bet: $
```
To get the flag it was enough for me to "win" a million dollars.

It has never been easier to become a millionaire!