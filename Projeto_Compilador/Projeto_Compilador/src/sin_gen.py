import sys
import re


def sanitize(token):
    """
    Remove non-alphanumeric characters from token and return lower-case.
    """
    # Remove quotes and punctuation
    token = re.sub(r"[^\w]", "", token)
    return token.lower()


def parse_grammar(grammar_text):
    """
    Parses the grammar text into a list of productions.
    Each production is a tuple (lhs, alternative).
    """
    productions = []
    current_lhs = None
    for line in grammar_text.splitlines():
        line = line.strip()
        if not line:
            continue
        # Check if line defines a new production or is an alternative
        if ':' in line:
            parts = line.split(":", 1)
            current_lhs = parts[0].strip()
            alternative = parts[1].strip()
            productions.append((current_lhs, alternative))
        elif line.startswith('|'):
            alternative = line[1:].strip()
            productions.append((current_lhs, alternative))
    return productions


def generate_function_name(lhs, alternative):
    """
    Generate a function name by concatenating:
      - The left-hand side of the production
      - The first token from the alternative.
    """
    # Split the alternative into tokens
    tokens = alternative.split()
    if tokens:
        first_token = tokens[0]
    else:
        first_token = ""
    # Sanitize tokens to be valid as part of a Python function name
    lhs_part = sanitize(lhs)
    token_part = sanitize(first_token)
    return f"p_{lhs_part}_{token_part}"


def generate_functions(grammar_text):
    """
    Generates Python function definitions (as strings) for each production.
    """
    productions = parse_grammar(grammar_text)
    output_lines = []
    for lhs, alt in productions:
        func_name = generate_function_name(lhs, alt)
        output_lines.append(f"def {func_name}(p):")
        output_lines.append('    """')
        output_lines.append(f"    {lhs} : {alt}")
        output_lines.append('    """')
        output_lines.append("")  # blank line for separation
    return "\n".join(output_lines)


def main():
    # Read grammar text from standard input
    grammar_text = sys.stdin.read()
    output = generate_functions(grammar_text)
    print(output)


if __name__ == "__main__":
    main()
