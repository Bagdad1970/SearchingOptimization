import sympy

def function_from_str(function: str):
    x, y = sympy.symbols('x y')
    expression = sympy.sympify(function)
    return sympy.lambdify((x, y), expression)