from random import choices
import numpy as np
import time
import functools

# calculate D(e, n)

@functools.lru_cache(128)
def unary_binary_subtrees(e, n):
    if e==0:
        return 0
    elif n==0:
        return 1
    else:
        return unary_binary_subtrees(e-1, n) + unary_binary_subtrees(e, n-1) + unary_binary_subtrees(e+1, n-1)

# calculate distribution K(e,n)

def distribution_k_a(e, n):
    population = []
    weights = []
    for k in range(e):
        population.append( (k, 1))
        e_n = unary_binary_subtrees(e, n)
        weights.append(unary_binary_subtrees(e-k, n-1)/e_n)
        population.append((k, 2))
        weights.append(unary_binary_subtrees(e-k+1, n-1)/e_n)
    return population, weights

# leaves and binary operators

leaves = ["x", "-5", "-4", "-3", "-2", "-1", "1", "2", "3", "4", "5"]
p_leaf = [1/6, 1/12, 1/12, 1/12, 1/12, 1/12, 1/12, 1/12, 1/12, 1/12, 1/12]
binary_operators = ["+", "-", "*", "/"]
unary_operators = ["exp", "log", "sqrt", "sin", "cos", "tan", "asin", "acos", "atan", "sinh", "cosh", "tanh", "asinh", "acosh", "atanh"]

# generate random binary trees

class Node_Binary:
    operator = True
    binary = True
    operand = False
    def __init__(self, data, left=None, right=None):
        self.data = data
        self.left = left
        self.right = right
        
class Node_Unary:
    operator = True
    binary = False
    operand = False
    def __init__(self, data, middle=None):
        self.data = data
        self.middle = middle 
        
class Leaf:
    operator = False
    binary = False
    operand = True
    def __init__(self, data):
        self.data = data

def random_binary_trees(n):
    population, weights = distribution_k_a(1, n)
    k, a = choices(population, weights)[0]
    if a == 1:
        operator = choices(unary_operators)[0]
        node = Node_Unary(operator)
        empty_node = [(node, 'middle')]
        e = 1
    else:
        operator = choices(binary_operators)[0]
        node = Node_Binary(operator)
        empty_node = [(node, 'left'), (node, 'right')]
        e = 2
    n = n - 1
    while n > 0:
        population, weights = distribution_k_a(e, n)
        k, a = choices(population, weights)[0]
        i = 0
        new_empty_node = []
        for ele in empty_node:
            if i < k:
                leave = choices(leaves, p_leaf)[0]
                value = Leaf(leave)
                setattr(ele[0], ele[1], value)
            elif i == k:
                if a == 1:
                    operator = choices(unary_operators)[0]
                    value = Node_Unary(operator)
                    setattr(ele[0], ele[1], value)
                    if ele[1] == 'left':
                        new_ele = ele[0].left
                    elif ele[1] == 'middle':
                        new_ele = ele[0].middle
                    else:
                        new_ele = ele[0].right
                    new_empty_node = [(new_ele, 'middle')]
                    e = e - k
                else:
                    operator = choices(binary_operators)[0]
                    value = Node_Binary(operator)
                    setattr(ele[0], ele[1], value)
                    if ele[1] == 'left':
                        new_ele = ele[0].left
                    elif ele[1] == 'middle':
                        new_ele = ele[0].middle
                    else:
                        new_ele = ele[0].right
                    new_empty_node = [(new_ele, 'left'), (new_ele, 'right')]
                    e = e - k + 1
            else:
                new_empty_node.append(ele)
            i += 1
        empty_node = new_empty_node
        n = n - 1
    if len(empty_node) != 0:
        for ele in empty_node:
            leave = choices(leaves, p_leaf)[0]
            value = Leaf(leave)
            setattr(ele[0], ele[1], value)
            
    return node

def traverse_unary_binary_prefix(root, seq=None, verbose=False):
    if not seq:
        seq = []
        
    if verbose:
        print(root.data)
        
    seq.append(root.data)
    
    if root.binary:
        if root.left.operator:
            traverse_unary_binary_prefix(root.left, seq)
        else:
            if verbose:
                print(root.left.data)
            seq.append(root.left.data)
        
        if root.right.operator:
            traverse_unary_binary_prefix(root.right, seq)
        else:
            if verbose:
                print(root.right.data)
            seq.append(root.right.data)
    else:
        if root.middle.operator:
            traverse_unary_binary_prefix(root.middle, seq)
        else:
            if verbose:
                print(root.middle.data)
            seq.append(root.middle.data)
    
    return seq
        
if __name__ == '__main__':
    
    root = random_binary_trees(1)
    print(traverse_unary_binary_prefix(root))  







