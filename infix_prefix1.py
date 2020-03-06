#!/usr/bin/env python

from __future__ import division
import random
from sympy import *

'''
Fix a priority level for each operator. For example, from high to low:
    3.    - (unary negation)
    2.    * /
    1.    + - (subtraction)
'''

OPERATORS = set(['+', '-', '*', '/', '(', ')', 'pow'])
UNARY_OPERATORS = set(["exp", "log", "sqrt", "sin", 
                 "cos", "tan", "asin", "acos", "atan", "sinh", "cosh", "tanh", "asinh", "acosh", "atanh"])
PRIORITY = {'+':1, '-':1, '*':2, '/':2, 'pow':2, "exp":3, "log":3, "sqrt":3, "sin":3, 
                 "cos":3, "tan":3, "asin":3, "acos":3, "atan":3, "sinh":3, "cosh":3, "tanh":3, "asinh":3, "acosh":3, "atanh":3}

operator_class = ["<class 'sympy.core.add.Add'>", "<class 'sympy.core.mul.Mul'>", "<class 'sympy.core.power.Pow'>", "exp", "log",
                 "sin", "cos", "tan", "asin", "acos", "atan", "sinh", "cosh", "tanh", "asinh", "acosh", "atanh", "Abs"]

operator_dict = {"<class 'sympy.core.add.Add'>": "+", "<class 'sympy.core.mul.Mul'>": "*", "<class 'sympy.core.power.Pow'>": "pow",
                 "exp": "exp", "log": "log", "sin": "sin", "cos": "cos", "tan": "tan", "asin": "asin", "acos": "acos", 
                 "atan": "atan", "sinh": "sinh", "cosh": "cosh", "tanh": "tanh", "asinh": "asinh", "acosh": "acosh", "atanh": "atanh", "Abs": "abs"}
rational_number = ["<class 'sympy.core.numbers.Rational'>", "<class 'sympy.core.numbers.Half'>"]
exp1_number = ["<class 'sympy.core.numbers.Exp1'>"]
invalid_function = ["<class 'sympy.core.numbers.ImaginaryUnit'>", "<class 'sympy.core.numbers.ComplexInfinity'>", 
                    "<class 'sympy.core.numbers.NegativeInfinity'>", "<class 'sympy.core.numbers.Infinity'>",
                   "<class 'sympy.core.numbers.NaN'>"]
invalid_expression = ["zoo", "oo", "I", "-oo"]



### INFIX ===> PREFIX ###
x = symbols('x')
def infix_to_prefix(expr, seq=None):
    if not seq:
        seq = []
    s1 = str(expr)
    s2 = str(expr.func)
    if s1 in invalid_expression or s2 in invalid_function:
        return False
    length = len(expr.args)
    if s2 in operator_class:
        op = operator_dict[s2]
        seq.append(op)
    elif s2 in rational_number:
        s1 = s1.split("/")
        seq.append("/")
        seq.append(s1[0])
        seq.append(s1[1])
    elif s2 in exp1_number:
        seq.append("exp")
        seq.append("1")
    else:
        seq.append(s1)
            
    i = 0
    while i < length:
        if i!=0 and i!=(length-1):
            seq.append(op)
        arg = expr.args[i]
        infix_to_prefix(arg, seq)
        i += 1
    return " ".join(seq)   
        
### PREFIX ===> INFIX ###
'''
Scan the formula reversely
1) When the token is an operand, push into stack
2) When the token is an operator, pop out 2 numbers from stack, merge them and push back to the stack
'''
def prefix_to_infix(formula):
    stack = []
    prev_op = None
    formula = formula.split()
    for ch in reversed(formula):
        if ch not in OPERATORS and ch not in UNARY_OPERATORS:
            stack.append(ch)
        else:
            if ch in OPERATORS:
                a = stack.pop()
                b = stack.pop()
                if prev_op and PRIORITY[prev_op] < PRIORITY[ch]:
                    exp = '(' + " " + a + " " + ')' + " " + ch + " "+ b
                else:
                    exp = a + " " + ch + " " + b
            else:
                a = stack.pop()
                exp = ch + " " + "(" + " " +  a + " " +")"
            stack.append(exp)
            prev_op = ch
    #print(stack[-1])
    #print(stack[-1].split())
    return stack[-1]





if __name__ == '__main__':
    print(infix_to_prefix(simplify(sympify("log(exp(x))"))))
    print("\n")
    print(prefix_to_infix("cosh - 4 sinh / -4 -2"))