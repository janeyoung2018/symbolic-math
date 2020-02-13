#!/usr/bin/env python

from __future__ import division
import random

'''
Q: Infix,  and prefix expression conversion
For example: 
Infix: 1 * (2 + 3) / 4
Postfix: 1 2 3 + * 4 /
Prefix: / * 1 + 2 3 4
'''

'''
Fix a priority level for each operator. For example, from high to low:
    3.    - (unary negation)
    2.    * /
    1.    + - (subtraction)
'''

OPERATORS = set(['+', '-', '*', '/', '(', ')'])
UNARY_OPERATORS = set(["exp", "log", "sqrt", "sin", 
                 "cos", "tan", "arcsin", "arccos", "arctan", "sinh", "cosh", "tanh", "sinh", "cosh", "tanh"])
PRIORITY = {'+':1, '-':1, '*':2, '/':2, "exp":3, "log":3, "sqrt":3, "sin":3, 
                 "cos":3, "tan":3, "arcsin":3, "arccos":3, "arctan":3, "sinh":3, "cosh":3, "tanh":3, "sinh":3, "cosh":3, "tanh":3}





### INFIX ===> PREFIX ###
def infix_to_prefix(formula):
    op_stack = []
    exp_stack = []
    exp_list = []
    for ch in formula:
        if ch not in OPERATORS and ch not in UNARY_OPERATORS:
            exp_stack.append(ch)
        elif ch in UNARY_OPERATORS:
            op_stack.append(ch)
        elif ch == '(':
            op_stack.append(ch)
        elif ch == ')':
            while op_stack[-1] != '(':
                generate_expression(op_stack, exp_stack) 
            op_stack.pop() # pop '('
        else:
            while op_stack and op_stack[-1] != '(' and PRIORITY[ch] <= PRIORITY[op_stack[-1]]:
                generate_expression(op_stack, exp_stack)
            op_stack.append(ch)
    
    # leftover
    while op_stack:
        generate_expression(op_stack, exp_stack)
    print(exp_stack[-1])
    print(exp_stack[-1].split())
    return exp_stack[-1], exp_stack[-1].split()

def generate_expression(op_stack, exp_stack):
    op = op_stack.pop()
    if op in OPERATORS:
        a = exp_stack.pop()
        b = exp_stack.pop()
        expression = op + " " + b + " " + a
        exp_stack.append(expression)
    else:
        a = exp_stack.pop()
        expression = op + " " + a
        exp_stack.append(expression)

### PREFIX ===> INFIX ###
'''
Scan the formula reversely
1) When the token is an operand, push into stack
2) When the token is an operator, pop out 2 numbers from stack, merge them and push back to the stack
'''
def prefix_to_infix(formula):
    stack = []
    prev_op = None
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
                    exp = a + " " + ch+ " " + b
            else:
                a = stack.pop()
                exp = ch + " " + "(" + " " +  a + " " +")"
            stack.append(exp)
            prev_op = ch
    print(stack[-1])
    print(stack[-1].split())
    return stack[-1], stack[-1].split()





if __name__ == '__main__':
    infix_to_prefix(['cosh', '(', '(', '4', '-', 'sinh', '(', '(', '-4', '/', '-2', ')', ')', ')', ')'])
    prefix_to_infix(['cosh', '-', '4', 'sinh', '/', '-4', '-2'])