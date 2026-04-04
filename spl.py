import math

# Global state
variables = {'a': 0.0, 'b': 0.0, 'c': 0.0}
functions = {'f': None, 'g': None}
x_param = 0.0  # the parameter x for function calls
exit_flag = False

def tokenize(line):
    """Split the input line into tokens (whitespace-delimited)."""
    return line.strip().split()

def evaluate(tokens):
    """
    Evaluate the next expression from the token list.
    Consumes tokens from the front as it goes.
    Returns a float value.
    """
    global variables, functions, x_param, exit_flag

    if not tokens:
        print("unrecognized expression: (empty)")
        return float('nan')

    token = tokens.pop(0)

    # --- Literals (numbers) ---
    try:
        return float(token)
    except ValueError:
        pass  # not a number, continue checking

    # --- Constants ---
    if token == 'pi':
        return math.pi

    # --- Exit ---
    if token == 'exit':
        exit_flag = True
        return 0.0

    # --- Binary operations ---
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

    # --- Unary math functions ---
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

    # --- Logical operators ---
    if token == '==':
        e1 = evaluate(tokens)
        e2 = evaluate(tokens)
        return 1.0 if e1 == e2 else 0.0

    if token == '<':
        e1 = evaluate(tokens)
        e2 = evaluate(tokens)
        return 1.0 if e1 < e2 else 0.0

    # --- If-then-else ---
    if token == 'if':
        condition = evaluate(tokens)
        if condition != 0.0:
            result = evaluate(tokens)
            skip_expression(tokens)
            return result
        else:
            skip_expression(tokens)
            result = evaluate(tokens)
            return result

    # --- Reading variables ---
    if token == 'a':
        return variables['a']

    if token == 'b':
        return variables['b']

    if token == 'c':
        return variables['c']

    # --- Writing variables ---
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

    # --- Accessing parameter x ---
    if token == 'x':
        return x_param

    # --- Writing functions (store text, don't evaluate) ---
    if token == 'f=':
        func_tokens = collect_expression(tokens)
        functions['f'] = func_tokens
        return 0.0

    if token == 'g=':
        func_tokens = collect_expression(tokens)
        functions['g'] = func_tokens
        return 0.0

    # --- Calling functions ---
    if token == 'f':
        e1 = evaluate(tokens)
        return call_function('f', e1)

    if token == 'g':
        e1 = evaluate(tokens)
        return call_function('g', e1)

    # --- Block expression ---
    if token == '{':
        result = 0.0
        while tokens and tokens[0] != '}':
            result = evaluate(tokens)
        if tokens and tokens[0] == '}':
            tokens.pop(0)
        return result

    # --- Unrecognized ---
    print(f"unrecognized expression: {token}")
    return float('nan')


def skip_expression(tokens):
    """
    Skip over one complete expression in the token list without evaluating it.
    """
    if not tokens:
        return

    token = tokens.pop(0)

    try:
        float(token)
        return
    except ValueError:
        pass

    if token in ('pi', 'exit', 'a', 'b', 'c', 'x'):
        return

    if token in ('+', '-', '*', '/', '^', '==', '<'):
        skip_expression(tokens)
        skip_expression(tokens)
        return

    if token in ('sin', 'cos', 'exp', 'log', 'sqrt'):
        skip_expression(tokens)
        return

    if token in ('a=', 'b=', 'c='):
        skip_expression(tokens)
        return

    if token == 'if':
        skip_expression(tokens)
        skip_expression(tokens)
        skip_expression(tokens)
        return

    if token in ('f=', 'g='):
        skip_expression(tokens)
        return

    if token in ('f', 'g'):
        skip_expression(tokens)
        return

    if token == '{':
        while tokens and tokens[0] != '}':
            skip_expression(tokens)
        if tokens and tokens[0] == '}':
            tokens.pop(0)
        return

    return


def collect_expression(tokens):
    """
    Collect tokens forming one complete expression (without evaluating).
    Returns them as a list of token strings.
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
    """Call a stored function with the given argument."""
    global x_param

    if functions[name] is None:
        print(f"unrecognized expression: {name}")
        return float('nan')

    old_x = x_param
    x_param = arg

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
