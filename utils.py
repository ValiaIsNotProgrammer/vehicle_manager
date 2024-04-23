# from math import radians, sin, cos, sqrt, atan2 ...
pi = 3.141592653589793

def calculate_distance(lat1: float, lon1: float, lat2: float, lon2: float) -> float:
    """
    Серф интернета привел меня к формуле гаверсинусов,
     где нужно относительно радуаса земного шара расчитать растояние между двумя координатами
     основной рефернс - https://otvet.mail.ru/question/213148016 , https://congyuzhou.medium.com/%D1%80%D0%B0%D1%81%D1%81%D1%82%D0%BE%D1%8F%D0%BD%D0%B8%D0%B5-%D0%BC%D0%B5%D0%B6%D0%B4%D1%83-%D0%B4%D0%B2%D1%83%D0%BC%D1%8F-%D1%82%D0%BE%D1%87%D0%BA%D0%B0%D0%BC%D0%B8-%D0%BD%D0%B0-%D0%BF%D0%BE%D0%B2%D0%B5%D1%80%D1%85%D0%BD%D0%BE%D1%81%D1%82%D0%B8-%D0%B7%D0%B5%D0%BC%D0%BB%D0%B8-a398352bfbde

     Radians = pi/180 * degrees
     x = sin^2 (delta lon / 2) + cos(lon1) * cos(lon2) * sin^2 (delta lon / 2)
     y = 2 * atan2 (x**0/5, (1-x)**0/5)
     d = R * y
     где delta lon = lon1 - lon2; delta lat = lat1 - lat2, R ~ 6371

    """
    radius = 6371.0

    lat1 = _radians(lat1)
    lon1 = _radians(lon1)
    lat2 = _radians(lat2)
    lon2 = _radians(lon2)

    # delta's
    dlon = lon2 - lon1
    dlat = lat2 - lat1

    # Формула гаверсинусов для расчета расстояния
    # from math import sin, cos
    x = sin(dlat / 2) ** 2 + _cos(lat1) * _cos(lat2) * sin(dlon / 2) ** 2
    y = 2 * _atan2((x ** 0.5), ((1 - x) ** 0.5)) # число в степени 1/2, как мы знаем - квадратный корень

    # Расстояние между двумя точками
    distance = radius * y

    return distance


# тут уже гораздно проще, чем с нахождением расстояния.
def find_closest_point(reference_point: tuple[float, float], points: list[tuple[float, float]]) -> tuple[float, float]:
    min_distance = float('inf')
    # from manager import VehicleManager
    # vs = VehicleManager().get_vehicles()
    closest_point = None

    ref_lat, ref_lon = reference_point

    for point in points:
        lat, lon = point
        distance = calculate_distance(ref_lat, ref_lon, lat, lon)
        # v = VehicleManager().get_vehicle_from_point(vs, (lat, lon))
        # print("Сейчас самое близкое:", distance, v)

        if distance < min_distance:
            min_distance = distance
            closest_point = point


    return closest_point


def _radians(degrees):
    return (pi / 180) * degrees


def _factorial(n):  # используем кеш, мы же детские задачи по оптимизации проходили)
    hash = {}
    if n == 0:
        return 1
    else:
        if n in hash.keys():
            return hash[n]
        else:
            x = n * _factorial(n - 1)
            hash[n] = x
            return x

# Cеализация функции синуса, косинуса и катангенса через ряд Тейлора


def _pow(base, exponent):
    return base ** exponent
# проверить, работает ли алгоритм можно провсто вместа x подставтиь 90, а далее уже по тригонометрической окружености получаем 1. С косинусом та же история


def sin(x):  # Taylor Expansion of sinx
    k = 0
    sinx = 0
    while x >= pi:
        x -= pi
    if pi > x > pi / 2:
        x = pi - x
    while k < 15:
        sinx += (-1) ** k * x ** (2*k + 1) / _factorial(2 * k + 1)
        k += 1
    return sinx


def _cos(x):
    cosx = sin(pi / 2 - x)
    return cosx

# так как я привык все решать НЕ через ar'танкенсы/катангенсы, то я тут снова воспользовался GPT


def _atan(x, terms=10):
    result = 0
    for n in range(terms):
        result += ((-1) ** n) * (x ** (2 * n + 1)) / (2 * n + 1)
    return result


def _atan2(y, x):
    # Простая аппроксимация atan2, работает хорошо, если y мало по сравнению с x
    if x > 0:
        return _atan(y / x)
    elif y >= 0 > x:
        return _atan(y / x) + pi
    elif y < 0 < x:
        return _atan(y / x) - pi
    elif y <= 0 > x:
        return _atan(y / x) + pi
    elif y > 0 and x == 0:
        return pi / 2
    elif y < 0 and x == 0:
        return -pi / 2




# reference_point = (55.753332, 37.621676)
# points = [
#     (59.829604, 30.374407),
#     (59.965711, 30.311941),
# ]
# closest_point = find_closest_point(reference_point, points)
# print(f"Ближайшая точка: {closest_point}")






