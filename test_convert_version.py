######################################
#
# main
if __name__ == "__main__":

    ver11 = 281479278886912  # 1.1.110
    ver21 = 562949955649542  # 2.0.34.xxx
    ver22 = 562949956239363  # 2.0.43.xxx

    def get_version_dict(ver_num):
        def next(ver):
            return ver % 65536, int(ver / 65536)

        d, ver_num = next(ver_num)
        c, ver_num = next(ver_num)
        b, ver_num = next(ver_num)
        a, ver_num = next(ver_num)
        return {"major": a, "minor ": b, "patch": c, "developer": d}

    print(get_version_dict(ver11))
    print(get_version_dict(ver21))
    print(get_version_dict(ver22))
