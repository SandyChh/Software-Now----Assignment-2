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

def evaluate_file(input_path: str) -> list[dict]:
    # read input file
    with open(input_path, "r") as file:
        lines = file.readlines()

    tokens = []

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
            print(expr)  # tokenization failed
    print(tokens)
    return []  # placeholder for results (not implemented)

def main():
    evaluate_file("input.txt")

if __name__ == "__main__":
    main()