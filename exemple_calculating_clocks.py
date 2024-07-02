from fractions import Fraction
from math import ceil


def print_fraction(num):
    print("{:0.3f} ( {} )".format(float(num), num))


def new_fraction(str):
    res = Fraction(0.0)
    for a in str.split():
        # print('a = ', type(a), a)
        res += Fraction(a)

    return res


######################################
#
# main
if __name__ == "__main__":
    item_per_sec = Fraction("0") + Fraction("1/6")

    print()
    print("==================")
    print("")
    print()
    print(item_per_sec / 1 / 60)

    print()
    print("==================")
    print("")
    print()
    print_fraction(Fraction(4) / (Fraction(4) + Fraction("8/25")))

    print_fraction(Fraction(7) * new_fraction("1701/2500") / new_fraction("4 463/1160"))

    print()
    print("==================")
    print("")
    print()

    print(Fraction(5 * 15, 1) / new_fraction("12 13/36"))

    # print_fraction(Fraction(8) * Fraction("2187/2000"))

    print()
    print("==================")
    print("соотношение сторон у монитора")
    print()
    print_fraction(new_fraction("3840/2160"))
    print_fraction(new_fraction("640/360"))
    print_fraction(new_fraction("640/480"))

    print()
    print("==================")
    print("")
    print()
    print_fraction(new_fraction("1 1/10") / 9 / 60)
    print_fraction(1000000 / new_fraction("256 1/2"))

    ore = 4000
    delta = 100
    while ore > 0:
        if ore % 24 == 0:
            print(ore / delta, ore, ore % 24)
        ore -= delta

    print()
    print("==================")
    print("RC")
    print()

    for rc in range(100, 5000):
        copper = new_fraction("1 1/49") * rc
        copper = new_fraction("2 6/7") * rc
        gc = new_fraction("1 3/7") * rc
        plastic = new_fraction("1 3/7") * rc

        s1 = ceil(copper / 100)
        s1 = ceil(copper / 200)
        s2 = ceil(gc / 200)
        s3 = ceil(plastic / 100)
        slots = s1 + s2 + s3

        print(
            "rc = {:5d} copper = {:<10.3f} gc = {:<10.3f} plastic = {:<10.3f} slots = {}".format(
                rc, float(copper), float(gc), float(plastic), slots
            )
        )
        print("\tcopper = {} gc = {} plastic = {}".format(s1, s2, s3))
        print("разгрузка = {:<10.2f}s".format((s1 * 100 + s2 * 200 + s3 * 100) / 27))
        print("производство = {:<10.2f}".format(float(rc / new_fraction("1 17/60"))))
        if slots > 37:
            break

    print()
    print("==================")
    print("solar panels")
    print()

    for panel in range(100, 5000):

        copper = new_fraction("5") * panel
        gc = new_fraction("15") * panel
        steel = new_fraction("5") * panel

        s1 = ceil(copper / 100)
        s2 = ceil(gc / 200)
        s3 = ceil(steel / 100)
        slots = s1 + s2 + s3

        print(
            "panel = {:5d} copper = {:<10.3f} gc = {:<10.3f} plastic = {:<10.3f} slots = {}".format(
                panel, float(copper), float(gc), float(steel), slots
            )
        )
        print("\tcopper = {} gc = {} steel = {}".format(s1, s2, s3))
        # print("разгрузка = {:<10.2f}s".format((s1 * 100 + s2 * 200 + s3 * 100) / 27))
        # print("производство = {:<10.2f}".format(float(rc / new_fraction("1 17/60"))))
        if slots > 39:
            break
