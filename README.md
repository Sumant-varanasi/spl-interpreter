# SPL Interpreter

> **SPL** — *Special Programming Language* — a simple expression-based interpreter written in Python, built as part of ACOL226 Assignment 1.

---

## What is SPL?

SPL is a minimal programming language where **everything is an expression** — there are no statements. Every expression evaluates to a `float` value and can optionally have side effects (like assigning a variable).

SPL uses **prefix notation** (also called Polish notation): the operator always comes *before* its operands. This eliminates operator precedence ambiguity entirely.

> Example: instead of `x + y * z`, you write `+ x * y z`

---

## Getting Started

### Requirements

- Python 3.x (no external dependencies)

### Run the interpreter

```bash
python3 spl.py
```

You'll see the `spl>` prompt. Type an expression and press Enter to evaluate it.

```
spl> + 3 4
7.0
spl> * 2 + 1 3
8.0
spl> exit
0.0
bye!
```

---

## Language Reference

All expressions use **prefix notation** and return a `float`.

### Literals & Constants

| Syntax | Returns |
|--------|---------|
| `3.14`, `42`, `-1.5` | the numeric value |
| `pi` | π (3.14159...) |

### Binary Operations

| Syntax | Returns |
|--------|---------|
| `+ e1 e2` | e1 + e2 |
| `- e1 e2` | e1 − e2 |
| `* e1 e2` | e1 × e2 |
| `/ e1 e2` | e1 ÷ e2 |
| `^ e1 e2` | e1 ^ e2 (power) |

### Math Functions

| Syntax | Returns |
|--------|---------|
| `sin e1` | sin(e1) |
| `cos e1` | cos(e1) |
| `exp e1` | e^e1 |
| `log e1` | ln(e1) |
| `sqrt e1` | √e1 |

### Variables

SPL has three built-in variables: `a`, `b`, `c` (all initialised to `0.0`).

| Syntax | Side Effect | Returns |
|--------|------------|---------|
| `a` | — | current value of a |
| `b` | — | current value of b |
| `c` | — | current value of c |
| `a= e1` | assigns e1 to a | e1 |
| `b= e1` | assigns e1 to b | e1 |
| `c= e1` | assigns e1 to c | e1 |

```
spl> a= 5
5.0
spl> + a 3
8.0
```

### Logical Operators

| Syntax | Returns |
|--------|---------|
| `== e1 e2` | 1.0 if e1 = e2, else 0.0 |
| `< e1 e2` | 1.0 if e1 < e2, else 0.0 |

### If-Then-Else

```
if <condition> <then-expr> <else-expr>
```

- If `condition ≠ 0`, evaluates and returns `then-expr` (skips `else-expr`)
- If `condition = 0`, evaluates and returns `else-expr` (skips `then-expr`)
- The skipped branch is **never evaluated** — side effects are avoided.

```
spl> if < a 10 a= + a 1 a= - a 1
1.0
```

### User-Defined Functions

SPL supports two user-definable single-argument functions: `f` and `g`. The argument is bound to `x` inside the function body.

| Syntax | Side Effect | Returns |
|--------|------------|---------|
| `f= e1` | stores expression text as f | 0.0 |
| `g= e1` | stores expression text as g | 0.0 |
| `f e1` | evaluates f with x = e1 | f(e1) |
| `g e1` | evaluates g with x = e1 | g(e1) |

**Factorial example:**
```
spl> f= if == x 0 1 * x f - x 1
0.0
spl> f 5
120.0
```

Functions support **recursion** — `f` can call `f`, and `g` can call `g` (or `f`).

### Block Expressions

Group multiple expressions together with `{ ... }`. All expressions are evaluated, but only the **last value** is returned.

```
{ e1 e2 ... en }
```

```
spl> { a= 3 b= 4 + a b }
7.0
```

### Exit

```
spl> exit
0.0
bye!
```

---

## Examples

### Fibonacci-style / Prime Checker

```
spl> g= if == x 1 0 if == * / x 2 2 x 0 g - x 2
spl> f= if == x 1 1 if g x 0 * x f - x 2
```

### Chained assignments

```
spl> a= b= c= 7
7.0
spl> + a + b c
21.0
```

---

## Project Structure

```
spl-interpreter/
└── spl.py        # The complete interpreter
```

### How it works

The interpreter uses a **recursive token-consumer** design:

1. **Tokenize** — split input line on whitespace into a token list
2. **Evaluate** — `evaluate(tokens)` pops the first token, dispatches on its type, and recursively evaluates sub-expressions as needed
3. **Skip** — `skip_expression(tokens)` traverses but discards a sub-expression (used by if-then-else to avoid unwanted side effects)
4. **Collect** — `collect_expression(tokens)` captures tokens for a function body without evaluating them (lazy storage)

---

## License

This project was created as part of a university assignment (ACOL226). Feel free to use it for learning purposes.
