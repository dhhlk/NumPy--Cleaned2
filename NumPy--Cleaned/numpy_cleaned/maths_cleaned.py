from decimal import Decimal, getcontext
from fractions import Fraction
from .stabilze import stabilize
from .condint import condint

# ───────────── Configuration & Constants ─────────────
getcontext().prec = 50

PI = Decimal("3.1415926535897932384626433832795028841971")
E  = Decimal("2.7182818284590452353602874713527")
ZERO = Decimal("0")
ONE  = Decimal("1")


# ───────────── Helpers ─────────────
def _to_decimal(x):
    """Convert int | float | Decimal | Fraction -> Decimal safely."""
    if isinstance(x, Decimal):
        return x
    elif isinstance(x, Fraction):
        return Decimal(x.numerator) / Decimal(x.denominator)
    else:  # int or float
        return Decimal(x)


def dec_div(a, b):
    """Safe division with Decimal conversion and zero check."""
    a = _to_decimal(a)
    b = _to_decimal(b)
    assert isinstance(a, Decimal) and isinstance(b, Decimal)
    if b == 0:
        raise ValueError("Cannot divide by zero. Please change.")
    return a / b


# ───────────── Basic Number Functions ─────────────
@stabilize
def fact(n, *, to_type=None, cond=None):
    n = int(n)
    if n < 0:
        raise ValueError("Factorial not defined for negatives")
    result = 1
    for i in range(1, n + 1):
        result *= i
    return condint(result, to_type=to_type, cond=cond)


@stabilize
def fibonacci(n, *, to_type=None, cond=None):
    n = int(n)
    a, b = ZERO, ONE
    series = []
    for _ in range(n):
        series.append(a)
        a, b = b, a + b
    return [condint(_to_decimal(x), to_type=to_type, cond=cond) for x in series]


@stabilize
def digital_root(n):
    n = abs(int(n))
    while n >= 10:
        n = sum(int(d) for d in str(n))
    return n


@stabilize
def is_harshad(n):
    n = int(n)
    return n % sum(int(d) for d in str(n)) == 0


@stabilize
def triangular(n, *, to_type=None, cond=None):
    n = _to_decimal(n)
    return condint(dec_div(n*(n+1), 2), to_type=to_type, cond=cond)


@stabilize
def collatz_steps(n):
    n = int(n)
    steps = 0
    while n != 1:
        n = n // 2 if n % 2 == 0 else 3 * n + 1
        steps += 1
    return steps


# ───────────── Roots & Powers ─────────────
@stabilize
def sqrt(x, *, to_type=None, cond=None):
    x = _to_decimal(x)
    if x < 0:
        raise ValueError("Cannot take square root of negative")
    guess = x / 2
    for _ in range(30):
        guess = (guess + dec_div(x, guess)) / 2
    return condint(guess, to_type=to_type, cond=cond)


@stabilize
def cbrt(x, *, to_type=None, cond=None):
    x = _to_decimal(x)
    guess = x / 3
    for _ in range(30):
        guess = (2*guess + dec_div(x, guess*guess)) / 3
    return condint(guess, to_type=to_type, cond=cond)


@stabilize
def power(base, exp, *, to_type=None, cond=None):
    base = _to_decimal(base)
    exp = int(exp)
    result = ONE
    for _ in range(abs(exp)):
        result *= base
    if exp < 0:
        result = dec_div(ONE, result)
    return condint(result, to_type=to_type, cond=cond)


# ───────────── Logarithms ─────────────
@stabilize
def ln(x, *, to_type=None, cond=None):
    x = _to_decimal(x)
    if x <= 0:
        raise ValueError("ln undefined for non-positive numbers")
    y = dec_div(x - ONE, x + ONE)
    term = y
    result = ZERO
    n = 1
    while abs(term) > Decimal("1e-40"):
        result += dec_div(term, n)
        term *= y * y
        n += 2
    return condint(2*result, to_type=to_type, cond=cond)


@stabilize
def log(x, base=10, *, to_type=None, cond=None):
    x = _to_decimal(x)
    base = _to_decimal(base)
    return condint(dec_div(ln(x, to_type=to_type, cond=cond),
                           ln(base, to_type=to_type, cond=cond)),
                   to_type=to_type, cond=cond)


# ───────────── Trigonometry ─────────────
@stabilize
def sin(x, *, to_type=None, cond=None):
    x = _to_decimal(x)
    term = x
    result = x
    n = 1
    while abs(term) > Decimal("1e-40"):
        term *= -x*x / ((2*n)*(2*n+1))
        result += term
        n += 1
    return condint(result, to_type=to_type, cond=cond)


@stabilize
def cos(x, *, to_type=None, cond=None):
    x = _to_decimal(x)
    term = ONE
    result = ONE
    n = 1
    while abs(term) > Decimal("1e-40"):
        term *= -x*x / ((2*n-1)*(2*n))
        result += term
        n += 1
    return condint(result, to_type=to_type, cond=cond)


@stabilize
def tan(x, *, to_type=None, cond=None):
    return condint(dec_div(sin(x, to_type=to_type, cond=cond),
                           cos(x, to_type=to_type, cond=cond)),
                   to_type=to_type, cond=cond)


# ───────────── Geometry ─────────────
@stabilize
def circumference(radius, *, to_type=None, cond=None):
    r = _to_decimal(radius)
    return condint(2*PI*r, to_type=to_type, cond=cond)


@stabilize
def area_circle(radius, *, to_type=None, cond=None):
    r = _to_decimal(radius)
    return condint(PI*r*r, to_type=to_type, cond=cond)


@stabilize
def area_square(side, *, to_type=None, cond=None):
    s = _to_decimal(side)
    return condint(s*s, to_type=to_type, cond=cond)


@stabilize
def area_rectangle(length, breadth, *, to_type=None, cond=None):
    l = _to_decimal(length)
    b = _to_decimal(breadth)
    return condint(l*b, to_type=to_type, cond=cond)


@stabilize
def area_triangle(base, height, *, to_type=None, cond=None):
    return condint(dec_div(_to_decimal(base)*_to_decimal(height), 2),
                   to_type=to_type, cond=cond)


@stabilize
def perimeter_square(side, *, to_type=None, cond=None):
    s = _to_decimal(side)
    return condint(4*s, to_type=to_type, cond=cond)


@stabilize
def perimeter_rectangle(length, breadth, *, to_type=None, cond=None):
    l = _to_decimal(length)
    b = _to_decimal(breadth)
    return condint(2*(l+b), to_type=to_type, cond=cond)


@stabilize
def distance_2d(x1, y1, x2, y2, *, to_type=None, cond=None):
    dx = _to_decimal(x2) - _to_decimal(x1)
    dy = _to_decimal(y2) - _to_decimal(y1)
    return condint(sqrt(dx*dx + dy*dy, to_type=to_type, cond=cond),
                   to_type=to_type, cond=cond)


@stabilize
def cube_volume(side, *, to_type=None, cond=None):
    s = _to_decimal(side)
    return condint(s**3, to_type=to_type, cond=cond)


@stabilize
def cube_surface_area(side, *, to_type=None, cond=None):
    s = _to_decimal(side)
    return condint(6*s*s, to_type=to_type, cond=cond)


@stabilize
def pythagoras(a, b, *, to_type=None, cond=None):
    a = _to_decimal(a)
    b = _to_decimal(b)
    return condint(sqrt(a*a + b*b, to_type=to_type, cond=cond),
                   to_type=to_type, cond=cond)


# ───────────── Finance & Percentages ─────────────
@stabilize
def percentage(part, total, *, to_type=None, cond=None):
    return condint(dec_div(_to_decimal(part)*100, total), to_type=to_type, cond=cond)


@stabilize
def simple_interest(principal, rate, time, *, to_type=None, cond=None):
    p = _to_decimal(principal)
    r = _to_decimal(rate)
    t = _to_decimal(time)
    return condint(dec_div(p*r*t, 100), to_type=to_type, cond=cond)


@stabilize
def compound_interest(principal, rate, time, *, to_type=None, cond=None):
    p = _to_decimal(principal)
    r = _to_decimal(rate)/100
    t = _to_decimal(time)
    return condint(p*((ONE+r)**t)-p, to_type=to_type, cond=cond)
