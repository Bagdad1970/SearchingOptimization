import sympy

def function_from_str(function: str):
    expression = sympy.sympify(function)
    func_symbols = sort_symbols_by_ord(expression.free_symbols)
    return sympy.lambdify(func_symbols, expression)

def sort_symbols_by_ord(symbols: set):
    str_symbols = sorted(map(str, symbols), key=lambda s: sum(ord(c) for c in s))
    return sympy.symbols(' '.join(str_symbols))
