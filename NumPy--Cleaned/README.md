#NumPy--Cleaned

A lightweight, Decimal-safe math and array library for environments where NumPy is not practical
(schools, restricted systems, macros, low-permission computers).

This is not a NumPy replacement.
It is a safe, understandable alternative for basic numeric work.

Why NumPy--Cleaned?

NumPy is powerful, but:

❌ Often unavailable on school computers

❌ Hard to install on restricted systems

❌ Overkill for simple math and arrays

❌ Uses floating-point math by default

NumPy--revised focuses on:

✅ Pure Python (no C extensions)

✅ Decimal-based precision

✅ Predictable behavior

✅ Game & education friendliness

✅ Clear, readable source code

What’s inside?
📐 Maths (maths_cleaned.py)

Factorials, Fibonacci, roots, powers

Trigonometry (series-based)

Geometry helpers

Finance & statistics

Number theory

Game-friendly math (clamp, smoothstep, logistic)

All calculations are Decimal-safe.

🔢 Arrays (arrays.py)

A small, NumPy-like system:

Array1, Array2, Array3

Element-wise operations

Scalar and array math

Works without NumPy

Designed for clarity, not magic

Example:

from NumPy--revised import Array1

a = Array1([1, 2, 3])
b = Array1([4, 5, 6])

result = a.add(b)
print(result.to_list())  # [5, 7, 9]

🔁 Conditional int/float conversion (condint.py)

Some systems require integers only, but calculations need floats.

condint solves this safely.

from NumPy--revised import condint

condint(3.0)      # → 3
condint(3.7)      # → 3.7
condint(3.0, to_type="float")  # → 3.0


Useful for:

Games

Grid systems

School engines

Macro environments

🛡 Stability layer (stabilize.py)

A friendly decorator for reliability:

@stabilize
def divide(a, b):
    return a / b


Instead of scary errors, you get:

Cannot divide by zero. Please change.

Installation

Currently designed for local use:

git clone: (https://github.com/dhhlk/NumPy--Cleaned/)


Then:

from NumPy--revised import Array1, condint


(Pip support may come later.)

Design philosophy

Simple > clever

Readable > fast hacks

Safe > silent failures

Understandable > opaque optimizations

This library is meant to be read, learned from, and trusted.

License

MIT License
You are free to use, modify, and distribute this project.

Disclaimer

This project does not aim to compete with NumPy.
If you can use NumPy, you probably should.

If you can’t, this exists for you.
