
import sympy as sp
from steps_generator import generate_steps


def parse_expression(expr_str):
   
    expr_str = expr_str.replace("^", "**")
    x, y, z, t = sp.symbols("x y z t")
    local_dict = {"x": x, "y": y, "z": z, "t": t}
    expr = sp.sympify(expr_str, locals=local_dict)
    return expr


def detect_problem_type(expr_str):
    
    expr_lower = expr_str.lower().strip()
    if expr_lower.startswith("diff(") or expr_lower.startswith("derivative("):
        return "derivative"
    if expr_lower.startswith("integrate(") or expr_lower.startswith("integral("):
        return "integral"
    if "=" in expr_str:
        return "equation"
    return "simplify"


import re


def add_implicit_multiplication(expr_str):
    expr_str = expr_str.replace("^", "**")
    expr_str = re.sub(r"(\d)([a-zA-Z])", r"\1*\2", expr_str)
    expr_str = re.sub(r"([a-zA-Z])(\d)", r"\1*\2", expr_str)
    return expr_str


def solve_equation(expr_str):
    x = sp.Symbol("x")
    parts = expr_str.split("=")
    if len(parts) != 2:
        return {"error": "Invalid equation format. Use format like: 2x + 3 = 11"}
    lhs_str = add_implicit_multiplication(parts[0].strip())
    rhs_str = add_implicit_multiplication(parts[1].strip())
    lhs = sp.sympify(lhs_str, locals={"x": x})
    rhs = sp.sympify(rhs_str, locals={"x": x})
    equation = sp.Eq(lhs, rhs)
    solution = sp.solve(equation, x)
    steps = generate_steps(
        "equation", lhs=lhs, rhs=rhs, equation=equation, solution=solution
    )
    return {
        "type": "equation",
        "expression": str(equation),
        "answer": str(solution),
        "steps": steps,
        "sympy_answer": solution,
    }


def solve_derivative(expr_str):
    x = sp.Symbol("x")
    inner = ""
    for keyword in ["diff(", "derivative("]:
        if expr_str.lower().startswith(keyword):
            inner = expr_str[len(keyword) :].rstrip(")")
            break
    if not inner:
        return {"error": "Could not parse derivative. Use format: diff(x^2)"}
    inner = add_implicit_multiplication(inner)
    expr = sp.sympify(inner, locals={"x": x})
    derivative = sp.diff(expr, x)
    simplified = sp.simplify(derivative)
    steps = generate_steps("derivative", expr=expr, result=simplified)
    return {
        "type": "derivative",
        "expression": str(expr),
        "answer": str(simplified),
        "steps": steps,
        "sympy_answer": simplified,
    }


def solve_integral(expr_str):
    x = sp.Symbol("x")
    inner = ""
    for keyword in ["integrate(", "integral("]:
        if expr_str.lower().startswith(keyword):
            inner = expr_str[len(keyword) :].rstrip(")")
            break
    if not inner:
        return {"error": "Could not parse integral. Use format: integrate(x^3)"}
    inner = add_implicit_multiplication(inner)
    expr = sp.sympify(inner, locals={"x": x})
    integral_result = sp.integrate(expr, x)
    result_str = str(integral_result) + " + C"
    steps = generate_steps("integral", expr=expr, result=integral_result)
    return {
        "type": "integral",
        "expression": str(expr),
        "answer": result_str,
        "steps": steps,
        "sympy_answer": integral_result,
    }


def solve_simplify(expr_str):
    x = sp.Symbol("x")
    expr_str = add_implicit_multiplication(expr_str)
    expr = sp.sympify(expr_str, locals={"x": x})
    expanded = sp.expand(expr)
    factored = sp.factor(expr)
    simplified = sp.simplify(expr)
    steps = generate_steps(
        "simplify",
        expr=expr,
        expanded=expanded,
        factored=factored,
        simplified=simplified,
    )
    return {
        "type": "simplify",
        "expression": str(expr),
        "answer": str(simplified),
        "steps": steps,
        "expanded": str(expanded),
        "factored": str(factored),
        "sympy_answer": simplified,
    }


def solve_math_problem(expr_str):
    try:
        problem_type = detect_problem_type(expr_str)
        if problem_type == "equation":
            return solve_equation(expr_str)
        elif problem_type == "derivative":
            return solve_derivative(expr_str)
        elif problem_type == "integral":
            return solve_integral(expr_str)
        else:
            return solve_simplify(expr_str)
    except Exception as e:
        return {
            "type": "error",
            "expression": expr_str,
            "answer": "Could not solve",
            "error": f"Error: {str(e)}. Please check your input format.",
            "steps": [],
        }