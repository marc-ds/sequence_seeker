from math import floor, sqrt
import sympy as sp


def roundz(f):
    """Round any number .5 to the next bigger int used in offset methods"""
    if (f - floor(f)) <= 0.5:
        return int(floor(f))
    else:
        return int(floor(f)) + 1


def isprime(num):
    """Return true to 1 , -1 and any prime, even the negatives."""
    if abs(num) == 1:
        return True
    return sp.isprime(abs(int(num)))


def nextprime(value):
    if value >= 1:
        return sp.nextprime(value)
    elif value == (0 or -1):
        return 1
    elif value == -2:
        return -1
    else:
        negative = sp.prevprime(-value)
        return negative * -1


def prevprime(value):
    if value > 2:
        return sp.prevprime(value)
    elif value == (0 or 1):
        return -1
    elif value == 2:
        return 1
    else:
        negative = sp.nextprime(abs(value))
        return negative * -1


def factorint(value):
    if value == 1:
        tmp = [(1,1)]
        return dict(tmp)
    else:
        return sp.factorint(value)


def x_from_abc(a, b, c, y):
    return int((a * (y ** 2)) + (b * y) + c)


def x0_abc(p1, p2, p3):
    a = (p1 - (2 * p2) + p3) / 2.
    b = (p3 - p1) / 2.
    c = p2

    f = offset(a, b)

    a0 = abs(a)
    b0 = -abs(b + (2 * a * f))
    if a <= 0:
        c0 = -(c + a * (f ** 2) + (b * f))
    else:
        c0 = (c + a * (f ** 2) + (b * f))

    return {'a0': int(a0), 'b0': int(b0), 'c0': int(c0)}


def x0_from_p1p2p3(p1,p2,p3,y):
    x0abc = x0_abc(p1,p2,p3)
    return x_from_abc(x0abc['a0'], x0abc['b0'], x0abc['c0'], y)


def x(p1, p2, p3, y):
    a = (p1 - (2 * p2) + p3) / 2.
    b = (p3 - p1) / 2.
    c = p2
    return (a * (y ** 2)) + (b * y) + c


def y_vertex(a, b):
    if a != 0:
        return -b / (2. * a)
    else:
        return 00


def offset(a, b):
    if a != 0:
        return roundz(y_vertex(a, b))
    else:
        return 00


def data_ctype(value):
    if abs(value) is 1:
        return 'one'
    elif value is 0:
        return 'zero'
    elif isprime(value):
        return 'prime'
    elif not (sqrt(abs(value)) * 10) % 2:
        return 'sqrt_round'
    else:
        return 'composite'


def data_ctypey0(value):
    """Used to show the right colors at y=-1, y=0 and y=1"""
    if abs(value) is 1:
        return 'y0_one'
    elif value is 0:
        return 'zero'
    elif isprime(value):
        return 'y0_prime'
    elif not (sqrt(abs(value)) * 10) % 2:
        return 'y0_sqrt_round'
    else:
        return 'y0_composite'


def header_ctype(value, dark=False):
    value = float(value)
    if not dark:
        if value < 0:
            return 'negative'
        elif value > 0:
            return 'positive'
        else:
            return 'zero'
    else:
        if value < 0:
            return 'negative_dark'
        elif value > 0:
            return 'positive_dark'
        else:
            return 'zero'


def rpdown_positive(value, k):
    if not isprime(value):
        value = prevprime(value)
    yield value
    i = 0
    while i < k - 1:
        value = prevprime(value)
        if value < 1:
            break
        i += 1
        yield value


def rpup_positive(value, k):
    if not isprime(value):
        value = nextprime(value)
    yield value
    i = 0
    while i < k - 1:
        value = nextprime(value)
        i += 1
        yield value


def range_ay2byc(a, b, c, y_init, y_end):
    for y in range(y_init, y_end+1):
        yield x_from_abc(a, b, c, y)


def isinfinity(value):
    if value == 0:
        return '&infin;'
    else:
        return value


def density(a, b, c, y_range):
    primes = int(0)
    for y in y_range:
        if isprime(x_from_abc(a, b, c, y)): primes += 1
    return primes


class X:
    """by P1, P2 and P3 set the values of a, b, c, delta, C.G.,
    y_vertex and offset, when called return f(x) = ay^2 + by + c"""

    def __init__(self, p1, p2, p3):
        """initialize all attributes"""
        self.p1 = p1
        self.p2 = p2
        self.p3 = p3

        self.a = (self.p1 - (2 * self.p2) + self.p3) / 2.
        self.b = (self.p3 - self.p1) / 2.
        self.c = self.p2

        self.y_vertex = y_vertex(self.a, self.b)
        self.offset = offset(self.a, self.b)

        self.delta = (self.b ** 2 - (4 * self.a * self.c))
        sqrtdelta = sqrt(abs(int(self.delta)))
        self.c_g = sqrtdelta - int(sqrtdelta)

        self.a0 = abs(self.a)
        self.b0 = -abs(self.b + (2 * self.a * self.offset))
        if self.a <= 0:
            self.c0 = -(self.c + self.a * (self.offset ** 2) + (self.b * self.offset))
        elif self.a > 0:
            self.c0 = (self.c + self.a * (self.offset ** 2) + (self.b * self.offset))

        self.y0_vertex = y_vertex(self.a0, self.b0)
        self.offset0 = offset(self.a0, self.b0)

        self.x01 = self.a0 - self.b0 + self.c0
        self.x02 = self.c0
        self.x03 = self.a0 + self.b0 + self.c0

        self.x_y0 = x(p1, p2, p3, 0)
        self.y0v_2 = self.y0_vertex ** 2

        if self.a != 0:
            self.xv = (-1 * self.delta) / (4 * abs(self.a))
            self.lr = 1 / abs(self.a)
            self.c0_a = self.c0 / abs(self.a)
            self.y0v_2c0a = (self.y0v_2 - self.c0) / self.a
        else:
            self.xv = 00
            self.lr = 00
            self.c0_a = 00
            self.y0v_2c0a = 00

        self.xvlr = -self.xv * self.lr
        self.y0vp_xv_lr = self.y0_vertex - self.xv + self.lr
        self.y0vm_xv_lr = self.y0_vertex + self.xv + self.lr
        self.par_type = self.par_type()

    def __call__(self, y):
        """return the value of f(x) = ay^2 + by + c"""
        return x_from_abc(self.a, self.b, self.c, y)

    def when_f0(self, y):
        """return the value of f(x) = ay^2 + by + c when offset is 0"""
        return x_from_abc(self.a0, self.b0, self.c0, y)

    def density_pos(self, yn):
        return density(self.a, self.b, self.c, range(1, yn + 1))

    def density_neg(self, yn):
        return density(self.a, self.b, self.c, range(-yn + 1, 1))

    def density_pos0(self, yn):
        return density(self.a0, self.b0, self.c0, range(1, yn + 1))

    def density_neg0(self, yn):
        return density(self.a0, self.b0, self.c0, range(-yn + 1, 1))

    def type(self, y0=False):
        """return if the number are abs(one), composite, prime or a perfect sqrt"""
        if y0:
            return data_ctypey0(self.x_y0)
        else:
            return data_ctype(self.x_y0)

    def type0(self, y0=False):
        """return if the number when f0 are
        abs(one), composite, prime or a perfect sqrt"""
        if y0:
            return data_ctypey0(self.x_y0)
        else:
            return data_ctype(self.x_y0)

    def yv_type(self):
        return header_ctype(self.y_vertex)

    def f_type(self):
        return header_ctype(self.offset)

    def d_type(self):
        return header_ctype(self.delta)

    def cg_type(self):
        return header_ctype(self.c_g)

    def yv_type0(self):
        return header_ctype(self.y0_vertex)

    def f_type0(self):
        return header_ctype(self.offset0)

    def par_type(self):
        if self.y0_vertex == 0:
            return 'SUB'
        elif self.y0_vertex < 0.5 > 0:
            return 'ACC'
        elif self.y0_vertex == 0.5:
            return 'DES'
        else:
            return 'none'

