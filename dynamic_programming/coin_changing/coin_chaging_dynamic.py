#!/bin/python3
# dynamic programming implementation to get all ways.  
# same solution as niave approach, but passes around global dictionary to keep subproblem solutions
# scaling: O(nm)
# solutions dictionary is set up as: outer key: n, inner key: current

import sys

def getWays(n, c, current, solutions):
    
    # base case (check if current denomination divides the current total)
    if(current == 0):
        if(not n % c[current]):
            return 1
        else:
            return 0
    
    count = 0
    for ways in range(n // c[current] + 1):
        
        # update
        new_n = n - c[current] * ways
        new_current = current - 1
        
        # check if this problem has already been computed
        if(new_n in solutions and new_current in solutions[new_n]):
            solution = solutions[new_n][new_current] 
            
        else:
            # compute the solution
            solution = getWays(new_n, c, new_current, solutions)
    
            # add it to solutions
            if(new_n in solutions):
                solutions[new_n][new_current] = solution
            else:
                solutions[new_n] = {new_current : solution}
        
        # increment count
        count += solution
    
    return count

if __name__ == "__main__":
    n, m = input().strip().split(' ')
    n, m = [int(n), int(m)]
    c = list(map(int, input().strip().split(' ')))
    # Print the number of ways of making change for 'n' units using coins having the values given by 'c'
    ways = getWays(n, c, len(c)-1, {})
    print(ways)


