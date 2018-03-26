
class SegmentTree(object):
    
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

