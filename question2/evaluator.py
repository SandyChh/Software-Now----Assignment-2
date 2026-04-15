# ---------------- TOKENIZER ---------------- #

# Function to convert input string into a list of tokens (NUM, OP, LPAREN, RPAREN, END)
# This is lexical analysis: it only reads characters, NOT meaning
def tokenize(expression):

    tokens = []  # store tokens found in the expression
    i = 0  # pointer to scan input string

    # scan each character in expression
    while i < len(expression):

        char = expression[i]

        # skip spaces (they are irrelevant for parsing)
        if char.isspace():
            i += 1
            continue

        # ---------------- NUMBER HANDLING ---------------- #
        # detect numbers (including decimals)
        elif char.isdigit() or char == ".":

            num = char  # start building number string
            i += 1

            # count decimal points to avoid invalid numbers like 1.2.3
            dot_count = 1 if char == "." else 0

            # keep reading digits / dots
            while i < len(expression) and (expression[i].isdigit() or expression[i] == "."):

                # invalid number format check
                if expression[i] == ".":
                    dot_count += 1
                    if dot_count > 1: # More than 1 dot is an invalid number
                        return "ERROR"  # invalid number format

                num += expression[i]
                i += 1

            # store number token after validation
            try:
                float(num)  # validate number
            except ValueError:
                return "ERROR"
            tokens.append(("NUM", num))
            continue

        # ----------------HANDLE OPERATORS +, -, *, / ---------------- #
        elif char in "+-*/":
            tokens.append(("OP", char))  # store operator token

        # ---------------- LEFT PARENTHESIS ---------------- #
        elif char == "(":
            tokens.append(("LPAREN", char))

        # ---------------- RIGHT PARENTHESIS ---------------- #
        elif char == ")":
            tokens.append(("RPAREN", char))

        # ---------------- INVALID CHARACTER ---------------- #
        else:
            return "ERROR"  # invalid input symbol

        i += 1  # move to next character

    # mark end of input stream (important for parser termination)
    tokens.append(("END", ""))

    return tokens


# ---------------- PARSER FUNCTIONS (GRAMMAR ENGINE) ---------------- #

# Expression parser: Handles + and - (lowest precedence level)
def parse_expression(tokens, pos):

    # first parse the left-hand side (higher precedence: * /) terms
    left, pos = parse_term(tokens, pos)

    # keep processing Loop while next token is + and - operators (can chain multiple additions/subtractions)
    while tokens[pos][0] == "OP" and tokens[pos][1] in "+-":

        op = tokens[pos][1]  # operator
        pos += 1  # move forward

        right, pos = parse_term(tokens, pos)  # parse right-hand term

        # build syntax tree node
        left = (op, left, right)

    return left, pos

# Term parser: Handles * and / (and implicit multiplication )
def parse_term(tokens, pos):

    # parse left-hand factor first
    left, pos = parse_factor(tokens, pos)

    while True:

        token = tokens[pos]

        # ---------------- NORMAL MULTIPLICATION/DIVISION ---------------- #
        if token[0] == "OP" and token[1] in "*/":

            op = token[1]
            pos += 1

            right, pos = parse_factor(tokens, pos)

            left = (op, left, right) # Build binary tree node

        # ---------------- IMPLICIT MULTIPLICATION ---------------- #
        # e.g. 2(3), (2)(3), 2 3 (adjacent expressions)
        elif token[0] in ("NUM", "LPAREN"):

            right, pos = parse_factor(tokens, pos)

            left = ("*", left, right) # Treat as multiplication

        else:
            break  # stop when no valid multiplication pattern

    return left, pos


# Factor parser: Handles numbers, parentheses, unary minus
def parse_factor(tokens, pos):

    token = tokens[pos]

    # ---------------- UNARY NEGATION (MINUS) ---------------- #
    # converts -x into (neg x)
    if token[0] == "OP" and token[1] == "-":

        pos += 1
        operand, pos = parse_factor(tokens, pos)

        return ("neg", operand), pos # Return unary negation node

    # ---------------- NUMBER ---------------- #
    elif token[0] == "NUM":

        pos += 1

        # Return float if decimal, else int
        return float(token[1]) if "." in token[1] else int(token[1]), pos

    # ---------------- PARENTHESES ---------------- #
    elif token[0] == "LPAREN":

        pos += 1  # skip "("

        expr, pos = parse_expression(tokens, pos) # Parse inside parentheses

        # ensure closing parenthesis exists
        if tokens[pos][0] != "RPAREN":
            raise Exception("Missing )")

        pos += 1  # skip ")"

        return expr, pos

    # ---------------- INVALID SYNTAX ---------------- #
    else:
        raise Exception("Invalid syntax")

def evaluate(tree):

    # if value is a number, return directly
    if isinstance(tree, (int, float)):
        return tree

    # unary negation case
    if tree[0] == "neg":
        return -evaluate(tree[1])

    op, left, right = tree # Binary operation

    # perform arithmetic operations
    if op == "+":
        return evaluate(left) + evaluate(right)

    elif op == "-":
        return evaluate(left) - evaluate(right)

    elif op == "*":
        return evaluate(left) * evaluate(right)

    elif op == "/":

        divisor = evaluate(right)

        # runtime error check (Division by zero check)
        if divisor == 0:
            raise ZeroDivisionError

        return evaluate(left) / divisor


# ---------------- TREE TO STRING (DISPLAY FORMAT) ---------------- #

def tree_to_string(tree):

    # number formatting
    if isinstance(tree, (int, float)):
        return str(tree)

    # unary format
    if tree[0] == "neg":
        return f"(neg {tree_to_string(tree[1])})"

    # binary operation format
    op, left, right = tree
    return f"({op} {tree_to_string(left)} {tree_to_string(right)})"


# ---------------- TOKEN DISPLAY FORMAT ---------------- #

def tokens_to_string(tokens):

    if tokens == "ERROR":
        return "ERROR"

    result = []

    # convert each token to string format
    for t in tokens:

        if t[0] == "END":
            result.append("[END]")  # Mark end token
        else:
            result.append(f"[{t[0]}:{t[1]}]")

    return " ".join(result)

# ---------------- MAIN DRIVER FUNCTION ---------------- #

def evaluate_file(input_path: str) -> list[dict]:
    
    # Reads expressions from a file, evaluates them, writes output.txt,
    # and returns a list of dictionaries with keys: input, tree, tokens, result.
    results: list[dict] = []       # store return results
    output_lines: list[str] = []   # store file output
# def evaluate_file(input_path: str):

#     results = []  # store return results
#     output_lines = []  # store file output

    # read input file
    with open(input_path, "r") as file:
        lines = file.readlines()

    # process each expression line
    for line in lines:

        expr = line.strip()

        if not expr:
            continue  # skip empty lines

        try:
            # STEP 1: TOKENIZE
            tokens = tokenize(expr)

            if tokens == "ERROR":
                raise Exception()

            tokens_str = tokens_to_string(tokens)

            # STEP 2: PARSE (build tree)
            try:
                tree, pos = parse_expression(tokens, 0)

                # ensure full expression consumed (check for leftover tokens)
                if tokens[pos][0] != "END":
                    raise Exception("Extra tokens")

                # STEP 3: convert to display format
                tree_str = tree_to_string(tree)

                # STEP 4: evaluate expression
                try:
                    value = evaluate(tree)

                    # formatting rule: remove .0 if integer
                    if isinstance(value, float) and value.is_integer():
                        value = int(value)
                    else:
                        value = round(value, 4)

                except:
                    value = "ERROR"
            except:
                tree_str = "ERROR"
                value = "ERROR"

        except:
            tree_str = "ERROR"
            tokens_str = "ERROR"
            value = "ERROR"

        # store result in return structure
        results.append({
            "input": expr,
            "tree": tree_str,
            "tokens": tokens_str,
            "result": value
        })

        # write formatted output block
        output_lines.append(f"Input: {expr}")
        output_lines.append(f"Tree: {tree_str}")
        output_lines.append(f"Tokens: {tokens_str}")
        output_lines.append(f"Result: {value}")
        output_lines.append("")

    # write output file
    with open("output.txt", "w") as file:
        file.write("\n".join(output_lines))
    
    print(" SUCCESS: Output written to output.txt successfully!")

    return results


def main():
    try:
        evaluate_file("input.txt")
    except Exception as e:
        print(f'Error occurred: {e}')

if __name__ == "__main__":
    main()