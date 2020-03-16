import random
import time

from sympy import Symbol, diff, simplify

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
        from sympy import S; S.Half #https://github.com/sympy/sympy/issues/18438
        d['expr'] = parse_expr(string, local_dict={'x': x}, evaluate=False)

    with Manager() as manager:
        d = manager.dict()
        p = Process(target=f, args=(d, string))
        p.start()
        p.join(timeout=3)
        if p.is_alive():
            p.terminate()
        else:
            try:
                expr = d["expr"]
            except KeyError:
                return None

    if expr==None or str(type(expr))=="<class 'sympy.calculus.util.AccumulationBounds'>":
        return None
    else:
        return expr


def generate_single_sequence():
    n = random.randint(1, 15)
    root = random_binary_trees(n)
    result = traverse_unary_binary_prefix(root)
    if 'x' not in result:
        return None

    result_infix = prefix_to_infix(result)
    result_expr = " ".join(result_infix)

    #  convert to sympy expression
    result_expr = parse_expr_timeout(result_expr)
    if result_expr is None:
        return None

    #  simplification
    result_simp = simplify_timeout(result_expr)
    if result_simp == "Error":
        return None

    #  back to prefix
    result_simp_prefix = infix_to_prefix(result_simp)
    if not result_simp_prefix:
        return None

    #  generate target
    try:
        expr_diff = diff(result_simp)
    except ValueError:
        return None

    expression = simplify_timeout(expr_diff)
    if expression == "Error":
        return None

    expression_prefix = infix_to_prefix(expression)
    if not expression_prefix:
        return None

    expression_prefix = " ".join(expression_prefix)
    result_simp_prefix = " ".join(result_simp_prefix)
    return expression_prefix, result_simp_prefix


def generate_bwd(num):

    while True:
        if _FINISH:
            break
        sequence = []
        start = time.time()

        i = 1
        while i<=num:
            seq = generate_single_sequence()
            if seq is not None:
                expression_prefix, result_simp_prefix = seq
                sequence.append(expression_prefix + "\t" + result_simp_prefix + "\n")
            else:
                continue
            i += 1

        end = time.time()
        #print(end - start)
        print('process finished')
        return sequence
