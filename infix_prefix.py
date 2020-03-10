import random

from sympy import *



OPERATORS = set(['+', '-', '*', '/', '(', ')', 'pow'])

UNARY_OPERATORS = set(["exp", "log", "sqrt", "sin", "cos", "tan", "asin", "acos", "atan", "sinh", "cosh", "tanh", "asinh", "acosh", "atanh"])

operator_class = ["<class 'sympy.core.add.Add'>", "<class 'sympy.core.mul.Mul'>", "<class 'sympy.core.power.Pow'>", "exp", "log", "sin", "cos", "tan", "asin", "acos", "atan", "sinh", "cosh", "tanh", "asinh", "acosh", "atanh", "Abs"]

operator_dict = {"<class 'sympy.core.add.Add'>": "+", "<class 'sympy.core.mul.Mul'>": "*", "<class 'sympy.core.power.Pow'>": "pow", "exp": "exp", "log": "log", "sin": "sin", "cos": "cos", "tan": "tan", "asin": "asin", "acos": "acos", "atan": "atan", "sinh": "sinh", "cosh": "cosh", "tanh": "tanh", "asinh": "asinh", "acosh": "acosh", "atanh": "atanh", "Abs": "abs"}

rational_number = ["<class 'sympy.core.numbers.Rational'>", "<class 'sympy.core.numbers.Half'>"]

exp1_number = ["<class 'sympy.core.numbers.Exp1'>"]

invalid_function = ["<class 'sympy.core.numbers.ImaginaryUnit'>", "<class 'sympy.core.numbers.ComplexInfinity'>", "<class 'sympy.core.numbers.NegativeInfinity'>", "<class 'sympy.core.numbers.Infinity'>", "<class 'sympy.core.numbers.NaN'>"]

invalid_expression = ["zoo", "oo", "I", "-oo"]

#x = symbols('x')
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

    for i in range(length):
        if i!=0 and i!=(length-1):
            seq.append(op)
        arg = expr.args[i]
        feedback = infix_to_prefix(arg, seq)
        if feedback==False:
            return False
    return seq

### PREFIX ===> INFIX ###
'''
Scan the formula reversely
1) When the token is an operand, push into stack
2) When the token is an operator, pop out 2 numbers from stack, merge them and push back to the stack
'''
def prefix_to_infix(formula):
    stack = []
    for ch in reversed(formula):
        if ch not in OPERATORS and ch not in UNARY_OPERATORS:
            stack.append(ch)
        else:
            if ch in OPERATORS:
                a = stack.pop()
                b = stack.pop()
                exp = "(" + " " + a + " " + ch + " " + b + " " + ")"  
            else:
                a = stack.pop()
                exp = ch + " " + "(" + " " +  a + " " +")"
            stack.append(exp)
    return stack[-1].split()


if __name__ == '__main__':
    pre = infix_to_prefix(simplify(sympify("log(exp(x))")))
    inf = prefix_to_infix(['cosh', '-', '4', 'sinh', '/', '-4', '-2'])
