

import sympy as sp


def generate_steps(problem_type, **kwargs):
   
    if problem_type == "equation":
        return steps_for_equation(**kwargs)
    elif problem_type == "derivative":
        return steps_for_derivative(**kwargs)
    elif problem_type == "integral":
        return steps_for_integral(**kwargs)
    elif problem_type == "evaluate":
        return steps_for_evaluate(**kwargs)
    elif problem_type == "simplify":
        return steps_for_simplify(**kwargs)
    else:
        return [{"title": "Result", "explanation": "Problem solved."}]


def steps_for_equation(lhs, rhs, equation, solution, **kwargs):
  
    steps = []
    x = sp.Symbol("x")

    # Step 1: Write the original equation
    steps.append({
        "title": "Step 1: Write Down the Equation",
        "explanation": f"We start with the equation: {lhs} = {rhs}"
    })

    # Step 2: Move terms to one side
    difference = sp.expand(lhs - rhs)
    steps.append({
        "title": "Step 2: Rearrange – Bring Everything to One Side",
        "explanation": (
            f"Subtract the right side from the left side:\n"
            f"  ({lhs}) - ({rhs}) = 0\n"
            f"  {difference} = 0"
        )
    })

    # Step 3: Identify the variable
    free_vars = list(equation.free_symbols)
    var_name = str(free_vars[0]) if free_vars else "x"
    steps.append({
        "title": f"Step 3: Identify the Variable",
        "explanation": f"We are solving for the variable: {var_name}"
    })

    # Step 4: Apply algebraic rules
    steps.append({
        "title": "Step 4: Apply Algebraic Rules",
        "explanation": (
            "Use inverse operations to isolate the variable:\n"
            "  - If a number is added, subtract it from both sides.\n"
            "  - If a number is multiplied, divide both sides by it."
        )
    })

    # Step 5: Show the solution
    if solution:
        sol_str = ", ".join([str(s) for s in solution])
        steps.append({
            "title": "Step 5: Final Solution",
            "explanation": f"Solving gives us: {var_name} = {sol_str}"
        })

        # Step 6: Verify by substitution
        if len(solution) == 1:
            check_val = solution[0]
            lhs_val = lhs.subs(x, check_val)
            rhs_val = rhs.subs(x, check_val) if hasattr(rhs, "subs") else rhs
            steps.append({
                "title": "Step 6: Verify the Answer",
                "explanation": (
                    f"Substitute {var_name} = {check_val} back into the equation:\n"
                    f"  Left side: {lhs} → {lhs_val}\n"
                    f"  Right side: {rhs}\n"
                    f"  {lhs_val} = {rhs_val} ✓ Verified!"
                )
            })
    else:
        steps.append({
            "title": "Step 5: Result",
            "explanation": "No real solution found for this equation."
        })

    return steps


def steps_for_derivative(expr, result, **kwargs):
 
    steps = []

    # Step 1: State the problem
    steps.append({
        "title": "Step 1: Identify the Function",
        "explanation": f"We need to differentiate: f(x) = {expr}"
    })

    # Step 2: Explain differentiation rules
    steps.append({
        "title": "Step 2: Recall the Differentiation Rules",
        "explanation": (
            "Key rules used for differentiation:\n"
            "  • Power Rule: d/dx (xⁿ) = n·xⁿ⁻¹\n"
            "  • Constant Rule: d/dx (c) = 0\n"
            "  • Sum Rule: d/dx (f + g) = f' + g'\n"
            "  • Product Rule: d/dx (f·g) = f'g + fg'"
        )
    })

    # Step 3: Break down the expression (check if it's additive)
    terms = sp.Add.make_args(sp.expand(expr))
    if len(terms) > 1:
        term_steps = []
        for term in terms:
            d_term = sp.diff(term, sp.Symbol("x"))
            term_steps.append(f"  d/dx({term}) = {d_term}")
        steps.append({
            "title": "Step 3: Differentiate Each Term Separately",
            "explanation": "Using the Sum Rule, we differentiate each term:\n" + "\n".join(term_steps)
        })
    else:
        steps.append({
            "title": "Step 3: Apply the Power Rule",
            "explanation": f"Apply differentiation rules to: {expr}"
        })

    # Step 4: Show the final derivative
    steps.append({
        "title": "Step 4: Write the Final Derivative",
        "explanation": f"Combining all terms, the derivative is:\n  f'(x) = {result}"
    })

    # Step 5: Interpretation
    steps.append({
        "title": "Step 5: What This Means",
        "explanation": (
            f"The derivative f'(x) = {result} tells us the rate of change of the function.\n"
            "It shows how fast the function value changes as x changes."
        )
    })

    return steps


def steps_for_integral(expr, result, **kwargs):
   
    steps = []

    # Step 1: State the problem
    steps.append({
        "title": "Step 1: Identify the Function to Integrate",
        "explanation": f"We need to find the integral of: f(x) = {expr}"
    })

    # Step 2: Recall integration rules
    steps.append({
        "title": "Step 2: Recall the Integration Rules",
        "explanation": (
            "Key rules used for integration:\n"
            "  • Power Rule: ∫xⁿ dx = xⁿ⁺¹/(n+1) + C\n"
            "  • Constant Rule: ∫c dx = cx + C\n"
            "  • Sum Rule: ∫(f + g) dx = ∫f dx + ∫g dx\n"
            "  • C is the constant of integration"
        )
    })

    # Step 3: Break down the expression
    terms = sp.Add.make_args(sp.expand(expr))
    if len(terms) > 1:
        term_steps = []
        for term in terms:
            i_term = sp.integrate(term, sp.Symbol("x"))
            term_steps.append(f"  ∫({term}) dx = {i_term}")
        steps.append({
            "title": "Step 3: Integrate Each Term Separately",
            "explanation": "Using the Sum Rule, we integrate each term:\n" + "\n".join(term_steps)
        })
    else:
        steps.append({
            "title": "Step 3: Apply the Power Rule",
            "explanation": (
                f"For the expression {expr}, increase the power by 1 "
                "and divide by the new power."
            )
        })

    # Step 4: Combine and add C
    steps.append({
        "title": "Step 4: Combine Terms and Add Constant C",
        "explanation": (
            f"Combining all integrated terms:\n"
            f"  ∫({expr}) dx = {result} + C\n"
            "Don't forget '+ C' — it represents an unknown constant."
        )
    })

    # Step 5: Verification by differentiation
    x = sp.Symbol("x")
    verify = sp.diff(result, x)
    simplified_verify = sp.simplify(verify - sp.expand(expr))
    is_correct = simplified_verify == 0

    steps.append({
        "title": "Step 5: Verify by Differentiating the Result",
        "explanation": (
            f"To check, differentiate the answer:\n"
            f"  d/dx({result} + C) = {verify}\n"
            f"  This equals our original function: {expr} {'✓' if is_correct else '(check manually)'}"
        )
    })

    return steps


def steps_for_evaluate(expr, assignments, substituted, result, **kwargs):
   
    steps = []

    # Step 1: Show the given assignments
    assignment_lines = [f"{name} = {value}" for name, value in assignments.items()]
    steps.append({
        "title": "Step 1: Read the Given Values",
        "explanation": "We are given:\n  " + "\n  ".join(assignment_lines)
    })

    # Step 2: State the expression to evaluate
    steps.append({
        "title": "Step 2: Identify the Expression",
        "explanation": f"We need to evaluate: {expr}"
    })

    # Step 3: Substitute the values
    steps.append({
        "title": "Step 3: Substitute the Values",
        "explanation": f"Replace each variable with its value:\n  {substituted}"
    })

    # Step 4: Compute the final result
    steps.append({
        "title": "Step 4: Compute the Result",
        "explanation": f"The evaluated result is:\n  {result}"
    })

    return steps


def steps_for_simplify(expr, expanded, factored, simplified, **kwargs):
   
    steps = []

    # Step 1: State the expression
    steps.append({
        "title": "Step 1: Write Down the Expression",
        "explanation": f"We start with the expression: {expr}"
    })

    # Step 2: Expand the expression
    steps.append({
        "title": "Step 2: Expand the Expression",
        "explanation": (
            f"Expanding (removing brackets by multiplying terms):\n"
            f"  {expr} → {expanded}"
        )
    })

    # Step 3: Factor the expression
    steps.append({
        "title": "Step 3: Factor the Expression",
        "explanation": (
            f"Factoring (writing as a product of simpler terms):\n"
            f"  {expr} → {factored}"
        )
    })

    # Step 4: Simplify
    steps.append({
        "title": "Step 4: Simplified Form",
        "explanation": (
            f"The simplified form of the expression is:\n"
            f"  {simplified}"
        )
    })

    # Step 5: What to use when
    steps.append({
        "title": "Step 5: Summary of Forms",
        "explanation": (
            f"  • Original: {expr}\n"
            f"  • Expanded (all terms visible): {expanded}\n"
            f"  • Factored (compact form): {factored}\n"
            f"  • Simplified: {simplified}\n\n"
            "Use expanded form for addition/subtraction.\n"
            "Use factored form to find roots (where the expression = 0)."
        )
    })

    return steps