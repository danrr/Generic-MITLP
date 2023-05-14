from typing import Any, ClassVar

from typing import overload

import gmpy2
Default: int
HAVE_THREADS: bool
RoundAwayZero: int
RoundDown: int
RoundToNearest: int
RoundToZero: int
RoundUp: int

def __getattr__(name) -> Any: ...

class mpz:
    denominator: int
    imag: int
    numerator: int
    real: int
    @classmethod
    def __init__(cls, n) -> mpz: ...
    def bit_clear(self, n) -> mpz: ...
    def bit_count(self) -> int: ...
    def bit_flip(self, n) -> mpz: ...
    @overload
    def bit_length(self) -> int: ...
    @overload
    def bit_length(self) -> Any: ...
    def bit_scan0(self, n = ...) -> int: ...
    def bit_scan1(self, n = ...) -> int: ...
    def bit_set(self, n) -> mpz: ...
    def bit_test(self, n) -> bool: ...
    def conjugate(self) -> number: ...
    def digits(self, *args, **kwargs) -> Any: ...
    def is_congruent(self, y, m) -> bool: ...
    def is_divisible(self, d) -> bool: ...
    def is_even(self) -> bool: ...
    def is_odd(self) -> bool: ...
    def is_power(self) -> bool: ...
    def is_prime(self, *args, **kwargs) -> Any: ...
    def is_square(self) -> bool: ...
    def num_digits(self, *args, **kwargs) -> Any: ...
    def __abs__(self) -> Any: ...
    def __add__(self, other) -> Any: ...
    def __and__(self, other) -> Any: ...
    def __bool__(self) -> bool: ...
    def __ceil__(self, *args, **kwargs) -> int: ...
    def __divmod__(self, other) -> Any: ...
    def __eq__(self, other) -> bool: ...
    def __float__(self) -> float: ...
    def __floor__(self, *args, **kwargs) -> int: ...
    def __floordiv__(self, other) -> Any: ...
    def __format__(self, fmt) -> string: ...
    def __ge__(self, other) -> bool: ...
    def __getitem__(self, index) -> Any: ...
    def __gt__(self, other) -> bool: ...
    def __hash__(self) -> int: ...
    def __index__(self) -> Any: ...
    def __int__(self) -> int: ...
    def __invert__(self) -> Any: ...
    def __le__(self, other) -> bool: ...
    def __len__(self) -> int: ...
    def __lshift__(self, other) -> Any: ...
    def __lt__(self, other) -> bool: ...
    def __mod__(self, other) -> Any: ...
    def __mul__(self, other) -> Any: ...
    def __ne__(self, other) -> bool: ...
    def __neg__(self) -> Any: ...
    def __or__(self, other) -> Any: ...
    def __pos__(self) -> Any: ...
    def __pow__(self, other) -> Any: ...
    def __radd__(self, other) -> Any: ...
    def __rand__(self, other) -> Any: ...
    def __rdivmod__(self, other) -> Any: ...
    def __rfloordiv__(self, other) -> Any: ...
    def __rlshift__(self, other) -> Any: ...
    def __rmod__(self, other) -> Any: ...
    def __rmul__(self, other) -> Any: ...
    def __ror__(self, other) -> Any: ...
    def __round__(self) -> Any: ...
    def __rpow__(self, other) -> Any: ...
    def __rrshift__(self, other) -> Any: ...
    def __rshift__(self, other) -> Any: ...
    def __rsub__(self, other) -> Any: ...
    def __rtruediv__(self, other) -> Any: ...
    def __rxor__(self, other) -> Any: ...
    def __sizeof__(self) -> Any: ...
    def __sub__(self, other) -> Any: ...
    def __truediv__(self, other) -> Any: ...
    def __trunc__(self) -> int: ...
    def __xor__(self, other) -> Any: ...

class xmpz:
    limb_size: ClassVar[int] = ...
    __hash__: ClassVar[None] = ...
    denominator: Any
    numerator: Any
    real: Any
    @classmethod
    def __init__(cls, n) -> xmpz: ...
    def bit_clear(self, n) -> mpz: ...
    def bit_flip(self, n) -> mpz: ...
    @overload
    def bit_length(self) -> int: ...
    @overload
    def bit_length(self) -> Any: ...
    def bit_scan0(self, n = ...) -> int: ...
    def bit_scan1(self, n = ...) -> int: ...
    def bit_set(self, n) -> mpz: ...
    def bit_test(self, n) -> bool: ...
    def conjugate(self) -> number: ...
    def copy(self) -> xmpz: ...
    def digits(self, *args, **kwargs) -> Any: ...
    def iter_bits(self, start = ..., stop = ...) -> iterator: ...
    def iter_clear(self, start = ..., stop = ...) -> iterator: ...
    def iter_set(self, start = ..., stop = ...) -> iterator: ...
    def limbs_finish(self, n) -> Any: ...
    def limbs_modify(self, n) -> int: ...
    def limbs_read(self) -> int: ...
    def limbs_write(self, n) -> int: ...
    def make_mpz(self) -> mpz: ...
    def num_digits(self, *args, **kwargs) -> Any: ...
    def num_limbs(self) -> int: ...
    def __abs__(self) -> Any: ...
    def __add__(self, other) -> Any: ...
    def __and__(self, other) -> Any: ...
    def __bool__(self) -> bool: ...
    def __delitem__(self, other) -> Any: ...
    def __divmod__(self, other) -> Any: ...
    def __eq__(self, other) -> bool: ...
    def __float__(self) -> float: ...
    def __floordiv__(self, other) -> Any: ...
    def __format__(self, fmt) -> string: ...
    def __ge__(self, other) -> bool: ...
    def __getitem__(self, index) -> Any: ...
    def __gt__(self, other) -> bool: ...
    def __iadd__(self, other) -> Any: ...
    def __iand__(self, other) -> Any: ...
    def __ifloordiv__(self, other) -> Any: ...
    def __ilshift__(self, other) -> Any: ...
    def __imod__(self, other) -> Any: ...
    def __imul__(self, other) -> Any: ...
    def __index__(self) -> Any: ...
    def __int__(self) -> int: ...
    def __invert__(self) -> Any: ...
    def __ior__(self, other) -> Any: ...
    def __ipow__(self, other) -> Any: ...
    def __irshift__(self, other) -> Any: ...
    def __isub__(self, other) -> Any: ...
    def __ixor__(self, other) -> Any: ...
    def __le__(self, other) -> bool: ...
    def __len__(self) -> int: ...
    def __lshift__(self, other) -> Any: ...
    def __lt__(self, other) -> bool: ...
    def __mod__(self, other) -> Any: ...
    def __mul__(self, other) -> Any: ...
    def __ne__(self, other) -> bool: ...
    def __neg__(self) -> Any: ...
    def __or__(self, other) -> Any: ...
    def __pos__(self) -> Any: ...
    def __pow__(self, other) -> Any: ...
    def __radd__(self, other) -> Any: ...
    def __rand__(self, other) -> Any: ...
    def __rdivmod__(self, other) -> Any: ...
    def __rfloordiv__(self, other) -> Any: ...
    def __rlshift__(self, other) -> Any: ...
    def __rmod__(self, other) -> Any: ...
    def __rmul__(self, other) -> Any: ...
    def __ror__(self, other) -> Any: ...
    def __rpow__(self, other) -> Any: ...
    def __rrshift__(self, other) -> Any: ...
    def __rshift__(self, other) -> Any: ...
    def __rsub__(self, other) -> Any: ...
    def __rtruediv__(self, other) -> Any: ...
    def __rxor__(self, other) -> Any: ...
    def __setitem__(self, index, object) -> None: ...
    def __sizeof__(self) -> Any: ...
    def __sub__(self, other) -> Any: ...
    def __truediv__(self, other) -> Any: ...
    def __xor__(self, other) -> Any: ...

def _mpmath_create(*args, **kwargs) -> Any: ...
def _mpmath_normalize(*args, **kwargs) -> Any: ...
def _printf(fmt, x) -> string: ...
def acos(x) -> number: ...
def acosh(x) -> number: ...
def add(x, y) -> number: ...
def agm(x, y) -> mpfr: ...
def ai(x) -> number: ...
def asin(x) -> number: ...
def asinh(x) -> number: ...
def atan(x) -> number: ...
def atan2(y, x) -> number: ...
def atanh(x) -> number: ...
def bincoef(n, k) -> mpz: ...
def bit_clear(x, n) -> mpz: ...
def bit_count(x) -> int: ...
def bit_flip(x, n) -> mpz: ...
def bit_length(x) -> int: ...
def bit_mask(n) -> mpz: ...
def bit_scan0(x, n = ...) -> int: ...
def bit_scan1(x, n = ...) -> int: ...
def bit_set(x, n) -> mpz: ...
def bit_test(x, n) -> bool: ...
def c_div(x, y) -> quotient: ...
def c_div_2exp(x, n) -> quotient: ...
def c_divmod(*args, **kwargs) -> Any: ...
def c_divmod_2exp(*args, **kwargs) -> Any: ...
def c_mod(x, y) -> remainder: ...
def c_mod_2exp(x, n) -> remainder: ...
def can_round(b, err, rnd1, rnd2, prec) -> Any: ...
def cbrt(x) -> number: ...
def ceil(x) -> mpfr: ...
def check_range(x) -> mpfr: ...
def cmp(x, y) -> integer: ...
def cmp_abs(x, y) -> integer: ...
def comb(n, k) -> mpz: ...
def const_catalan(*args, **kwargs) -> Any: ...
def const_euler(*args, **kwargs) -> Any: ...
def const_log2(*args, **kwargs) -> Any: ...
def const_pi(*args, **kwargs) -> Any: ...
def context() -> contextmanager: ...
def copy_sign(*args, **kwargs) -> Any: ...
def cos(x) -> number: ...
def cosh(x) -> number: ...
def cot(x) -> number: ...
def coth(x) -> number: ...
def csc(x) -> number: ...
def csch(x) -> number: ...
def degrees(x) -> mpfr: ...
def denom(x) -> mpz: ...
def digamma(x) -> number: ...
def digits(*args, **kwargs) -> Any: ...
def div(x, y) -> number: ...
def div_2exp(x, n) -> number: ...
def divexact(x, y) -> mpz: ...
def divm(a, b, m) -> mpz: ...
def double_fac(n) -> mpz: ...
def eint(x) -> number: ...
def erf(x) -> number: ...
def erfc(x) -> number: ...
def exp(x) -> number: ...
def exp10(x) -> number: ...
def exp2(x) -> number: ...
def expm1(x) -> number: ...
def f2q(*args, **kwargs) -> Any: ...
def f_div(x, y) -> quotient: ...
def f_div_2exp(x, n) -> Any: ...
def f_divmod(*args, **kwargs) -> Any: ...
def f_divmod_2exp(*args, **kwargs) -> Any: ...
def f_mod(x, y) -> remainder: ...
def f_mod_2exp(x, n) -> remainder: ...
def fac(n) -> mpz: ...
def factorial(n) -> mpfr: ...
def fib(n) -> mpz: ...
def fib2(n) -> tuple: ...
def floor(x) -> mpfr: ...
def floor_div(x, y) -> number: ...
def fma(x, y, z) -> number: ...
def fmma(x, y, z, t) -> number: ...
def fmms(x, y, z, t) -> number: ...
def fmod(x, y) -> mpfr: ...
def fms(x, y, z) -> number: ...
def frac(x) -> number: ...
def free_cache() -> Any: ...
def frexp(*args, **kwargs) -> Any: ...
def from_binary(bytes) -> gmpy2object: ...
def fsum(iterable) -> mpfr: ...
def gamma(x) -> number: ...
def gcd(*integers) -> mpz: ...
def gcdext(a, b) -> Any: ...
def get_cache(*args, **kwargs) -> Any: ...
def get_context() -> gmpy2context: ...
def get_emax_max() -> integer: ...
def get_emin_min() -> integer: ...
def get_exp(mpfr) -> integer: ...
def get_max_precision() -> integer: ...
def hamdist(x, y) -> int: ...
def hypot(x, y) -> number: ...
def ieee(*args, **kwargs) -> Any: ...
def invert(x, m) -> mpz: ...
def iroot(*args, **kwargs) -> Any: ...
def iroot_rem(*args, **kwargs) -> Any: ...
def is_bpsw_prp(n) -> bool: ...
def is_congruent(x, y, m) -> bool: ...
def is_divisible(x, d) -> bool: ...
def is_euler_prp(n, a) -> bool: ...
def is_even(x) -> bool: ...
def is_extra_strong_lucas_prp(n, p) -> bool: ...
def is_fermat_prp(n, a) -> bool: ...
def is_fibonacci_prp(n, p, q) -> bool: ...
def is_finite(x) -> bool: ...
def is_infinite(x) -> bool: ...
def is_integer(x) -> bool: ...
def is_lessgreater(x, y) -> bool: ...
def is_lucas_prp(n, p, q) -> bool: ...
def is_nan(x) -> bool: ...
def is_odd(x) -> bool: ...
def is_power(x) -> bool: ...
def is_prime(*args, **kwargs) -> Any: ...
def is_regular(x) -> bool: ...
def is_selfridge_prp(n) -> bool: ...
def is_signed(x) -> bool: ...
def is_square(x) -> bool: ...
def is_strong_bpsw_prp(n) -> bool: ...
def is_strong_lucas_prp(n, p, q) -> bool: ...
def is_strong_prp(n, a) -> bool: ...
def is_strong_selfridge_prp(n) -> bool: ...
def is_unordered(x, y) -> bool: ...
def is_zero(x) -> bool: ...
def isqrt(x) -> mpz: ...
def isqrt_rem(x) -> tuple: ...
def j0(x) -> number: ...
def j1(x) -> number: ...
def jacobi(x, y) -> mpz: ...
def jn(x, n) -> mpfr: ...
def kronecker(x, y) -> mpz: ...
def lcm(*integers) -> mpz: ...
def legendre(x, y) -> mpz: ...
def lgamma(*args, **kwargs) -> Any: ...
def li2(x) -> number: ...
def license() -> string: ...
def lngamma(x) -> number: ...
def local_context(*args, **kwargs) -> Any: ...

def mpz_random(random_state, int) -> mpz: ...
def mpz_rrandomb(random_state, bit_count) -> mpz: ...
def mpz_urandomb(random_state, bit_count) -> mpz: ...
def next_prime(x) -> mpz: ...
def powmod(x, y, m) -> mpz: ...
def powmod_base_list(base_lst, exp, mod) -> list: ...
def powmod_exp_list(base, exp_lst, mod) -> list: ...

def random_state(*args, **kwargs) -> Any: ...
def to_binary(x) -> bytes: ...