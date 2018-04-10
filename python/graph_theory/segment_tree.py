
import sys

class SegmentTree(object):
    
    # this class was constructed with inspiration and guidance from:
    # https://leetcode.com/articles/a-recursive-approach-to-segment-trees-range-sum-queries-lazy-propagation/
    # O(n) leaves, O(n-1) internal nodes.
    # build:  O(n) :D
    # update: O(k), where k = height of tree :D
    # query:  O(k), where k = height of tree :D
    
    def __init__(self, n):
        
        from math import log
        from math import ceil
        
        # The node of the tree is at index 0, thus tree[0] is the root
        # The children of three[i] are tored at tree[2*i+1] and tree[2*i+2]
        # The internal nodes in 
        
        self.n = n
        self.tree = [0] * (2 * 2 ** (ceil(log(n, 2))) - 1)
        self.merge_op = '+'
        
    def build_tree(self, data, ind, lo, hi):
        
        # call as build_tree(data, 0, 0, n-1)
    
        # leaf node, store value
        if (lo == hi):
            self.tree[ind] = data[lo]
            return
        
        # recurse
        mid = lo + (hi - lo) // 2
        self.build_tree(data, 2 * ind + 1, lo, mid)
        self.build_tree(data, 2 * ind + 2, mid + 1, hi)
    
        # merge
        self.tree[ind] = self.merge(self.tree[2 * ind + 1], self.tree[2 * ind + 2])
        
    def merge(self, val1, val2):
        
        if(self.merge_op == '+'):
            return val1 + val2
        
        
    def query(self, ind, lo, hi, i, j):
        # call as query(0, 0, n-1, i, j)
        # where i:j is the slice being queried
        
        if (lo > j or hi < i):
            return 0
        
        if (i <= lo and j >= hi):
            return self.tree[ind]
        
        mid = lo + (hi - lo) // 2
        
        if (i > mid):
            return self.query(2 * ind + 2, mid + 1, hi, i, j)
        elif (j <= mid):
            return self.query(2 * ind + 1, lo, mid, i, j)
        
        lq = self.query(2 * ind + 1, lo, mid, i, mid)
        rq = self.query(2 * ind + 2, mid + 1, hi, mid + 1, j)
    
        return self.merge(lq, rq)
    
    def update_value(self, tind, lo, hi, aind, val):
        # call as update_value(0, 0, n-1, i, val)
        # updates value of array index with val
        
        if (lo = hi):
            tree[tind] = val
            return
        
        mid = lo + (hi - lo) // 2 
        
        if (aind > mid):
            self.update_value(2 * tind + 2, mid + 1, hi, aind, val)
        elif (aind <= mid):
            self.update_value(2 * tind + 1, lo, mid, aind, val)
            
        self.tree[tind] = self.merge(self.tree[2 * tind + 1], self.tree[2 * tind + 2])



