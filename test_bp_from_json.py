from bp_from_json import blueprint, print_id, entity


#############################################
#
# main
if __name__ == "__main__":
    bp_txt = '0eNqd2tFumzAYxfF34TpUNcb2IU8yaaommritNUIiIO2qKu8+SLYma1HXfy/j' +\
             'cj6w++PmiJfsttnHXZfaIVu+ZGm1bfts+f0l69N9WzfT2vC8i9kyS0PcZIusr' +\
             'TfTr65OTXZYZKldx1/Z0hwW/43UfR83t01q7/NNvXpIbcztxYhidsRj6ob9uP' +\
             'I65XRF/u0iaWeTd80+rc+5p3qI3UWoPNwsstgOaUjxtOPjj+cf7X5zO165NB8' +\
             '/+CLbbfsxvG2ne44DfXBXbpE9j8ng7ZUbb9XFVTodRLdt8/tYd/nTQ4zTbqaj' +\
             '6adkv4txnW+2630Tjze9XMiL90v2uLTrxl+rIT2Oj3z5l8N0Fm92UpwPb6hXP' +\
             '/PU9rGbTmNmD+HtHtZp3MXpkmJmtv3a7OLtbD8zu7yYPZ5avnqI/TA3WP8Onh' +\
             'nlzg6223VsPzXLzs/yF481vgb3D0N+fBveD5N5HTU3KHxh0OwT6QuDwmF6AYb' +\
             'U/NH/7iCKv1deH17HN3W7vkvN9OZ/lDA4UeCExYkSJxxOeJwIOCGcqGgifPp/' +\
             'brESi5VYrMRiJRYrsViJxUosVmKxEouVWKykxEpKrKTESkqspMRKSqykxEpKr' +\
             'KTESkqspMRKHFbisBKHlTisxGElDitxWInDShxW4rASh5V4rMRjJR4r8ViJx0' +\
             'o8VuKxEo+VeKzEYyUeKwlYScBKAlYSsJKAlQSsJGAlASsJWEnASgJWIqxEWIm' +\
             'wEmElwkqElQgrEVYirERYibCSCiupsJIKK6mwkgorqbCSCiupsJIKK6mwkooq' +\
             '0TVVck4YnChwwuJEiRMOJzxOBJwQTlQ08XklBisxWInBSgxWYrASg5UYrMRgJ' +\
             'QYrMViJwUpw9yrcvQp3r8Ldq3D3Kty9Cnevwt2rcPcq3L0Kd6/C3atw9yrcvQ' +\
             'p3r8Ldq3D3Kty9Cnevwt2rcPcq3L0Kd6/C3atw9yrcvQp3r8Ldq3D3Kty9Cne' +\
             'vwt2rcPcq3L0Kd6/C3atw9yrcvQp3r8Ldq3D3Kty9Cnev+rh7vTl9pDCunb8Q' +\
             'WWSPsetPHwPIlKEqRjBeGk/78BsNtKk1'
    bp_book_txt = '0eNrtlNtugzAMht8l10k1oBxfZZqqABZEhQQlabuq4t2XgNayNttou5t' +\
                  'JXCHb8WebxP8J5c0OOsm43uRCbFF2ungUyl4npo2xQvDRrVjFaWN9+tg' +\
                  'ByhDT0CKMOG2tJSlrUI8R4yW8o8zr8a8pVClo84bxirS0qBkHEkwQfv+' +\
                  'GEXDNNIOxhcE4bviuzUGaGj+TMOqEMsmC2w4MMI2CVYjR0WQGcboKTSk' +\
                  'JBRs7k4KTCqgkhxqgMcm2V2UzVQdQklaUuwaGolMH8W9dweDqpLEKzfa' +\
                  'm5Wmkt3/mahL/PInStNgSxhVIbSKOGcLLDMkwQ8nMFOORyMEOHmOn12z' +\
                  'fwV6f2QchSuCkqEFpFzn6Snawwkmf5gZmoRI3KpqgzLusak2G5+mApee' +\
                  'uXKD4flDivODkAVDQ2wUYViabLCVGe5BqvJLEW8epH4dpEJvvZXVebAu' +\
                  '3i37NIkMAI2qfKWw+k+dU8NwVvpOS5w8sYrSI0SJG/1OMHJlPSM9f87z' +\
                  '5PG8Oz79PGhdhW4RtEbZF2Mwb+hsh6j8AHNaICQ=='

    bp1 = blueprint.from_string(bp_txt)
    bp2 = blueprint.from_string(bp_book_txt)
    bp3 = blueprint.from_file('bp.txt')
    bp4_txt = '0eNqdk9tugzAMht/F16RaoRxfZZqmABZYCwElabuq4t3n' +\
              'gNSxLtqhl3bw5//H9hVqdcTJkHZQXYGaUVuonq9gqdNS+' +\
              'Zy7TAgVkMMBItBy8JGRpGCOgHSL71Dt5+jXEmktDrUi3Y' +\
              'lBNj1pFMkGEc8vEaB25AhXCUtwedXHoUbDPX4mRTCNlot' +\
              'H7RUwsMySXRrBhSuTvNyl3MpgQ6syM2rRoTTi3CMqLvZa' +\
              'ra+0E2IrhrE9KlyabhMi/p5KltRkOGocnVjy9mX2f+bOS' +\
              'XxzYp1s3gRpi8bxS8BD+umhWDy0xC7WT7IAO3mMXd6z4w' +\
              'D7cGOfx7FFLZoerQuRs6/kACvd6OQJ/AlVhFHZBsV72fV' +\
              'OLOsZgJU3VSFQ/n9QERxw8QAomf0BLCdTbY4yAiVr3lDO' +\
              'TXuOTmjsOqBif8jLOM+esqLIDvP8ASH5Owg='
    bp4 = blueprint.from_string(bp4_txt)

    print("bp1")
    print(bp1.to_str())

    print("bp2")
    print(bp2.to_str())

    print("bp3")
    # print(bp3.to_str())

    print("bp4")
    print(bp4.to_str())
    print()

    print_id("bp1", bp1)
    print_id("bp2", bp2)
    print_id("bp3", bp3)

    print('------------------------------')
    print(bp1.get_all_items())

    print('------------------------------')
    print(bp2.get_all_items())

    print('------------------------------')
    print(bp3.get_all_items())
    print('------------------------------')

    bps = bp2.get_all_bp()
    print(bps)
    '''
    for level in range(len(bps)):
        for x in range(len(bps[level])):
            str = '{}{}'.format(level, x)
            # print(str,' '*level,bps[level][x].read_item(),
            #       '\t',bps[level][x].read_label())
            bps[level][x].set_label(str)
    '''

    bps = bp2.get_all_bp(onedimensional=True, blueprint_only=True)
    n = 1
    for a in bps:
        a.set_label('bp{}'.format(n))
        n += 1

    bp2.set_label_color(1, 0, 1)
    bp2.set_description("dhjshdfjkskjdfjsd\nshdgfhgsjdhfgjhsdgf")

    bp2.set_icons(1, 'virtual', 'signal-Z')
    bp2.set_icons(2, 'virtual', 'signal-S')
    bp2.set_icons(3, 'virtual', 'signal-L')
    bp2.set_icons(4, 'virtual', 'signal-A')
    bp2.set_icons(1, 'virtual', 'signal-1')

    print()
    print(bp2.to_str())

    print()
    print(bp1.get_all_tiles())
    print(bp2.get_all_tiles())
    print(bp3.get_all_tiles())

    e = entity.new_entity('stack-inserter', 70, 35)
    e.update_items({'nuclear-fuel': 3})
    e = entity.new_entity('locomotive', 70, 35)
    e.update_items({'nuclear-fuel': 3})

    """
    print()
    print_id("", bp1.get_md5())
    print_id("", bp2.get_md5())
    print_id("", bp3.get_md5())
    """

    '''
    print()
    bps = bp2.get_all_bp(onedimensional=True, blueprint_only=True)
    for a in bps:
        print('****************************')
        print(a.to_str())
        print('****************************')
        print()
    '''

#    print('****************************')
#    print('print(bp1.compare(bp2))')
#    print(bp1.compare(bp2))

#    print('****************************')
#    print('print(bp4.compare(bp2))')
#    print(bp4.compare(bp2))

    """
    print()
    bp4 = blueprint.from_string(bp_txt)
    print(bp1.compare(bp4))
    print()
    bp4.set_label("1")
    print(bp1.compare(bp4))
    """

    """
    print('****************************')
    bp1.print_entities()
    print('----------------------------')
    bp4.print_entities()
    """

    print('****************************')
    print('print(bp1.compare(bp4))')
    print(bp1.compare(bp4))

    """
    print('****************************')
    bp1.print_entities()
    print('----------------------------')
    bp4.print_entities()
    """

    print()
    print("bp1")
    print('bp_txt == bp1.to_str():', bp_txt == bp1.to_str())

    print("bp4")
    print('bp4_txt == bp4.to_str()', bp4_txt == bp4.to_str())
    print()
