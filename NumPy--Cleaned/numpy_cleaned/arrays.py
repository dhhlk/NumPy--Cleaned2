from decimal import Decimal, getcontext
from .stabilze import stabilize
from .condint import condint, condint_list
from .maths_cleaned import _to_decimal, dec_div

# ───────────── Array Base Class ─────────────
getcontext().prec = 1000  # High precision for calculations
class BaseArray:
    def __init__(self, data, *, to_type=None, cond=None):
        # convert all input to Decimal safely
        self.data = [_to_decimal(x) for x in data]
        self.to_type = to_type
        self.cond = cond

    def __repr__(self):
        return f"{self.__class__.__name__}({[condint(x, to_type=self.to_type, cond=self.cond) for x in self.data]})"

    def __len__(self):
        return len(self.data)

    def __getitem__(self, idx):
        return condint(self.data[idx], to_type=self.to_type, cond=self.cond)

    def __setitem__(self, idx, value):
        self.data[idx] = _to_decimal(value)

    def to_list(self):
        return [condint(x, to_type=self.to_type, cond=self.cond) for x in self.data]

# ───────────── Element-wise Operations ─────────────
    def _elementwise(self, other, op):
        if isinstance(other, BaseArray):
            if len(self.data) != len(other.data):
                raise ValueError("Array lengths must match")
            return [op(a, b) for a, b in zip(self.data, other.data)]
        else:  # scalar
            o = _to_decimal(other)
            return [op(a, o) for a in self.data]

# ───────────── Arithmetic ─────────────
    @stabilize
    def add(self, other):
        return condint_list(self._elementwise(other, lambda a, b: a+b),
                            to_type=self.to_type, cond=self.cond)

    @stabilize
    def sub(self, other):
        return condint_list(self._elementwise(other, lambda a, b: a-b),
                            to_type=self.to_type, cond=self.cond)

    @stabilize
    def mul(self, other):
        return condint_list(self._elementwise(other, lambda a, b: a*b),
                            to_type=self.to_type, cond=self.cond)

    @stabilize
    def div(self, other):
        return condint_list(self._elementwise(other, dec_div),
                            to_type=self.to_type, cond=self.cond)
    
# ───────────── Vectorized Math Helpers ─────────────
    @stabilize
    def sum(self):
        return condint(sum(self.data), to_type=self.to_type, cond=self.cond)

    @stabilize
    def mean(self):
        if len(self.data) == 0:
            raise ValueError("Cannot compute mean of empty array")
        return condint(dec_div(sum(self.data), len(self.data)), to_type=self.to_type, cond=self.cond)

    @stabilize
    def cumsum(self):
        total = _to_decimal(0)
        result = []
        for x in self.data:
            total += x
            result.append(condint(total, to_type=self.to_type, cond=self.cond))
        return result

    @stabilize
    def dot(self, other):
        if not isinstance(other, BaseArray) or len(other.data) != len(self.data):
            raise ValueError("Dot product requires arrays of same length")
        total = sum(a*b for a, b in zip(self.data, other.data))
        return condint(total, to_type=self.to_type, cond=self.cond)

# ───────────── Array1, Array2, Array3 ─────────────
class Array1(BaseArray):
    """1D array wrapper with Decimal-safe operations."""
    def __init__(self, data, *, to_type=None, cond=None):
        self.data = [_to_decimal(v) for v in data]
        self.to_type = to_type
        self.cond = cond

    def __getitem__(self, idx):
        return condint(self.data[idx], to_type=self.to_type, cond=self.cond)

    def __setitem__(self, idx, value):
        self.data[idx] = _to_decimal(value)

    def to_list(self):
        return [condint(x, to_type=self.to_type, cond=self.cond) for x in self.data]


class Array2(BaseArray):
    """2D array wrapper. Nested lists assumed for input."""
    def __init__(self, data, *, to_type=None, cond=None):
        # flatten inner lists to Decimal lists
        flattened = [[_to_decimal(v) for v in row] for row in data]
        self.data = flattened
        self.to_type = to_type
        self.cond = cond

    def __getitem__(self, idx):
        row = self.data[idx]
        return [condint(x, to_type=self.to_type, cond=self.cond) for x in row]

    def __setitem__(self, idx, value):
        self.data[idx] = [_to_decimal(v) for v in value]

    def to_list(self):
        return [[condint(x, to_type=self.to_type, cond=self.cond) for x in row] for row in self.data]

class Array3(BaseArray):
    """3D array wrapper. Nested 3-level lists assumed for input."""
    def __init__(self, data, *, to_type=None, cond=None):
        # flatten inner lists to Decimal lists
        self.data = [[[ _to_decimal(v) for v in layer] for layer in matrix] for matrix in data]
        self.to_type = to_type
        self.cond = cond

    def __getitem__(self, idx):
        matrix = self.data[idx]
        return [[condint(x, to_type=self.to_type, cond=self.cond) for x in layer] for layer in matrix]

    def __setitem__(self, idx, value):
        self.data[idx] = [[_to_decimal(v) for v in layer] for layer in value]

    def to_list(self):
        return [[[condint(x, to_type=self.to_type, cond=self.cond) for x in layer] for layer in matrix] for matrix in self.data]