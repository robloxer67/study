import re
from decimal import Decimal

c = r'(?:\d+(?:\.\d+)*)'

def num(x):
    return float(x) if '.' in x else int(x)

def stro(x):
    return format(Decimal(repr(x)), "f")

def norm(x):
    while re.search(r"--|\+\+|\+-|-\+", x):
        x = re.sub(r"--|\+\+", "+", x)
        x = re.sub(r"\+-|-\+", "-", x)
    return re.sub(r"(^|[*/])\+", r"\1", x)

def schet(x):
    x = norm(x)
    while m := re.search(rf"({c})([*/])({c})", x):
        a, b = num(m[1]), num(m[3])
        v = a * b if m[2] == "*" else a / b
        x = x[:m.start()] + stro(v) + x[m.end():]

    x = norm(x)
    while m := re.match(rf"({c})([+-])({c})", x):
        a, b = num(m[1]), num(m[3])
        v = a + b if m[2] == "+" else a - b
        x = stro(v) + x[m.end():]

    if not re.fullmatch(c, x):
        raise ValueError("Ошибка в выражении")
    return num(x)

def poln_schet(x):
    part = [schet(p) for p in x.split("<<")]
    res = part[0]
    for p in part[1:]:
        if res != int(res) or p != int(p) or p < 0:
            raise ValueError("<< работает только с целыми неотрицательными числами")
        res = int(res) << int(p)
    return res

def itog(x):
    if re.search(r"[\d)]\s*(\(|abs)|\)\s*\d|\d\s+\d", x):
        raise ValueError("Пропущен оператор")
    x = re.sub(r"\s+", "", x)

    while m := re.search(r"(abs)?\(([^()]*)\)", x):
        znach = poln_schet(m[2])
        if m[1]:
            znach = abs(znach)
        x = x[:m.start()] + stro(znach) + x[m.end():]

    return poln_schet(x)

while True:
    virag = input("Введите выражение: ")
    if not virag.strip():
        break
    try:
        print("Результат:", stro(itog(virag)))
    except (ValueError, ZeroDivisionError) as e:
        print("Ошибка:", e)
