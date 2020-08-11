"""Функция, которая ищет арифметические выражения в тексте,
подставляет начальные значения переменных и считает их"""


def calculate(data, findall):
    "Ищет в тексте выражения вида a+=b+c и считает их"

    matches = findall(r"([abc])(\+|-)?=([abc])?((?:\+|-)?\d+)?")
    for var1, sign1, var2, sign2_num in matches:
        tmp = int(sign2_num or 0)+data.get(var2, 0)
        if not var2 and not sign2_num:
            continue
        if not sign1:
            data[var1] = tmp
        else:
            if sign1 == "+":
                data[var1] += tmp
            else:
                data[var1] -= tmp
    return data
