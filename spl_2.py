import math

# We'll store everything globally – much easier for a small interpreter.
# a, b, c are the only variables; f, g are user-defined functions.
variables = {'a': 0.0, 'b': 0.0, 'c': 0.0}
functions = {'f': None, 'g': None}
x_param = 0.0  # the parameter x (used when calling f or g)
exit_flag = False

def tokenize(line):
    """split the input line into tokens by whitespace"""
    return line.strip().split()

def evaluate(tokens):
    """
    Reads one complete expression from the token list and returns its value.
    Consumes the tokens it uses.
    """
    global variables, functions, x_param, exit_flag

    if not tokens:
        print("unrecognized expression: (empty)")
        return float('nan')

    token = tokens.pop(0)

    # --- try to read a number literal first ---
    try:
        return float(token)
    except ValueError:
        pass  # wasn't a number, keep checking

    # --- a few special constants and built‑ins ---
    if token == 'pi':
        return math.pi

    if token == 'exit':
        exit_flag = True
        return 0.0

    # --- arithmetic operators ---
    if token == '+':
        e1 = evaluate(tokens)
        e2 = evaluate(tokens)
        return e1 + e2

    if token == '-':
        e1 = evaluate(tokens)
        e2 = evaluate(tokens)
        return e1 - e2

    if token == '*':
        e1 = evaluate(tokens)
        e2 = evaluate(tokens)
        return e1 * e2

    if token == '/':
        e1 = evaluate(tokens)
        e2 = evaluate(tokens)
        return e1 / e2

    if token == '^':
        e1 = evaluate(tokens)
        e2 = evaluate(tokens)
        return e1 ** e2

    # --- unary math stuff (trig, exp, log) ---
    if token == 'sin':
        e1 = evaluate(tokens)
        return math.sin(e1)

    if token == 'cos':
        e1 = evaluate(tokens)
        return math.cos(e1)

    if token == 'exp':
        e1 = evaluate(tokens)
        return math.exp(e1)

    if token == 'log':
        e1 = evaluate(tokens)
        return math.log(e1)

    if token == 'sqrt':
        e1 = evaluate(tokens)
        return math.sqrt(e1)

    # --- comparisons (return 1.0 or 0.0) ---
    if token == '==':
        e1 = evaluate(tokens)
        e2 = evaluate(tokens)
        return 1.0 if e1 == e2 else 0.0

    if token == '<':
        e1 = evaluate(tokens)
        e2 = evaluate(tokens)
        return 1.0 if e1 < e2 else 0.0

    # --- if‑then‑else: if cond true_expr false_expr ---
    if token == 'if':
        condition = evaluate(tokens)
        if condition != 0.0:
            result = evaluate(tokens)
            skip_expression(tokens)   # throw away the false branch
            return result
        else:
            skip_expression(tokens)   # throw away the true branch
            result = evaluate(tokens)
            return result

    # --- reading variables a, b, c ---
    if token == 'a':
        return variables['a']

    if token == 'b':
        return variables['b']

    if token == 'c':
        return variables['c']

    # --- assignments: a=, b=, c= (they return the assigned value) ---
    if token == 'a=':
        e1 = evaluate(tokens)
        variables['a'] = e1
        return e1

    if token == 'b=':
        e1 = evaluate(tokens)
        variables['b'] = e1
        return e1

    if token == 'c=':
        e1 = evaluate(tokens)
        variables['c'] = e1
        return e1

    # --- accessing the parameter x inside a function ---
    if token == 'x':
        return x_param

    # --- function definitions: f= and g= store the body as a token list ---
    if token == 'f=':
        func_tokens = collect_expression(tokens)
        functions['f'] = func_tokens
        return 0.0

    if token == 'g=':
        func_tokens = collect_expression(tokens)
        functions['g'] = func_tokens
        return 0.0

    # --- function calls: f arg, g arg ---
    if token == 'f':
        e1 = evaluate(tokens)
        return call_function('f', e1)

    if token == 'g':
        e1 = evaluate(tokens)
        return call_function('g', e1)

    # --- block expression: { expr1 expr2 ... } returns last value ---
    if token == '{':
        result = 0.0
        while tokens and tokens[0] != '}':
            result = evaluate(tokens)
        if tokens and tokens[0] == '}':
            tokens.pop(0)
        return result

    # --- anything we don't recognise ---
    print(f"unrecognized expression: {token}")
    return float('nan')


def skip_expression(tokens):
    """
    Skip one complete expression silently, without evaluating it.
    Used by if to discard the branch that won't be taken.
    """
    if not tokens:
        return

    token = tokens.pop(0)

    # a number literal
    try:
        float(token)
        return
    except ValueError:
        pass

    if token in ('pi', 'exit', 'a', 'b', 'c', 'x'):
        return

    # binary ops
    if token in ('+', '-', '*', '/', '^', '==', '<'):
        skip_expression(tokens)
        skip_expression(tokens)
        return

    # unary ops
    if token in ('sin', 'cos', 'exp', 'log', 'sqrt'):
        skip_expression(tokens)
        return

    # assignments
    if token in ('a=', 'b=', 'c='):
        skip_expression(tokens)
        return

    # if
    if token == 'if':
        skip_expression(tokens)
        skip_expression(tokens)
        skip_expression(tokens)
        return

    # function definitions
    if token in ('f=', 'g='):
        skip_expression(tokens)
        return

    # function calls
    if token in ('f', 'g'):
        skip_expression(tokens)
        return

    # block
    if token == '{':
        while tokens and tokens[0] != '}':
            skip_expression(tokens)
        if tokens and tokens[0] == '}':
            tokens.pop(0)
        return

    # unknown tokens are just ignored silently
    return


def collect_expression(tokens):
    """
    Gather all tokens that make up one complete expression.
    Needed to save the body of f= or g= without evaluating it.
    """
    if not tokens:
        return []

    token = tokens.pop(0)
    collected = [token]

    try:
        float(token)
        return collected
    except ValueError:
        pass

    if token in ('pi', 'exit', 'a', 'b', 'c', 'x'):
        return collected

    if token in ('+', '-', '*', '/', '^', '==', '<'):
        collected += collect_expression(tokens)
        collected += collect_expression(tokens)
        return collected

    if token in ('sin', 'cos', 'exp', 'log', 'sqrt'):
        collected += collect_expression(tokens)
        return collected

    if token in ('a=', 'b=', 'c='):
        collected += collect_expression(tokens)
        return collected

    if token == 'if':
        collected += collect_expression(tokens)
        collected += collect_expression(tokens)
        collected += collect_expression(tokens)
        return collected

    if token in ('f=', 'g='):
        collected += collect_expression(tokens)
        return collected

    if token in ('f', 'g'):
        collected += collect_expression(tokens)
        return collected

    if token == '{':
        while tokens and tokens[0] != '}':
            collected += collect_expression(tokens)
        if tokens and tokens[0] == '}':
            collected.append(tokens.pop(0))
        return collected

    return collected


def call_function(name, arg):
    """Call a stored function f or g with the given argument."""
    global x_param

    if functions[name] is None:
        print(f"unrecognized expression: {name}")
        return float('nan')

    old_x = x_param
    x_param = arg

    # work on a copy of the token list so recursion works properly
    func_tokens = list(functions[name])
    result = evaluate(func_tokens)

    x_param = old_x

    return result


def main():
    global exit_flag

    while True:
        try:
            line = input("spl> ")
        except EOFError:
            break

        if not line.strip():
            continue

        tokens = tokenize(line)
        result = evaluate(tokens)

        if math.isnan(result):
            print("NaN")
        else:
            print(result)

        if exit_flag:
            print("bye!")
            break


if __name__ == '__main__':
    main()
