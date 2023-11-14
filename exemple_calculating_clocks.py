from fractions import Fraction


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

    print(Fraction(8, 60) / 1 / 60)

    # print_fraction(Fraction(8) * Fraction("2187/2000"))
