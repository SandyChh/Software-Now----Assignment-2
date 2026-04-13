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

def evaluate_file(input_path: str) -> list[dict]:
    # read input file
    with open(input_path, "r") as file:
        lines = file.readlines()

    tokens = []
    output_lines = []  # store lines that will be written to output.txt
    
    # process each expression line
    for line in lines:

        expr = line.strip()

        if not expr:
            continue  # skip empty lines

        try:
            # STEP 1: TOKENIZE
            token = tokenize(expr)
            if token == "ERROR":
                raise Exception()
            tokens.append(token)
        except Exception:
          # instead of printing error to console, store it for file output
            output_lines.append(expr)  
    output_lines.append(str(tokens))

    # write all collected output lines into output.txt
    with open("output.txt", "w") as f:
        f.write("\n".join(output_lines))    
    return []  # placeholder for results


def main():
    evaluate_file("input.txt")
    print(" SUCCESS: Output written to output.txt successfully!")

if __name__ == "__main__":
    main()