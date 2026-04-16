


# readable labels for each problem type
TYPE_LABELS = {
    "equation": "Algebraic Equation",
    "derivative": "Derivative",
    "integral": "Indefinite Integral",
    "simplify": "Expression Simplification",
    "evaluate": "Expression Evaluation",
    "error": "Error",
}

# Emoji icons for each problem type (makes output friendlier)
TYPE_ICONS = {
    "equation": "⚖️",
    "derivative": "📈",
    "integral": "∫",
    "evaluate": "📊",
    "simplify": "🔢",
    "error": "⚠️",
}

# Short descriptions explaining each type to beginners
TYPE_DESCRIPTIONS = {
    "equation": (
        "An algebraic equation contains an '=' sign and we solve it by "
        "finding the value of the unknown variable (like x) that makes both sides equal."
    ),
    "derivative": (
        "A derivative measures how fast a function changes at any point. "
        "It is the foundation of calculus and used in physics, economics, and engineering."
    ),
    "integral": (
        "An integral is the reverse of a derivative. It finds the area under a curve "
        "or accumulates quantities. We add '+ C' because many functions share the same derivative."
    ),
    "simplify": (
        "Simplification rewrites an expression in its most compact or useful form. "
        "We can expand (open brackets), factor (group terms), or reduce the expression."
    ),
    "evaluate": (
        "Evaluation substitutes given variable values into an expression and computes the result. "
        "This is useful for questions like 'if a=9, b=6, what is 2a+6b'."
    ),
    "error": (
        "Something went wrong while solving the problem. "
        "Please check your input format and try again."
    ),
}


def format_result(result_data, original_input, source):
    """
    Takes raw solver output and formats it into a dictionary
    ready for rendering in the result.html template.

    Parameters:
        result_data  (dict): Output from solver.py
        original_input (str): The original expression the user typed or the OCR output
        source       (str): 'text' or 'image' — how the input was received

    Returns:
        dict: Formatted data for the template
    """
    problem_type = result_data.get("type", "error")

    # Get a friendly label and icon for this type
    label = TYPE_LABELS.get(problem_type, "Unknown")
    icon = TYPE_ICONS.get(problem_type, "❓")
    description = TYPE_DESCRIPTIONS.get(problem_type, "")

    # Clean the answer for display
    raw_answer = result_data.get("answer", "No answer")
    display_answer = clean_answer(raw_answer, problem_type)

    # Source label: how did the problem arrive?
    source_label = "📷 Extracted from Image" if source == "image" else "⌨️ Typed by User"

    # Get steps list (each step has 'title' and 'explanation')
    steps = result_data.get("steps", [])

    # Extra info for simplification problems
    extra_info = {}
    if problem_type == "simplify":
        extra_info = {
            "expanded": result_data.get("expanded", ""),
            "factored": result_data.get("factored", ""),
        }

    # Check if there was an error
    error_message = result_data.get("error", None)

    # Put everything together in one dictionary
    formatted = {
        "original_input": original_input,
        "source_label": source_label,
        "problem_type": problem_type,
        "type_label": label,
        "type_icon": icon,
        "type_description": description,
        "expression": result_data.get("expression", original_input),
        "answer": display_answer,
        "steps": steps,
        "extra_info": extra_info,
        "error_message": error_message,
        "has_steps": len(steps) > 0,
    }

    return formatted


def clean_answer(answer_str, problem_type):
    """
    Clean and format the raw answer string for better readability.
    """
    if not answer_str:
        return "No answer"

    answer_str = str(answer_str)

    # For equations, format list answers like [3] → x = 3
    if problem_type == "equation":
        # Remove square brackets from list representation
        answer_str = answer_str.strip("[]")
        if "," in answer_str:
            # Multiple solutions
            solutions = [s.strip() for s in answer_str.split(",")]
            answer_str = " or ".join([f"x = {s}" for s in solutions])
        else:
            answer_str = f"x = {answer_str.strip()}"

    # Replace ** with ^ for display (more readable)
    answer_str = answer_str.replace("**", "^")

    # Replace * with · for cleaner display
    answer_str = answer_str.replace("*", "·")

    return answer_str


def format_expression_for_display(expr_str):
    
    if not expr_str:
        return ""

    expr_str = str(expr_str)
    expr_str = expr_str.replace("**", "^")
    expr_str = expr_str.replace("*", "·")

    return expr_str