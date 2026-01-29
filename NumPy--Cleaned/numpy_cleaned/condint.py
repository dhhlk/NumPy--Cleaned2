from decimal import Decimal
from fractions import Fraction
from typing import Callable, Optional

def condint(x, *, to_type: Optional[str] = None, cond: Optional[Callable] = None):
    """
    Conditionally converts between int and float for game-safe operations.

    Parameters:
    x       : int, float, Decimal, or Fraction.
    to_type : 'int' -> force int if allowed
              'float' -> force float if allowed
              None -> default auto-conversion
    cond    : callablle taking x, return True to convert, False to leave as is.

    Behavior:
    - If to_type='int': converts x to int if possible and cond(x) allows
    - If to_type='float': converts x to float if cond(x) allows
    - If to_type=None: 
        - float with integer value -> int
        - int -> int (or can be float internally if needed)
    """
    if cond is None:
        cond = lambda v: True  # Default: always allow conversion

    # Determine if x is an exact integer
    is_exact_int = (
        isinstance(x, int) or
        (isinstance(x, float) and x.is_integer()) or
        (isinstance(x, Decimal) and x == x.to_integral_value()) or
        (isinstance(x, Fraction) and x.denominator == 1)
    )

    # Force int
    if to_type == 'int' and cond(x) and is_exact_int:
        if isinstance(x, Fraction):
            return x.numerator
        return int(x)

    # Force float
    if to_type == 'float' and cond(x):
        return float(x)

    # Auto conversion: exact floats → int
    if to_type is None and cond(x) and is_exact_int and isinstance(x, float):
        return int(x)

    # Otherwise, return as-is
    return x


def condint_list(lst, *, to_type: Optional[str] = None, cond: Optional[Callable] = None):
    """
    Apply condint to a list of values
    """
    return [condint(x, to_type=to_type, cond=cond) for x in lst]
