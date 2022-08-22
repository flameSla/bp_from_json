import os
from bp_from_json import blueprint


################################################################
def set_requests_for_centrifuges(book):
    for bp in book.get_all_bp(onedimensional=True,
                              blueprint_only=True):
        for entity in bp.get_entities():
            if 'centrifuge' in entity.read_name():
                if entity.read_recipe() == 'kovarex-enrichment-process':
                    entity.update_items({'uranium-235': 40},
                                        name_verification=False)
                    bp.set_label_color(1, 0, 1)
                    if bp.read_label() == 'untitled':
                        bp.set_label('ha-ha-ha')


################################################################
#
# main
if __name__ == "__main__":
    DEBUG = True

    if DEBUG:
        # vanilla
        exchange_str1 = '0eNrtl9uOmzAYhN/F17DCP8fkVapVROBPai0YZCDaaMW7' +\
                        '15Cm2WqTylOlF5V86cMMnzmMmA+xbybujdLjbt91b2L7c' +\
                        'ZsZxPbbp+GypqpOX6YHddRls8yN557FVqiRWxEIXbbLqG' +\
                        'I9GnWYjizmQChd87vYyvk1EHZBjYovLuvgvNNTu2djN9z' +\
                        'TB6LvBivp9HI1a5PL9CUNxNnuT1L5ks5z8MWJHJ2K350C' +\
                        'YbhS63kmU2o1tWFvuoqHQemj1S+HHBbx0DPXYdvVU8Nhv' +\
                        'JLbjfVUjepkOT6v3MOL3fBIPsTTU9VwacLDxM0TwRJHsM' +\
                        'QJLDT8T25f6kiZP6R8606l4feQtVHV99a6XB/0EzEzN8w' +\
                        '4+hvM5VsaVfPzQ/ryYidXx2j+RdGUuj6ophEL62OFhBXk' +\
                        'qkhhqhSmSmGqDKbKYKoMpsphqhymymGqAqYqYKoCptrAV' +\
                        'BuYaoNSUYRS3RQSVjhTSZhKwlQSpiKYimAqgqlimCqGqW' +\
                        'KYCs52grOd4GwnONsJznaCs53gbCc42wnOdoKzneBsJzj' +\
                        'bCc52grOd/pztr5efLzt3qx2BOLEZVg8qZJJvKM+irCiy' +\
                        '5NYsouVa7lXGdx3fdXzX8V3Hdx3fdXzX8V3Hdx3fdXzX8' +\
                        'V3nv+g66T1luDaaQJTL7xrvrlvdupOzX+TiJ5/jN/8Axa' +\
                        'ZpIg=='
        # bob mod
        exchange_str2 = '0eNrtldlugzAQRf/FzzgKhgDhV6oqYpkkVsBGXtKgiH+v' +\
                        'TRQFtaZ11VZ9KG944Z7r8XjmispGQycoU7uS8xPKr48Zi' +\
                        'fKnydCu0Yqz27SkB1Y0dk71HaAcUQUtChArWjuqgClB9/' +\
                        'oAOEJDgCir4YLycHgOkFmiisJNZxz0O6bbEoTZ4FYIUMe' +\
                        'l+YkzSzRCOI7Xq02AevMZRWS1MQwBFR2taFEwqlvcCV6B' +\
                        'lJQdjIV3KOKNitJZFNNVA4XAew2NCxL5Q+JZyImfCwEXD' +\
                        'EzQ6tgaofvRjJCNu7QqonjBsgOocctr3QDOUJ4MDk+xv6' +\
                        'dw1lPJSxPXouRauXw5sBtvLMlmsV2jFR8vd4w8lz1TR5D' +\
                        'USUz8iZtZojpyYXn2hrGAj3Mq9SeSWWINWoE/M3MwP3kw' +\
                        'ZOudYA7g1hM4eTZfAL7JaDNd60rRs3EwSWziSuxw7Qo/+' +\
                        'eS1fS8YYejPDH8vHvFgK+tYg/NJyQ7QGYQcTZAsjNMtSZ' +\
                        'N1kmVJ/KjJa3sq/zaw9ImlTyx9YukTS5/4d33C8Sceu0G' +\
                        'ACouC3X3rX+glP6M3vAIYEVMb'

        bp1 = blueprint.from_string(exchange_str1)
        bp2 = blueprint.from_string(exchange_str2)

        print()
        print(bp1.get_all_items())
        print()
        print(bp2.get_all_items())

        set_requests_for_centrifuges(bp1)
        print('---------------------------------')
        print('vanilla')
        print(bp1.to_str())
        print('---------------------------------')
        set_requests_for_centrifuges(bp2)
        print('---------------------------------')
        print('bob mod')
        print(bp2.to_str())
        print('---------------------------------')
    else:
        exchange_str = input('bp:(string or filename.txt)')
        if os.path.exists(exchange_str):
            with open(exchange_str, 'r') as f:
                exchange_str = f.read()

        bp = blueprint.from_string(exchange_str)
        set_requests_for_centrifuges(bp)
        print(bp.to_str())
