"""
NumPy_Revised
A lightweight, Decimal-safe math + array toolkit
for restricted environments (schools, macros, no NumPy).
"""

# Core math
from .maths_cleaned import *

# Arrays
from .arrays import Array1, Array2, Array3

# Conditional int/float conversion
from .condint import condint, condint_list

# Stability decorator
from .stabilze import stabilize

__all__ = [
    # Arrays
    "Array1", "Array2", "Array3",

    # Conversion
    "condint", "condint_list",

    # Stability
    "stabilize",
]
