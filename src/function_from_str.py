import sympy

def function_from_str(function: str):
    x, y = sympy.symbols('x1 x2')
    expression = sympy.sympify(function)
    return sympy.lambdify((x, y), expression)