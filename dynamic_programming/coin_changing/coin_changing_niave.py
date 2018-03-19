#!/bin/python3
# Niave implementation to get all ways.  
# recurse denominations from largest to smalles.
# divide the problem up as {n - 0 * current, ... , n - n // current * current}
# check if current is the last denomination, if it divides n, return 1, else return 0
# scaling is exponential :o

import sys
from copy import deepcopy

def getWays(n, c, current):
    
    # base case (check if current denomination divides the current total)
    if(current == 0):
        if(not n % c[current]):
            return 1
        else:
            return 0
    
    count = 0
    for ways in range(n // c[current] + 1):
        count += getWays(n - c[current] * ways, c, current-1)
    
    return count

if __name__ == "__main__":
    n, m = input().strip().split(' ')
    n, m = [int(n), int(m)]
    c = list(map(int, input().strip().split(' ')))
    # Print the number of ways of making change for 'n' units using coins having the values given by 'c'
    ways = getWays(n, c, len(c)-1)
    print(ways)


