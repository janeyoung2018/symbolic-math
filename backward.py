import random
import time

from sympy import Symbol

from infix_prefix import prefix_to_infix, infix_to_prefix
from random_trees import random_binary_trees, traverse_unary_binary_prefix


_FINISH = False
x = Symbol('x', real=True) # TODO


def simplify_timeout(expr):
    from multiprocessing import Process, Manager
    
    result = None
    def f(d, expr):
        try:
            d['result'] = simplify(expr)
        except:
            d['result'] = "Error"

    with Manager() as manager:
        d = manager.dict()
        p = Process(target=f, args=(d, expr))
        p.start()
        p.join(timeout=3)
        if p.is_alive():
            p.terminate()
        else:    
            result = d["result"]
    if result==None:
        return expr
    else:
        return result


def parse_expr_timeout(string):
    from multiprocessing import Process, Manager
    from sympy.parsing.sympy_parser import parse_expr

    expr = None
    def f(d, string):
        d['expr'] = parse_expr(string, local_dict={'x': x})
        
    with Manager() as manager:
        d = manager.dict()
        p = Process(target=f, args=(d, string))
        p.start()
        p.join(timeout=3)
        if p.is_alive():
            p.terminate()
        else:    
            expr = d["expr"]
    if expr==None or str(type(expr))=="<class 'sympy.calculus.util.AccumulationBounds'>":
        return None
    else:
        return expr


def generate_bwd(num):
    
    while True:
        if _FINISH:
            break
        sequence = []
        start = time.time()

        i = 1
        while i<=num:
            n = random.randint(1, 15)
            root = random_binary_trees(n)
            result = traverse_unary_binary_prefix(root)
            if 'x' not in result:
                continue
            result_infix = prefix_to_infix(result) 
            result_expr = " ".join(result_infix)
            
            #  convert to sympy expression
            result_expr = parse_expr_timeout(result_expr)
            if result_expr==None:
                continue
                
            #  simplification
            result_simp = simplify_timeout(result_expr)
            if result_simp == "Error":
                continue
                
            #  back to prefix
            result_simp_prefix = infix_to_prefix(result_simp)
            if result_simp_prefix == False:
                continue
                
            #  generate target
            try:
                expr_diff = diff(result_simp)
            except ValueError:
                continue
            expression = simplify_timeout(expr_diff)
            expression_prefix = infix_to_prefix(expression)
            if expression_prefix == False:
                continue  
            expression_prefix = " ".join(expression_prefix)
            result_simp_prefix = " ".join(result_simp_prefix)
            sequence.append(expression_prefix + "\t" + result_simp_prefix + "\n")
            i += 1

        end = time.time()
        print(end - start)
        return sequence
