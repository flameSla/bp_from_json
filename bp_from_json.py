import base64
import collections
import json
import zlib
import hashlib


#############################################
class position():
    def __init__(self, obj):
        self.data = obj

    @classmethod
    def new_position(cls, x, y):
        return cls({'x': x, 'y': y})

    @classmethod
    def from_dict(cls, d):
        return cls(d)

    def __iadd__(self, other):
        self.data['x'] += other.data['x']
        self.data['y'] += other.data['y']
        return self

    def __isub__(self, other):
        self.data['x'] -= other.data['x']
        self.data['y'] -= other.data['y']
        return self

    def __str__(self):
        return "{{'x': {0}, 'y': {1}}}".format(self.data['x'],
                                               self.data['y'])

    def read_x(self):
        return self.data['x']

    def read_y(self):
        return self.data['y']


#############################################
class entity():
    def __init__(self, obj):
        self.data = obj

    @classmethod
    def new_entity(cls, name, pos_x, pos_y,
                   direction=None, orientation=None):
        entity = dict()
        entity['entity_number'] = 0
        entity['name'] = name
        entity['position'] = position.new_position(pos_x, pos_y)
        if direction is not None:
            entity['direction'] = direction
        if orientation is not None:
            entity['orientation'] = orientation
        return cls(entity)

    def update_items(self, item, name_verification=True):
        entity_may_contain_items = (
            'artillery-turret',
            'artillery-wagon',
            'assembling-machine-1',
            'assembling-machine-2',
            'assembling-machine-3',
            'beacon',
            'boiler',
            'burner-inserter',
            'burner-mining-drill',
            'cargo-wagon',
            'centrifuge',
            'chemical-plant',
            'electric-furnace',
            'electric-mining-drill',
            'gun-turret',
            'iron-chest',
            'lab',
            'locomotive',
            'nuclear-reactor',
            'oil-refinery',
            'pumpjack',
            'roboport',
            'rocket-silo',
            'steel-chest',
            'steel-furnace',
            'stone-furnace',
            'wooden-chest')

        if self.data['name'] in entity_may_contain_items or\
           name_verification is False:
            if 'items' in self.data:
                self.data['items'].update(item)
            else:
                self.data['items'] = item
        else:
            print(f"Warning! '{self.data['name']}' cannot contain items")

    def set_inventory_filter(self, filtr):
        if 'inventory' not in self.data:
            self.data['inventory'] = dict()

        if 'filters' not in self.data['inventory']:
            self.data['inventory']['filters'] = list()

        self.data['inventory']['filters'].append(filtr)

    def read_name(self):
        return self.data['name']

    def read_items(self):
        if 'items' in self.data:
            return self.data['items']
        else:
            return dict()

    def read_recipe(self):
        if 'recipe' in self.data:
            return self.data['recipe']
        else:
            return None

    def __eq__(self, other):
        a = self.data.copy()
        b = other.data.copy()
        a['entity_number'] = 0
        b['entity_number'] = 0
        return a == b

    def get_pos(self):
        return position(self.data['position'])


#############################################
def print_id(s, a):
    print(s, '\t', id(a), '\t', a, '\t', type(a))


#############################################
def get_items():
    # read json file
    with open('items.json', 'r') as read_file:
        json_items = json.load(read_file)

    # json -> dist()
    items = dict_bp()
    for i in json_items['items']:
        items[i['name']] = float(i['stack'])  # items["wooden-chest"] = 50.0

    return items


#############################################
class dict_bp(dict):
    def __add__(self, other):
        temp = dict_bp(self)
        for key, value in other.items():
            if key in temp:
                temp[key] += value
            else:
                temp[key] = value
        return temp

    def __iadd__(self, other):
        for key, value in other.items():
            if key in self:
                self[key] += value
            else:
                self[key] = value
        return self

    def __str__(self):
        s = str()
        for k, v in self.items():
            s += '"{}" = {}\n'.format(k, v)
        return s


#############################################
class blueprint:
    def __init__(self, data):
        self.data = data
        if 'blueprint_book' in self.data:
            self.obj = self.data['blueprint_book']
        elif 'blueprint' in self.data:
            self.obj = self.data['blueprint']
        else:
            self.data = None
            self.obj = None

    @classmethod
    def new_blueprint(cls):
        bp_json = collections.OrderedDict()
        bp_json['blueprint'] = collections.OrderedDict()
        # bp_json['blueprint']['description'] = str()
        # bp_json['blueprint']['icons'] = list()
        # [{'signal': {'type': 'virtual', 'name': 'signal-a'}, 'index': 1}]
        bp_json['blueprint']['entities'] = list()
        # bp_json['blueprint']['tiles'] = list()
        # bp_json['blueprint']['schedules'] = list()
        bp_json['blueprint']['item'] = 'blueprint'
        # bp_json['blueprint']['label'] = str()
        # bp_json['blueprint']['label_color']
        bp_json['blueprint']['version'] = 281479275937792

        return cls(bp_json)

    @classmethod
    def from_string(cls, str):
        version_byte = str[0]
        if version_byte == '0':
            json_str = zlib.decompress(base64.b64decode(str[1:]))
            bp_json = json.loads(json_str,
                                 object_pairs_hook=collections.OrderedDict)
        else:
            print('Warning! The version byte is currently 0 '
                  '(for all Factorio versions through 1.1)')
            print('Warning! Unsupported version: {0}'.format(version_byte))
            bp_json = None

        return cls(bp_json)

    @classmethod
    def from_file(cls, filename):
        exchange_str = ''
        with open(filename, 'r') as f:
            exchange_str = f.read()

        return cls.from_string(exchange_str)

    def to_str(self):
        json_str = json.dumps(self.data,
                              separators=(",", ":"),
                              ensure_ascii=False).encode("utf8")
        exchange_str = '0' + base64.b64encode(zlib.compress(json_str,
                                                            9)).decode('utf-8')
        return exchange_str

    def __get_all_items_parse(self, bp, items):
        if bp.is_blueprint_book():
            for b in bp.read_blueprints():
                self.__get_all_items_parse(blueprint(b), items)
        elif bp.is_blueprint():
            for entity in bp.get_entities():
                if entity.read_name() == 'curved-rail':
                    items += {"rail": 4}
                elif entity.read_name() == 'straight-rail':
                    items += {"rail": 1}
                else:
                    items += {entity.read_name(): 1}
                items += entity.read_items()

    def get_all_items(self):
        items = dict_bp()
        self.__get_all_items_parse(self, items)
        return items

    def __get_all_tiles_parse(self, bp, tiles):
        if bp.is_blueprint_book():
            for b in bp.read_blueprints():
                self.__get_all_tiles_parse(blueprint(b), tiles)
        elif bp.is_blueprint():
            for t in bp.read_tiles():
                tiles += {t['name']: 1}

    def get_all_tiles(self):
        tiles = dict_bp()
        self.__get_all_tiles_parse(self, tiles)
        return tiles

    def __get_all_bp_parse(self, bp, bps, current_directory):
        if bp.is_blueprint_book():
            md5 = bp.get_md5()
            current_directory += md5 + '\\'
            bps.append([bp, md5, current_directory])
            for b in bp.read_blueprints():
                self.__get_all_bp_parse(blueprint(b), bps, current_directory)
        elif bp.is_blueprint():
            md5 = bp.get_md5()
            bps.append([bp, md5, current_directory])

    def get_all_bp(self,
                   onedimensional=False,
                   blueprint_only=False):
        bps = list()
        self.__get_all_bp_parse(self, bps, '')

        if onedimensional is False:
            return bps
        elif onedimensional is True:
            temp = list()
            for a in bps:
                if blueprint_only is False:
                    temp.append(a[0])
                else:
                    if a[0].is_blueprint():
                        temp.append(a[0])
            return temp
        else:
            return list()

    def is_blueprint_book(self):
        if self.data is not None:
            return 'blueprint_book' in self.data

    def is_blueprint(self):
        if self.data is not None:
            return 'blueprint' in self.data

    def read_blueprints(self):
        return self.obj.get('blueprints', list())

    def get_entities(self):
        return list(map(lambda x: entity(x), self.obj['entities']))

    def normalize_entities(self):
        # position -= pos_min
        x = list()
        y = list()
        entities = self.get_entities()
        for e in entities:
            x.append(e.get_pos().read_x())
            y.append(e.get_pos().read_y())

        pmin = position.new_position(min(x), min(y))
        for e in entities:
            e.get_pos().__isub__(pmin)

    def read_tiles(self):
        return self.obj.get('tiles', list())

    def read_label(self):
        return self.obj.get('label', 'untitled')

    def set_label(self, str):
        self.obj['label'] = str

    def read_description(self):
        return self.obj.get('description', 'description is missing')

    def set_description(self, str):
        self.obj['description'] = str

    def read_label_color(self):
        return self.obj.get('label_color', None)

    def set_label_color(self, r, g, b):
        self.obj['label_color'] = {"r": r, "g": g, "b": b}

    def read_icons(self):
        return self.obj.get('icons', None)

    def read_schedules(self):
        return self.obj.get('schedules', list())

    def read_version(self):
        return self.obj.get('version', '')

    def set_icons(self, index, icon_type, name):
        new_icon = {'signal': {'type': icon_type, 'name': name},
                    'index': index}
        if index >= 1 and index <= 4:
            if 'icons' in self.obj:
                if index in [icon['index'] for icon in self.obj['icons']]:
                    for i in range(len(self.obj['icons'])):
                        if self.obj['icons'][i]['index'] == index:
                            self.obj['icons'][i] = new_icon
                            break
                else:
                    self.obj['icons'].append(new_icon)
            else:
                self.obj['icons'] = [new_icon]

    def read_item(self):
        return self.obj['item']

    def __md5(self, data):
        return hashlib.md5(json.dumps(data,
                           sort_keys=True).encode('utf-8')).hexdigest()

    def get_md5(self):
        return self.__md5(self.data)

    def __compare_entities(self, bp, debug):
        e1 = sorted(self.get_entities(),
                    key=lambda a: (a.data['position']['x'],
                                   a.data['position']['y']))
        e2 = sorted(bp.get_entities(),
                    key=lambda a: (a.data['position']['x'],
                                   a.data['position']['y']))
        if e1 == e2:
            return True
        else:
            '''
            print("len1={} len2={}".format(len(e1), len(e2)))
            for i in range(len(e1)):
                print(f"{i} ", e1[i].data)
                print(f"{i} ", e2[i].data)
            '''
            return False

    def __compare_bp_bp(self, bp, debug):
        result = dict()
        if debug:
            print("blueprint vs bplueprint")
        result['md5'] = self.get_md5() == bp.get_md5()
        if result['md5'] and debug:
            print('md5 are equal')
        result['label'] = self.read_label() == bp.read_label()
        if result['label'] and debug:
            print('label are equal')
        result['label_color'] = \
            self.read_label_color() == bp.read_label_color()
        if result['label_color'] and debug:
            print('label_color are equal')
        result['description'] = \
            self.read_description() == bp.read_description()
        if result['description'] and debug:
            print('description are equal')
        self.normalize_entities()
        bp.normalize_entities()
        result['entities'] = self.__compare_entities(bp, debug)
        if result['entities'] and debug:
            print('entities are equal')
        result['tiles'] = self.read_tiles() == bp.read_tiles()
        if result['tiles'] and debug:
            print('tiles are equal')
        result['icons'] = self.read_icons() == bp.read_icons()
        if result['icons'] and debug:
            print('icons are equal')
        result['schedules'] = self.read_schedules() == bp.read_schedules()
        if result['schedules'] and debug:
            print('schedules are equal')
        result['version'] = self.read_version() == bp.read_version()
        if result['version'] and debug:
            print('version are equal')
        return [self.get_md5(), bp.get_md5(), result]

    def __compare_bp_book(self, bp, debug):
        result = list()
        if debug:
            print("blueprint vs book")
        for b in bp.get_all_bp(onedimensional=True, blueprint_only=True):
            result.append(self.__compare_bp_bp(b, debug))
        return result

    def compare(self, bp, debug=False):
        if self.is_blueprint() and bp.is_blueprint():
            return self.__compare_bp_bp(bp, debug)
        elif self.is_blueprint_book() and bp.is_blueprint_book():
            return {}
        else:
            if self.is_blueprint():
                return self.__compare_bp_book(bp, debug)
            else:
                return bp.__compare_bp_book(self, debug)


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
    print(bp1.to_str())

    print("bp3")
    print(bp1.to_str())

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

    p1 = position.new_position(10, 10)
    p2 = position.new_position(1, 1)

    print()
    print(p1)
    print(p2)
    p1 += p2
    print(p1)
    print(p2)
    p1 -= position.new_position(5, 255)
    print(p1)
    print(p2)

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

    print('****************************')
    print('print(bp1.compare(bp2))')
    print(bp1.compare(bp2))

    print('****************************')
    print('print(bp4.compare(bp2))')
    print(bp4.compare(bp2))

    """
    print()
    bp4 = blueprint.from_string(bp_txt)
    print(bp1.compare(bp4))
    print()
    bp4.set_label("1")
    print(bp1.compare(bp4))
    """

    print('****************************')
    print('print(bp1.compare(bp4))')
    print(bp1.compare(bp4))

    """
    print('****************************')
    for e in bp1.get_entities():
        print(e.get_pos(), " ", e.data)
    for e in bp4.get_entities():
        print(e.get_pos(), " ", e.data)
    """
